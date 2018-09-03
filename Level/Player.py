# -*- coding: UTF-8 -*-

import pygame


class Player(object):

    def __init__(self, map):
        self.x = map.player_x
        self.y = map.player_y
        self.speed = 5
        self.rect = pygame.rect.Rect(6, 58, 38, 38)

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def move_right(self):
        self.x += self.speed

    def move_left(self):
        self.x -= self.speed
