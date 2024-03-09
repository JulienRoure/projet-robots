from global_import import screen, screen_width, screen_height, speed, zones
import pygame
import math
import numpy as np
from time import sleep

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
    if robot.path == [] and robot.end_chemin and not position_to_case(robot) == robot.targets[0]:
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