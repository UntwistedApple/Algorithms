# -*- coding: UTF-8 -*-

import pygame


class Player(object):

    def __init__(self, map):
        self.lines_x = map.lines_x
        self.lines_y = map.lines_y
        self.x = map.player_x
        self.y = map.player_y
        self.speed = 5
        self.rect = pygame.rect.Rect(6, 58, 38, 38)

    def move_up(self):
        self.y -= self.speed
        for line in self.lines_x:
            if line[1] <= self.y + self.speed:
                if self.y <= line[1] and self.x <= line[0][1] and self.x+38 > line[0][0]:
                    self.y = line[1]+2

    def move_down(self):
        self.y += self.speed
        for line in self.lines_x:
            if line[1] >= self.y+38 - self.speed:
                if self.y+38 >= line[1] and self.x <= line[0][1] and self.x+38 > line[0][0]:
                    self.y = line[1]-38

    def move_right(self):
        self.x += self.speed
        for line in self.lines_y:
            if line[0] >= self.x+38 - self.speed:
                if self.x+38 >= line[0] and self.y <= line[1][1] and self.y+38 > line[1][0]:
                    self.x = line[0]-38

    def move_left(self):
        self.x -= self.speed
        for line in self.lines_y:
            if line[0] <= self.x + self.speed:
                if self.x <= line[0] and self.y <= line[1][1] and self.y+38 > line[1][0]:
                    self.x = line[0]+2
