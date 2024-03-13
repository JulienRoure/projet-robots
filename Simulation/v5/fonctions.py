from global_import import speed, zones, colis
import math
import numpy as np
from time import sleep

def position_to_colis(robot):
    if robot.state == "colis 1":    
        return (int(robot.position[1]/200), int(robot.position[0]/100)-6)
    elif robot.state == "colis 2":
        return (int(robot.position[1]/200)-1, int(robot.position[0]/100)-6)

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
                    robot.nb_packages += 1
                    c = position_to_colis(robot)
                    colis[c[0]][c[1]] -= 1
                    if robot.targets[0] == position_to_case(robot):
                        if robot.state == robot.current[0]:
                            robot.nb_packages += 1
                            colis[c[0]][c[1]] -= 1
                            robot.targets.pop(0)
                            robot.current.pop(0)
                        else:
                            robot.end_chemin = False
                            robot.state = robot.current.pop(0)
                            robot.targets.pop(0)
                else:
                    robot.nb_packages = 0
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
        if robot.current_speed_left == 0 and robot.current_speed_right == 0:
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
    virtual = False
    map_real = robot.map
    G = np.array([[99 for i in range(n)] for j in range(n)])
    for i in range(n):
        for j in range(n):
            if robot.map[i][j] == 1:
                G[i][j] = 100
    if G[reach[0], reach[1]] == 100:
        robot.can_move = False
        robot.map = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        virtual = True
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
    robot.map = map_real
    return G, virtual

def path_to_targets(robot):
    robot.targets_line = []
    pos = position_to_case(robot)
    count = 0
    current = 0
    if robot.path != []:
        current = robot.path[0]
    for i in range(len(robot.path)+1):
        if i < len(robot.path) and current == robot.path[i]:
            count += 1
            direction = ind_map(current)
            pos = (pos[0] + direction[0], pos[1] + direction[1])
        else:
            if robot.path != []:
                robot.targets_line.append(pos)
            if i < len(robot.path):
                current = robot.path[i]
            count = 1

def path_tronqué(robot):
    d = 0
    pos = position_to_case(robot)
    for i in range(len(robot.path)):
        direction = ind_map(robot.path[i])
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        if robot.map[pos[0]][pos[1]] == 1:
            d = i
            break
    robot.path = robot.path[:d]

def dijkstra_path(robot, reach, start = None):
    G, virtual = dijkstra(robot, reach)
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
    if virtual:
        path_tronqué(robot)
    if virtual and robot.path == []:
        robot.blocked = True
        return 100
    return distance_start

def suite_coords(robot):
    if robot.path == [] and robot.end_chemin:
        print("------------------------------------")
        if robot.targets != []:
            robot.destination = robot.targets.pop(0)
        if robot.targets != [] and robot.destination == robot.targets[0]:
            robot.targets.pop(0)
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
    if robot.blocked:
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
                            [0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    for other_robot in robots:
        if other_robot != robot:
            pos = position_to_case(other_robot)
            pos_start = position_to_case(other_robot, other_robot.position_start)
            robot.map[pos[0]][pos[1]] = 1
            if other_robot.path != []:
                path = other_robot.path[0]
                direction = ind_map(path)
                count = 1
                pos_start = (pos_start[0] + direction[0], pos_start[1] + direction[1])
                if pos_start[0] < 10 and pos_start[1] < 10 and pos_start[0] >= 0 and pos_start[1] >= 0: 
                    robot.map[pos_start[0]][pos_start[1]] = 1
                while count < len(other_robot.path) and path == other_robot.path[count]:
                    pos_start = (pos_start[0] + direction[0], pos_start[1] + direction[1])
                    if pos_start[0] < 10 and pos_start[1] < 10 and pos_start[0] >= 0 and pos_start[1] >= 0:
                        robot.map[pos_start[0]][pos_start[1]] = 1
                    count += 1
                pos_start = position_to_case(other_robot, other_robot.position_start)
                while pos != pos_start:
                    robot.map[pos_start[0], pos_start[1]] = 0
                    pos_start = (pos_start[0] + direction[0], pos_start[1] + direction[1])
            if other_robot.destination[1] >= 5:
                line = other_robot.destination[0]
                robot.map[line][5] = 1
                robot.map[line][6] = 1
                robot.map[line][7] = 1
                robot.map[line][8] = 1
                robot.map[line][9] = 1
            if pos[1] >= 5 and pos[0] != 9:
                line = pos[0]
                robot.map[line][5] = 1
                robot.map[line][6] = 1
                robot.map[line][7] = 1
                robot.map[line][8] = 1
                robot.map[line][9] = 1