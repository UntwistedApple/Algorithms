# -*- coding: UTF-8 -*-

import pygame
from numpy import sqrt


class Dot(object):

    def __init__(self, coords, map, speed=7):
        self.img = map.tileset.image
        self.x = coords[0]
        self.y = coords[1]
        self.speed = speed
        self.rect = pygame.rect.Rect(109, 56, 15, 15)

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y), self.rect)


class LineDot(Dot):

    def __init__(self, map, moves):
        Dot.__init__(self, moves[0], map)
        self.moves = moves
        self.ind = 0

    def render(self, screen):
        if (self.x, self.y) == self.moves[self.ind]:
            if self.ind < len(self.moves)-1:
                self.ind += 1
            else:
                self.ind = 0
        needto = list((self.moves[self.ind][0] - self.x, self.moves[self.ind][1] - self.y))
        willdo = self.calc_willdo(needto)
        if willdo is not None:
            if needto[0] < 0:
                self.x -= willdo[0]
            else:
                self.x += willdo[0]
            if needto[1] < 0:
                self.y -= willdo[1]
            else:
                self.y += willdo[1]
        super().render(screen)

    def calc_willdo(self, needto):
        if abs(needto[0]) + abs(needto[1]) < self.speed:
            self.x += needto[0]
            self.y += needto[1]
            return None
        else:
            if needto[0] == 0:
                relx = 0
            elif needto[1] == 0:
                relx = 1
            else:
                if abs(round(needto[0], 6)) == abs(round(needto[1], 6)):
                    relx = 0.5
                else:
                    relx = 1 / (round(needto[1], 6) / round(needto[0], 6) + 1)
            if relx < 0:
                relx = -relx
            willdo = list((self.speed*relx, self.speed*(1-relx)))
            length = sqrt(willdo[0] ** 2 + willdo[1] ** 2)
            adjust = self.speed - length
            willdo[0] += relx*adjust
            willdo[1] += (1-relx)*adjust
            return willdo
