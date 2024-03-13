from classe_robot import Robot
from fonctions import update_map, coords_commandes, suite_coords, path_to_targets
from global_import import commandes
from math import pi
from time import sleep

def main():
    tick = 0
    visu_robot = 0
    robot1 = Robot("robot1.png", (150, 550), 0, 1)
    robot2 = Robot("robot2.png", (150, 650), 0, 2)
    robot3 = Robot("robot3.png", (150, 750), 0, 3)
    robots = [robot1, robot2, robot3]
    running = True

    while running:
        tick += 1

        for robot in robots:
            if robot.id == visu_robot:
                robot.draw_map()

        if tick % 10 == 1:
            for robot in robots:
                update_map(robot, robots)

        for robot in robots:
            if tick % 10 == 1:
                update_map(robot, robots)

            robot.moving = False
            if robot.targets == [] and commandes != []:
                robot.targets, robot.current = coords_commandes(robot, commandes)
                robot.decharge = False
            if commandes == [] and robot.targets == []:
                robot.targets = [(4 + robot.id, 1)]
                robot.current = ["fin"]

            print("Robot : "+str(robot.id))

            print(commandes)
            print(robot.path)
            print(robot.targets)
            print(robot.targets_line)
            print(robot.destination)
            print(robot.position)
            print(robot.current)

            #récupérer robot_end et la position

            if tick % 50 == robot.id*10:
                robot.dijkstra = True
                robot.end = True
                robot.end_test = False
                if robot.path != []:
                    pos = robot.targets_line.pop(0)
                robot.position = (pos[1]*100+50, pos[0]*100+50)
                if pos == robot.destination:
                    robot.end_chemin = True
                    robot.path = []
                robot.position_start = robot.position
                if robot.path != []:
                    robot.angle = robot.path[0]*45

            suite_coords(robot)

            path_to_targets(robot)
                 
            if not robot.blocked and robot.targets_line != [] and robot.path != []:
                with open("./fichiers_ecriture/robot_target"+str(robot.id)+".txt", "r+") as f:
                    lines = f.readlines()
                    if lines != []:
                        if lines[0] != "("+str(float(robot.targets_line[0][0]))+", "+str(float(robot.targets_line[0][1]))+", "+format(robot.path[0]*45*2*pi/360, ".2f")+")":
                            lines[0] = "("+str(float(robot.targets_line[0][0]))+", "+str(float(robot.targets_line[0][1]))+", "+format(robot.path[0]*45*2*pi/360, ".2f")+")"
                            f.seek(0)
                            f.writelines(lines)
                    else:
                        f.write("("+str(float(robot.targets_line[0][0]))+", "+str(float(robot.targets_line[0][1]))+", "+format(robot.path[0]*45*2*pi/360, ".2f")+")")

if __name__ == "__main__":
    main()