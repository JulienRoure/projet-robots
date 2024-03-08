import pygame
import math
import numpy as np
from time import sleep
from random import random

speed = 10

zones = {"Zone 1": (1, 2), "Zone 2": (3, 2), "Colis S1.1": [(0, 6), (2, 6)], "Colis S1.2": [(0, 7), (2, 7)], "Colis S1.3": [(0, 8), (2, 8)], "Colis S1.4": [(0, 9), (2, 9)], "Colis S2.1": [(2, 6), (4, 6)], "Colis S2.2": [(2, 7), (4, 7)], "Colis S2.3": [(2, 8), (4, 8)], "Colis S2.4": [(2, 9), (4, 9)], "Colis S3.1": [(4, 6), (6, 6)], "Colis S3.2": [(4, 7), (6, 7)], "Colis S3.3": [(4, 8), (6, 8)], "Colis S3.4": [(4, 9), (6, 9)], "Colis S4.1": [(6, 6), (8, 6)], "Colis S4.2": [(6, 7), (8, 7)], "Colis S4.3": [(6, 8), (8, 8)], "Colis S4.4": [(6, 9), (8, 9)]}

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

def write_names():
    font = pygame.font.Font('freesansbold.ttf', 24)
    allee_1 = []
    allee_2 = []
    allee_3 = []
    allee_4 = []

    for i in range(1,5):
        name = 'S1.' + str(i)
        textName = font.render(name, True, 'white', 'black')
        textRect = textName.get_rect()
        x = 550+100*i
        textRect.center = (x,150)
        allee_1.append([textName,textRect])

    for i in range(1,5):
        name = 'S2.' + str(i)
        textName = font.render(name, True, 'white', 'black')
        textRect = textName.get_rect()
        x = 550+100*i
        textRect.center = (x,350)
        allee_2.append([textName,textRect])

    for i in range(1,5):
        name = 'S3.' + str(i)
        textName = font.render(name, True, 'white', 'black')
        textRect = textName.get_rect()
        x = 550+100*i
        textRect.center = (x,550)
        allee_3.append([textName,textRect])

    for i in range(1,5):
        name = 'S4.' + str(i)
        textName = font.render(name, True, 'white', 'black')
        textRect = textName.get_rect()
        x = 550+100*i
        textRect.center = (x,750)
        allee_4.append([textName,textRect])

    zones = []

    name = 'Zone 1'
    textName = font.render(name, True, 'white', 'red')
    textRect = textName.get_rect()
    textRect.center = (150,150)
    zones.append([textName,textRect])

    name = 'Zone 2'
    textName = font.render(name, True, 'white', 'orange')
    textRect = textName.get_rect()
    textRect.center = (150,350)
    zones.append([textName,textRect])

    return [allee_1, allee_2, allee_3, allee_4, zones]

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
    def __init__(self, image_path, initial_position, initial_angle, id):
        self.id = id
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
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.targets = []
        self.end_chemin = True
        self.end_test = False
        self.where = []
        self.decharge = True
        self.nb_packages = 0
        self.current = []
        self.state = ""
        self.destination = (0, 0)
        self.can_move = True
        self.blocked = False
        self.dijkstra = True

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

        if self.nb_packages == 0:
            pygame.draw.circle(screen, (0, 128, 0), self.rect.center, 20)  # Cercle vert plein avec un rayon de 20 pixels
        if self.nb_packages == 1:
            pygame.draw.circle(screen, (255, 165, 0), self.rect.center, 20)  # Cercle orange plein avec un rayon de 20 pixels
        if self.nb_packages == 2:
            pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 20)  # Cercle rose plein avec un rayon de 20 pixels

        # Écrire le nombre de colis dans le cercle
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.nb_packages), True, (255, 255, 255))  # Couleur blanche
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

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

def reach_angle(robot, angle_start, mode):
    robot.end_test = True
    angle_diff = (abs(robot.angle_target - robot.angle)) % 360
    angle_diff_start = (abs(robot.angle_target - angle_start)) % 360
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
    if angle_diff_start > 180:
        angle_diff_start = 360 - angle_diff_start
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
                robot.angle_start = robot.angle % 360
                if mode == "colis":
                    robot.nb_packages+=1
                else:
                    robot.nb_packages=0
                if robot.targets == []:
                    robot.decharge = True
                sleep(1/speed)
                
        

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
            robot.end_test = False
            #robot.path = []
            robot.dijkstra = True

def move(robot, case, position_start, angle_start, mode):
    #robot.angle_target = 45*case
    #robot.position_target = (position_start[0] + 50*math.cos(case*math.pi/4), position_start[1] - 50*math.sin(case*math.pi/4))
    if robot.turn:
        reach_angle(robot, angle_start, mode)
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
    
