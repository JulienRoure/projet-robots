from classe_robot import Robot
from fonctions import makeMap, draw_grid, update_map, coords_commandes, suite_coords, chemin, write_names
from global_import import walls, stock_1, stock_2, waiting_zone, screen, speed
import pygame
from time import sleep

pygame.init()

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
            if commandes == [] and robot.targets == []:
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