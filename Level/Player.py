# -*- coding: UTF-8 -*-

import pygame
import datetime
import numpy


class Player(object):

    def __init__(self, map):
        if map.is_bot:
            self.fitness = 0
            self.moves = list()
        self.count_moves = 0
        self.time = list()
        self.finish_time = list()
        self.map = map
        self.lines_x = map.lines_x
        self.lines_y = map.lines_y
        self.x = map.player_x
        self.y = map.player_y
        self.speed = 4
        self.rect = pygame.rect.Rect(6, 58, 38, 38)

    def move_up(self):
        self.y -= self.speed
        for line in self.lines_x:
            if line[1] <= self.y + self.speed:
                if self.y <= line[1] and self.x <= line[0][1] and self.x+38 > line[0][0]:
                    self.y = line[1]+2
        self.check_goal()

    def move_down(self):
        self.y += self.speed
        for line in self.lines_x:
            if line[1] >= self.y+38 - self.speed:
                if self.y+38 >= line[1] and self.x <= line[0][1] and self.x+38 > line[0][0]:
                    self.y = line[1]-38
        self.check_goal()

    def move_right(self):
        self.x += self.speed
        for line in self.lines_y:
            if line[0] >= self.x+38 - self.speed:
                if self.x+38 >= line[0] and self.y <= line[1][1] and self.y+38 > line[1][0]:
                    self.x = line[0]-38
        self.check_goal()

    def move_left(self):
        self.x -= self.speed
        for line in self.lines_y:
            if line[0] <= self.x + self.speed:
                if self.x <= line[0] and self.y <= line[1][1] and self.y+38 > line[1][0]:
                    self.x = line[0]+2
        self.check_goal()

    def check_goal(self):
        for goal in self.map.goals:
            if (goal[0]*52-38 < self.x < (goal[0]+1)*52)  and (goal[1]*52-38 < self.y < (goal[1]+1)*52):
                now = str(datetime.datetime.now())
                self.finish_time = list(map(lambda x: int(x), (now[:4], now[5:7], now[8:10], now[11:13], now[14:16], now[17:19], now[20:26])))
                time = tuple(numpy.subtract(self.finish_time, self.map.time))
                for ind in range(len(time)):
                    if ind > 1:
                        self.time.append(time[ind])
                if self.time[1] < 0:
                    self.time[0] -= 1
                    self.time[1] += 24
                if self.time[2] < 0:
                    self.time[1] -= 1
                    self.time[2] += 60
                if self.time[3] < 0:
                    self.time[2] -= 1
                    self.time[3] += 60
                if self.time[4] < 0:
                    self.time[3] -= 1
                    self.time[4] += 1000000
                if not self.map.is_bot:
                    self.map.done(self.time)
                return
        if self.map.is_bot:
            self.count_moves += 1

    def fail(self):
        if not self.map.is_bot:
            self.map.fail()
        else:
            self.map.players = list(filter(lambda x: x != self, self.map.players))
