import pygame
import math
import numpy as np
from time import sleep

# Initialisation de Pygame
pygame.init()

# Configuration de l'écran
screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode((screen_width, screen_height))

walls = [pygame.Rect(600, 100 , 400, 100),
         pygame.Rect(600, 300 , 400, 100),
         pygame.Rect(600, 500 , 400, 100),
         pygame.Rect(600, 700 , 400, 100),] #(x,y,width,length), x,y du coin supérieur gauche
stock_1 = [pygame.Rect(100, 100, 200, 100)]
stock_2 = [pygame.Rect(100, 300, 200, 100)]
waiting_zone = [pygame.Rect(100, 500, 100, 300)]

def draw_grid():
    # Couleur de la grille
    color = (0, 0, 0) # Noir
    # Épaisseur des lignes
    thickness = 1
    # Dessin des lignes verticales et horizontales
    for x in range(0, screen_width+1, 100):
        pygame.draw.line(screen, color, (x, 0), (x, screen_height), thickness)
    for y in range(0, screen_height+1, 100):
        pygame.draw.line(screen, color, (0, y), (screen_width, y), thickness)

class Robot:
    def __init__(self, image_path, initial_position, initial_angle):
        self.rect = pygame.Rect(initial_position[0], initial_position[1], 1, 1)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (70, 70))
        self.position = pygame.Vector2(initial_position)
        self.angle = 0
        self.target_speed_left = 0
        self.target_speed_right = 0
        self.current_speed_left = 0
        self.current_speed_right = 0
        self.L = 50  # Distance entre les roues en pixels
        self.Kp, self.Ki, self.Kd = 0.5, 0.0004, 0.3
        self.integral_left = self.integral_right = 0
        self.last_error_left = self.last_error_right = 0
        self.moving = False
        self.angle_target = 0
        self.position_target = (0, 0)
        self.position_diff_start = 0
        self.temps = 0
        self.S = [False for i in range(4)]
        self.turn = True
        self.end = False
        self.path = []
        self.A = []
        self.P = []
        self.angle_start = initial_angle
        self.position_start = initial_position
        self.map = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.targets = []
        self.end_chemin = True

    def update(self, action):
        # Méthode pour mettre à jour la vitesse en fonction de l'action
        power = 0.01
        if action == "avancer":
            self.target_speed_left += power
            self.target_speed_right += power
        elif action == "reculer":
            self.target_speed_left -= power
            self.target_speed_right -= power
        elif action == "gauche":
            self.target_speed_left -= power
            self.target_speed_right += power
        elif action == "droite":
            self.target_speed_left += power
            self.target_speed_right -= power
        elif action == "gauche_avancer":
            self.target_speed_left -= power / 2
        elif action == "droite_avancer":
            self.target_speed_right -= power / 2
        elif action == "gauche_reculer":
            self.target_speed_left += power / 2
        elif action == "droite_reculer":
            self.target_speed_right += power / 2

        #self.target_speed_left = max(-1, min(1, self.target_speed_left))
        #self.target_speed_right = max(-1, min(1, self.target_speed_right))

        self.moving = True

    def apply_pid(self):
        # Application du PID pour chaque roue et mise à jour de la position et de l'angle
        for side in ['left', 'right']:
            target_speed = self.target_speed_left if side == 'left' else self.target_speed_right
            current_speed = self.current_speed_left if side == 'left' else self.current_speed_right
            last_error = self.last_error_left if side == 'left' else self.last_error_right
            integral = self.integral_left if side == 'left' else self.integral_right

            error = target_speed - current_speed
            integral += error
            derivative = error - last_error
            command = self.Kp * error + self.Ki * integral + self.Kd * derivative
            current_speed += command

            if side == 'left':
                self.current_speed_left, self.last_error_left, self.integral_left = current_speed, error, integral
            else:
                self.current_speed_right, self.last_error_right, self.integral_right = current_speed, error, integral
        
        if abs(self.target_speed_left) < 0.01 and not self.moving:
            self.current_speed_left = 0
        if abs(self.target_speed_right) < 0.01 and not self.moving:
            self.current_speed_right = 0

        # Calcul de la vitesse et de la rotation globales
        v = (self.current_speed_left + self.current_speed_right) / 2
        omega = (self.current_speed_right - self.current_speed_left) / self.L
        self.angle += math.degrees(omega)
        self.position[0] += math.cos(math.radians(self.angle)) * v
        self.position[1] += -math.sin(math.radians(self.angle)) * v

    def draw(self):
        # Rotation et affichage du robot
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, new_rect.topleft)
        self.rect = pygame.Rect(self.position[0]-35, self.position[1]-35, 70, 70)

    def collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
            # Déterminer la direction générale du mouvement
                moving_forward = self.current_speed_left + self.current_speed_right > 0

                if moving_forward:
                    # Si le robot avance et heurte un obstacle, reculer légèrement
                    self.target_speed_left = -0.1
                    self.target_speed_right = -0.1
                else:
                    # Si le robot recule et heurte un obstacle, avancer légèrement
                    self.target_speed_left = 0.1
                    self.target_speed_right = 0.1

                # Ajuster la position pour éviter que le robot ne reste coincé dans l'obstacle
                adjustment = pygame.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)))
                if moving_forward:
                    self.position -= adjustment * 10  # Reculer
                else:
                    self.position += adjustment * 10  # Avancer
                self.rect.topleft = self.position

    def tourner(self, angle, eps):
        angle_rel = angle - self.angle
        while abs(angle_rel) > eps:
            if angle_rel%360 > 0 and angle_rel%360 < 180:
                self.update("droite")
            else:
                self.update("gauche")
            self.collision(walls)
            self.apply_pid()
            self.draw()
            angle_rel = angle - self.angle