def ind_map(case):
    c = case % 8
    if c == 0:
        return (0, 1)
    elif c == 1:
        return (-1, 1)
    elif c == 2:
        return (-1, 0)
    elif c == 3:
        return (-1, -1)
    elif c == 4:
        return (0, -1)
    elif c == 5:
        return (1, -1)
    elif c == 6:
        return (1, 0)
    elif c == 7:
        return (1, 1)
    
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
            move(robot, robot.path[0], robot.position_start, robot.angle_start, mode)
        else:
            #robot.path = robot.path[c:]
            robot.angle_start = robot.angle % 360
            robot.position_start = (robot.position[0], robot.position[1])
            robot.end = False
    else:
        if mode == "colis 1":
            robot.angle_target = 270
            robot.angle_start = 0
            reach_angle(robot, robot.angle_start, "colis")
        elif mode == "colis 2":
            robot.angle_target = 90
            robot.angle_start = 0
            reach_angle(robot, robot.angle_start, "colis")
        elif mode == "stock":
            robot.angle_target = 180
            if not robot.moving and not robot.end_test:
                robot.angle_start = robot.angle % 360
            reach_angle(robot, robot.angle_start, "stock")
        elif mode == "fin":
            robot.angle_target = 0
            if not robot.moving and not robot.end_test:
                robot.angle_start = robot.angle % 360
            reach_angle(robot, robot.angle_start, "fin")
    
def position_to_case(robot, pos = None):
    if pos == None:
        pos = robot.position
    return (int(pos[1] / 100), int(pos[0] / 100))

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
    for i in range(n):
        for j in range(n):
            if robot.map[i][j] == 1:
                G[i][j] = 100
    if G[reach[0], reach[1]] == 100:
        robot.can_move = False
        return G
    G[reach[0], reach[1]] = 0
    here = reach
    visit = [reach]
    deja_vu = [reach]
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

def dijkstra_path(robot, reach, start = None):
    G = dijkstra(robot, reach)
    if robot.id  == 1:
        print(G)
        print(reach)
    if start == None:
        start = position_to_case(robot)
    distance_start = G[start[0]][start[1]]
    if distance_start > 50:
        robot.blocked = True
        robot.path = []
        return 100
    if robot.path == []:
        P = []
        next = 0
        distance = G[start[0]][start[1]]
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
                        break
            if test:
                for points in around(start[0], start[1]):
                    if G[points[0], points[1]] == distance - 1:
                        next = points
                        P.append(next)
                        distance -= 1
                        robot.path.append(inv_ind(next[1] - start[1], next[0] - start[0]))
                        start = next
                        break
            test = True
    robot.can_move = True
    robot.blocked = False
    return distance_start

def suite_coords(robot):
    if robot.path == [] and robot.end_chemin:
        if robot.targets != []:
            robot.destination = robot.targets.pop(0)
        d = dijkstra_path(robot, robot.destination)
        if d != 100:
            robot.state = robot.current.pop(0)
            robot.end_chemin = False
        else:
            robot.targets.append(robot.destination)
    if robot.path != [] and robot.targets != [] and robot.end_chemin and not robot.moving:
        dijkstra_path(robot, robot.targets[0])
    if robot.dijkstra:
        robot.path = []
        dijkstra_path(robot, robot.destination)
        robot.dijkstra = False
    if robot.blocked and robot.state == "stock":
        robot.path = []
        dijkstra_path(robot, robot.destination)
        
def min_index(L):
    m = L[0]
    index = 0
    for i in range(len(L)):
        if L[i] < m:
            m = L[i]
            index = i
    return index

def coords_commandes(robot, commandes):
    new_commandes = []
    current = []
    zone = ""
    if commandes != []:
        d1 = dijkstra_path(robot, zones[commandes[0][0]][0])
        robot.path = []
        d2 = dijkstra_path(robot, zones[commandes[0][0]][1])
        robot.path = []
        if d2 > d1 and d1 != 100:
            new_commandes.append(zones[commandes[0][0]][0])
            current.append("colis 1")
        elif d2 != 100:
            new_commandes.append(zones[commandes[0][0]][1])
            current.append("colis 2")
        zone = commandes[0][1]
        commandes.pop(0)
    D = []
    for i in range(min(len(commandes), 3)):
        if commandes[i][1] == zone and new_commandes != []:
            d1 = dijkstra_path(robot, zones[commandes[i][0]][0], new_commandes[0])
            robot.path = []
            d2 = dijkstra_path(robot, zones[commandes[i][0]][1], new_commandes[0])
            robot.path = []
            D.append(min(d1, d2))
        else:
            D.append(100)
    if D != []:
        index = min_index(D)
        if commandes[index][1] == zone and new_commandes != []:
            d1 = dijkstra_path(robot, zones[commandes[index][0]][0], new_commandes[0])
            robot.path = []
            d2 = dijkstra_path(robot, zones[commandes[index][0]][1], new_commandes[0])
            robot.path = []
            if d2 > d1 and d1 != 100:
                new_commandes.append(zones[commandes[index][0]][0])
                current.append("colis 1")
            elif d2 != 100:
                new_commandes.append(zones[commandes[index][0]][1])
                current.append("colis 2")
            commandes.pop(index)
    if new_commandes != []:
        new_commandes.append(zones[zone])
        current.append("stock")
    else:
        new_commandes = [(4 + robot.id, 1)]
        current = ["fin"]
    return new_commandes, current

