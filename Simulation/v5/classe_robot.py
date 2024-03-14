import numpy as np

class Robot:
    def __init__(self, image_path, initial_position, initial_angle, id):
        self.id = id
        self.position = initial_position
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
        self.map = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],])
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
        self.targets_line = []
        self.pos_map = (0, 0)