def makeMap(coord, color):
    for rect in coord:
        pygame.draw.rect(screen, color, rect)

def reach_angle(robot, angle_start):
    angle_diff = (abs(robot.angle_target - robot.angle)) % 360
    angle_diff_start = (abs(robot.angle_target - angle_start)) % 360
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
    if angle_diff_start > 180:
        angle_diff_start = 360 - angle_diff_start
    #print(angle_diff)
    if angle_diff > angle_diff_start/2:
        robot.moving = True
        if (robot.angle_target - robot.angle) % 360 < 180:
            robot.update("gauche")
        else:
            robot.update("droite")
    else:
        robot.moving = False
        if robot.current_speed_left == 0 and robot.current_speed_right == 0:
            robot.angle = robot.angle_target
            if not robot.end_chemin and robot.path == []:
                robot.end_chemin = True
                sleep(1)
        

def reach_position(robot, position_start):
    position_diff = math.sqrt((robot.position_target[0] - robot.position[0])**2 + (robot.position_target[1] - robot.position[1])**2)
    position_diff_start = math.sqrt((robot.position_target[0] - position_start[0])**2 + (robot.position_target[1] - position_start[1])**2)
    #print(position_diff)
    if position_diff > position_diff_start/2:
        robot.moving = True
        robot.update("avancer")
    else:
        robot.moving = False
        if robot.current_speed_left == 0 and robot.current_speed_right == 0:
            robot.position = [robot.position_target[0], robot.position_target[1]]
            robot.turn = True
            robot.end = True

def move(robot, case, position_start, angle_start):
    #robot.angle_target = 45*case
    #robot.position_target = (position_start[0] + 50*math.cos(case*math.pi/4), position_start[1] - 50*math.sin(case*math.pi/4))
    if robot.turn:
        reach_angle(robot, angle_start)
        if robot.target_speed_left == 0 and robot.target_speed_right == 0:
            robot.turn = False
            robot.moving = True
    else:
        reach_position(robot, position_start)

def ind(case):
    c = case % 8
    if c == 0:
        return (1, 0)
    elif c == 1:
        return (1, 1)
    elif c == 2:
        return (0, 1)
    elif c == 3:
        return (-1, 1)
    elif c == 4:
        return (-1, 0)
    elif c == 5:
        return (-1, -1)
    elif c == 6:
        return (0, -1)
    elif c == 7:
        return (1, -1)
    
def inv_ind(i, j):
    if i == 1 and j == 0:
        return 0
    elif i == 1 and j == 1:
        return 7
    elif i == 0 and j == 1:
        return 6
    elif i == -1 and j == 1:
        return 5
    elif i == -1 and j == 0:
        return 4
    elif i == -1 and j == -1:
        return 3
    elif i == 0 and j == -1:
        return 2
    elif i == 1 and j == -1:
        return 1