def update_map(robot, robots):
    robot.map = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    for other_robot in robots:
        if other_robot != robot:
            pos = position_to_case(other_robot)
            robot.map[pos[0]][pos[1]] = 1
            if other_robot.path != []:
                path = other_robot.path[0]
                direction = ind_map(path)
                count = 1
                pos = (pos[0] + direction[0], pos[1] + direction[1])
                if pos[0] < 10 and pos[1] < 10 and pos[0] >= 0 and pos[1] >= 0: 
                    robot.map[pos[0]][pos[1]] = 1
                while count < len(other_robot.path) and path == other_robot.path[count]:
                    pos = (pos[0] + direction[0], pos[1] + direction[1])
                    if pos[0] < 10 and pos[1] < 10 and pos[0] >= 0 and pos[1] >= 0:
                        robot.map[pos[0]][pos[1]] = 1
                    count += 1
            if other_robot.destination[1] >= 6:
                line = other_robot.destination[0]
                robot.map[line][6] = 1
                robot.map[line][7] = 1
                robot.map[line][8] = 1
                robot.map[line][9] = 1
            


def main():
    tick = 0
    grille = True
    robot1 = Robot("robot.png", (150, 550), 0, 1)

    commandes = [("Colis S1.1", "Zone 1"), ("Colis S3.2", "Zone 2"), ("Colis S2.2", "Zone 2"), ("Colis S2.3", "Zone 1"), ("Colis S4.4", "Zone 2"), ("Colis S1.3", "Zone 1"), ("Colis S3.4", "Zone 2"), ("Colis S4.3", "Zone 1"), ("Colis S1.4", "Zone 1"), ("Colis S3.3", "Zone 2"), ("Colis S2.4", "Zone 1"), ("Colis S4.2", "Zone 2"), ("Colis S1.2", "Zone 1"), ("Colis S3.1", "Zone 2"), ("Colis S2.1", "Zone 1"), ("Colis S4.1", "Zone 2")]
    #robot1.path = [2, 1, 1, 1, 0]
    #robot1.targets = [(0, 6)]
    robot2 = Robot("robot.png", (150, 650), 0, 2)
    robot3 = Robot("robot.png", (150, 750), 0, 3)
    #robots = [robot1, robot2, robot3]
    #robot1.path = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3]
    robots = [robot1, robot2, robot3]
    #robot2.path = [1, 2, 5, 5, 3, 1, 0, 7, 6, 4, 2, 0]
    #robot3.path = [2, 3, 6, 6, 4, 2, 1, 0, 7, 5, 3, 1]
    clock = pygame.time.Clock()
    running = True

    while running:
        tick += 1
        screen.fill((255, 255, 255))  # Efface l'écran en le remplissant de blanc
        
        makeMap(walls, "black")
        makeMap(stock_1, "red")  
        makeMap(stock_2,"orange")
        makeMap(waiting_zone,"blue")

        allTexts = write_names()

        for text in allTexts[0]:
            screen.blit(text[0], text[1])
        for text in allTexts[1]:
            screen.blit(text[0], text[1])
        for text in allTexts[2]:
            screen.blit(text[0], text[1])
        for text in allTexts[3]:
            screen.blit(text[0], text[1])
        for text in allTexts[4]:
            screen.blit(text[0], text[1])

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        if tick % 10 == 1:
            for robot in robots:
                update_map(robot, robots)

        for robot in robots:
            if tick % 10 == 1:
                update_map(robot, robots)
            
            robot.moving = False  # Réinitialisation de la variable moving
            if robot.targets == [] and robot.decharge and commandes != []:
                robot.targets, robot.current = coords_commandes(robot, commandes)
                robot.decharge = False
            if commandes == []:
                robot.targets = [(4 + robot.id, 1)]
                robot.current = ["fin"]

            suite_coords(robot)

            if not robot.blocked:
                chemin(robot, robot.state)

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

            robot.collision(walls)
            for other_robot in robots:
                if other_robot != robot:
                    robot.collision([other_robot.rect])
            robot.apply_pid()
            robot.draw()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_g]:
            grille = not grille
            sleep(0.05)

        if grille:
            draw_grid()
        
        pygame.display.flip()
        clock.tick(speed*60)  # Limite la boucle à 60 images par seconde pour une animation fluide

    pygame.quit()

if __name__ == "__main__":
    main()
