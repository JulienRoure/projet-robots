from classe_robot import Robot
from fonctions import makeMap, draw_grid, update_map, coords_commandes, suite_coords, chemin, write_names
from global_import import walls, stock_1, stock_2, waiting_zone, screen, speed, commandes, colis, stock_1_o, stock_2_o
import pygame
from time import sleep

pygame.init()

def main():
    tick = 0
    grille = True
    grille_key_released = True
    texts = True
    texts_key_released = True
    pause = False
    pause_key_released = True
    visu_robot = 0
    visu_robot_key_released = True
    robot1 = Robot("robot1.png", (150, 550), 0, 1)
    robot2 = Robot("robot2.png", (150, 650), 0, 2)
    robot3 = Robot("robot3.png", (150, 750), 0, 3)
    robots = [robot1, robot2, robot3]
    clock = pygame.time.Clock()
    running = True

    while running:
        tick += 1
        screen.fill((255, 255, 255))  # Efface l'écran en le remplissant de blanc
        
        makeMap(walls, "black")
        makeMap(stock_1, "red") 
        makeMap(stock_1_o, "black") 
        makeMap(stock_2,"orange")
        makeMap(stock_2_o, "black")
        makeMap(waiting_zone,"blue")
        
        allTexts = write_names(colis)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if grille:
            draw_grid()

        for robot in robots:
            if robot.id == visu_robot:
                robot.draw_map()

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
                if robot.current_speed_left > 0.01:
                    robot.current_speed_left -= 0.01
                elif robot.current_speed_left < -0.01:
                    robot.current_speed_left += 0.01
                else:
                    robot.current_speed_left = 0
                if robot.current_speed_right > 0.01:
                    robot.current_speed_right -= 0.01
                elif robot.current_speed_right < -0.01:
                    robot.current_speed_right += 0.01
                else:
                    robot.current_speed_right = 0

            robot.collision(walls)
            for other_robot in robots:
                if other_robot != robot:
                    robot.collision([other_robot.rect])
            robot.move()
            robot.draw()
            if texts:
                robot.draw_circle()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_g]:
            if grille_key_released:
                grille = not grille
                grille_key_released = False
        else:
            grille_key_released = True 

        if keys[pygame.K_t]:
            if texts_key_released:
                texts = not texts
                texts_key_released = False
        else:
            texts_key_released = True

        if keys[pygame.K_p]:
            if pause_key_released:
                pause = not pause
                pause_key_released = False
        else:
            pause_key_released = True

        if keys[pygame.K_KP0]:
            if visu_robot_key_released:
                visu_robot = 0
                visu_robot_key_released = False
        else:
            visu_robot_key_released = True

        if keys[pygame.K_KP1]:
            if visu_robot_key_released:
                visu_robot = 1
                visu_robot_key_released = False
        else:
            visu_robot_key_released = True
        
        if keys[pygame.K_KP2]:
            if visu_robot_key_released:
                visu_robot = 2
                visu_robot_key_released = False
        else:
            visu_robot_key_released = True

        if keys[pygame.K_KP3]:
            if visu_robot_key_released:
                visu_robot = 3
                visu_robot_key_released = False
        else:
            visu_robot_key_released = True

        if pause:
            sleep(0.1)
            continue
        
        if texts:
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
        
        pygame.display.flip()
        clock.tick(speed*60)  # Limite la boucle à 60 images par seconde pour une animation fluide

    pygame.quit()

if __name__ == "__main__":
    main()