def chemin(robot, mode):
    if robot.path != []:
        c = 0
        for p in robot.path:
            if p == robot.path[0]:
                c += 1
            else:
                break
        robot.angle_target = 45*robot.path[0]
        robot.position_target = (robot.position_start[0] + c*100*ind(robot.path[0])[0], robot.position_start[1] - c*100*ind(robot.path[0])[1])
        if not robot.end:
            move(robot, robot.path[0], robot.position_start, robot.angle_start)
        else:
            robot.path = robot.path[c:]
            robot.angle_start = robot.angle % 360
            robot.position_start = (robot.position[0], robot.position[1])
            robot.end = False
    else:
        if mode == "colis":
            robot.angle_target = 90
            robot.angle_start = 0
            reach_angle(robot, robot.angle_start)
        if mode == "stock":
            robot.angle_target = 0
            robot.angle_start = 90
            reach_angle(robot, robot.angle_start)
    
def position_to_case(robot):
    return (int(robot.position[1] / 100), int(robot.position[0] / 100))

def around(i, j):
    if i == 0 and j == 0:
        return [(0, 1), (1, 0), (1, 1)]
    elif i == 0 and j == 9:
        return [(0, 8), (1, 9), (1, 8)]
    elif i == 9 and j == 0:
        return [(8, 0), (9, 1), (8, 1)]
    elif i == 9 and j == 9:
        return [(8, 9), (9, 8), (8, 8)]
    elif i == 0:
        return [(0, j-1), (1, j), (0, j+1), (1, j-1), (1, j+1)]
    elif i == 9:
        return [(9, j-1), (8, j), (9, j+1), (8, j-1), (8, j+1)]
    elif j == 0:
        return [(i-1, 0), (i, 1), (i+1, 0), (i-1, 1), (i+1, 1)]
    elif j == 9:
        return [(i-1, 9), (i, 8), (i+1, 9), (i-1, 8), (i+1, 8)]
    else:
        return [(i-1, j), (i, j+1), (i+1, j), (i, j-1), (i-1, j-1), (i-1, j+1), (i+1, j+1), (i+1, j-1)]

def impossible_move(robot, start, end):
    if start[0] + 1 == end[0]  and start[1] + 1 == end[1]:
        if robot.map[start[0]][start[1] + 1] == 1 or robot.map[start[0] + 1][start[1]] == 1:
            return False
    if start[0] + 1 == end[0] and start[1] - 1 == end[1]:
        if robot.map[start[0]][start[1] - 1] == 1 or robot.map[start[0] + 1][start[1]] == 1:
            return False
    if start[0] - 1 == end[0] and start[1] + 1 == end[1]:
        if robot.map[start[0]][start[1] + 1] == 1 or robot.map[start[0] - 1][start[1]] == 1:
            return False
    if start[0] - 1 == end[0] and start[1] - 1 == end[1]:
        if robot.map[start[0]][start[1] - 1] == 1 or robot.map[start[0] - 1][start[1]] == 1: 
            return False
    return True

def dijkstra(robot, reach):
    n = 10
    G = np.array([[99 for i in range(n)] for j in range(n)])
    G[reach[0], reach[1]] = 0
    here = reach
    visit = [reach]
    deja_vu = [reach]
    for i in range(n):
        for j in range(n):
            if robot.map[i][j] == 1:
                G[i][j] = 100
    while visit != []:
        here = visit.pop(0)
        for points in around(here[0], here[1]):
            if G[points[0], points[1]] != 100:
                if points not in visit and points not in deja_vu and impossible_move(robot, here, points):
                    visit.append(points)
                    deja_vu.append(points)
                    G[points[0], points[1]] = min([G[point[0], point[1]] + 100*(not impossible_move(robot, points, point)) for point in around(points[0], points[1])]) + 1
            else:
                deja_vu.append(here)
    return G

