import pygame
import math
import numpy as np
from time import sleep
from random import random

def colis_to_list(colis):
    return (int(colis[7])-1, int(colis[9])-1)

def count_colis(commandes):
    C = [[0 for _ in range(4)] for _ in range(4)]
    for c in commandes:
        c = colis_to_list(c[0])
        C[c[0]][c[1]] += 1
    return C

speed = 100

zones = {"Zone 1": (1, 2), "Zone 2": (3, 2), "Colis S1.1": [(0, 6), (2, 6)], "Colis S1.2": [(0, 7), (2, 7)], "Colis S1.3": [(0, 8), (2, 8)], "Colis S1.4": [(0, 9), (2, 9)], "Colis S2.1": [(2, 6), (4, 6)], "Colis S2.2": [(2, 7), (4, 7)], "Colis S2.3": [(2, 8), (4, 8)], "Colis S2.4": [(2, 9), (4, 9)], "Colis S3.1": [(4, 6), (6, 6)], "Colis S3.2": [(4, 7), (6, 7)], "Colis S3.3": [(4, 8), (6, 8)], "Colis S3.4": [(4, 9), (6, 9)], "Colis S4.1": [(6, 6), (8, 6)], "Colis S4.2": [(6, 7), (8, 7)], "Colis S4.3": [(6, 8), (8, 8)], "Colis S4.4": [(6, 9), (8, 9)]}

commandes = [("Colis S1.1", "Zone 1"), ("Colis S3.2", "Zone 2"), ("Colis S2.2", "Zone 2"), ("Colis S2.3", "Zone 1"), ("Colis S4.4", "Zone 2"), ("Colis S1.3", "Zone 1"), ("Colis S3.4", "Zone 2"), ("Colis S4.3", "Zone 1"), ("Colis S1.4", "Zone 1"), ("Colis S3.3", "Zone 2"), ("Colis S2.4", "Zone 1"), ("Colis S4.2", "Zone 2"), ("Colis S1.2", "Zone 1"), ("Colis S3.1", "Zone 2"), ("Colis S2.1", "Zone 1"), ("Colis S4.1", "Zone 2")]
colis = count_colis(commandes)

screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode((screen_width, screen_height))

walls = [pygame.Rect(600, 100 , 400, 100),
         pygame.Rect(600, 300 , 400, 100),
         pygame.Rect(600, 500 , 400, 100),
         pygame.Rect(600, 700 , 400, 100),]
stock_1 = [pygame.Rect(200, 100, 100, 100)]
stock_1_o = [pygame.Rect(100, 100, 100, 100)]
stock_2 = [pygame.Rect(200, 300, 100, 100)]
stock_2_o = [pygame.Rect(100, 300, 100, 100)]
waiting_zone = [pygame.Rect(100, 500, 100, 300)]