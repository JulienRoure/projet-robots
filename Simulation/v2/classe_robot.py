from global_import import screen, walls
import pygame
import math
import numpy as np

class Robot:
    def __init__(self, image_path, initial_position, initial_angle, id):
        self.id = id
        self.rect = pygame.Rect(initial_position[0], initial_position[1], 1, 1)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (70, 70))
        self.position = pygame.Vector2(initial_position)
        self.angle = 0
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
            self.current_speed_left += power
            self.current_speed_right += power
        elif action == "reculer":
            self.current_speed_left -= power
            self.current_speed_right -= power
        elif action == "gauche":
            self.current_speed_left -= power
            self.current_speed_right += power
        elif action == "droite":
            self.current_speed_left += power
            self.current_speed_right -= power
        elif action == "gauche_avancer":
            self.current_speed_left -= power / 2
        elif action == "droite_avancer":
            self.current_speed_right -= power / 2
        elif action == "gauche_reculer":
            self.current_speed_left += power / 2
        elif action == "droite_reculer":
            self.current_speed_right += power / 2

        #self.current_speed_left = max(-1, min(1, self.current_speed_left))
        #self.current_speed_right = max(-1, min(1, self.current_speed_right))

        self.moving = True

    def move(self):
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

    def draw_circle(self):
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

    def draw_map(self):
        print("oui")
        for i in range(10):
            for j in range(10):
                if self.map[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(j*100, i*100, 100, 100))

    def collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
            # Déterminer la direction générale du mouvement
                moving_forward = self.current_speed_left + self.current_speed_right > 0

                if moving_forward:
                    # Si le robot avance et heurte un obstacle, reculer légèrement
                    self.current_speed_left = -0.1
                    self.current_speed_right = -0.1
                else:
                    # Si le robot recule et heurte un obstacle, avancer légèrement
                    self.current_speed_left = 0.1
                    self.current_speed_right = 0.1

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