def dijkstra_path(robot, reach):
    if robot.path == []:
        G = dijkstra(robot, reach)
        P = []
        start = position_to_case(robot)
        next = 0
        distance = G[start[0], start[1]]
        while distance != 0:
            test = True
            if robot.path != []:
                for points in around(start[0], start[1]):
                    if G[points[0], points[1]] == distance - 1 and inv_ind(points[1] - start[1], start[0] - points[0]) == robot.path[-1]:
                        next = points
                        P.append(next)
                        distance -= 1
                        robot.path.append(inv_ind(next[1] - start[1], next[0] - start[0]))
                        start = next
                        test = False
            if test:
                for points in around(start[0], start[1]):
                    if G[points[0], points[1]] == distance - 1:
                        next = points
                        P.append(next)
                        distance -= 1
                        robot.path.append(inv_ind(next[1] - start[1], next[0] - start[0]))
                        start = next
            test = True

def suite_coords(robot):
    if robot.path == [] and robot.targets != [] and robot.end_chemin:
        dijkstra_path(robot, robot.targets.pop(0))
        robot.end_chemin = False

def main():
    robot1 = Robot("C:/Users/tomdu/OneDrive/Bureau/Centrale/SEC/Projet Commande/robot.png", (150, 550), 0)
    robot1.targets = [(8, 9), (0, 0)]
    #robot2 = Robot("C:/Users/tomdu/OneDrive/Bureau/Centrale/SEC/Projet Commande/robot.png", (150, 650), 0)
    #robot3 = Robot("C:/Users/tomdu/OneDrive/Bureau/Centrale/SEC/Projet Commande/robot.png", (150, 750), 0)
    #robots = [robot1, robot2, robot3]
    #robot1.path = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3]
    robots = [robot1]
    #robot2.path = [1, 2, 5, 5, 3, 1, 0, 7, 6, 4, 2, 0]
    #robot3.path = [2, 3, 6, 6, 4, 2, 1, 0, 7, 5, 3, 1]
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((255, 255, 255))  # Efface l'écran en le remplissant de blanc
        
        makeMap(walls, "black")
        makeMap(stock_1, "red")  
        makeMap(stock_2,"orange")
        makeMap(waiting_zone,"blue")

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        for robot in robots:
            robot.moving = False  # Réinitialisation de la variable moving

            # Gestion des commandes de mouvement basées sur les touches pressées
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                robot.update("gauche_avancer")
            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                robot.update("droite_avancer")
            if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                robot.update("gauche_reculer")
            if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                robot.update("droite_reculer")
            if keys[pygame.K_UP]:
                robot.update("avancer")
            if keys[pygame.K_DOWN]:
                robot.update("reculer")
            if keys[pygame.K_LEFT]:
                robot.update("gauche")
            if keys[pygame.K_RIGHT]:
                robot.update("droite")

            #robot.angle_target = 90
            #reach_angle(robot, 0)

            #robot.position_target = (500, 550)
            #reach_position(robot, (500, 500))
            
            #robot.angle_target = 45
            #reach_angle(robot, robot.angle_start)


            #move(robot, 2, (500, 500), 0)
            #print(robot.end)
            #print(robot.moving)
            if len(robot.targets) % 2 == 1:
                chemin(robot, "colis")
            else:
                chemin(robot, "stock")
            #dijkstra_path(robot, (8, 9))
            suite_coords(robot)
            #print(impossible_move(robot, (3, 5), (4, 6)))
            #print(dijkstra(robot, (0, 0)))
            #print(around(2, 3))
            #print(robot.position_target)
            #print(robot.position)
            #print(robot.angle_target)
            #print(robot.end)


            if not robot.moving:
                if robot.target_speed_left > 0.01:
                    robot.target_speed_left -= 0.01
                elif robot.target_speed_left < -0.01:
                    robot.target_speed_left += 0.01
                else:
                    robot.target_speed_left = 0
                if robot.target_speed_right > 0.01:
                    robot.target_speed_right -= 0.01
                elif robot.target_speed_right < -0.01:
                    robot.target_speed_right += 0.01
                else:
                    robot.target_speed_right = 0

            
            #robot.angle_target = 45
            
            
            
            robot.collision(walls)
            robot.apply_pid()
            robot.draw()
        draw_grid()
        
        pygame.display.flip()
        clock.tick(180)  # Limite la boucle à 60 images par seconde pour une animation fluide

    pygame.quit()

if __name__ == "__main__":
    main()