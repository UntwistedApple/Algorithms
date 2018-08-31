# -*- coding: UTF-8 -*-

import pygame


class Button(object):

    def __init__(self, msg, x, y, w, h, bw, tsize, func):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self. h = h
        self.bw = bw
        self.tsize = tsize
        self.font = pygame.font.SysFont('Comic Sans MS', self.tsize)
        self.text = self.font.render(msg, False, (0, 0, 0))
        self.click = func

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.bw, self.y + self.bw, self.w - self.bw * 2, self.h - self.bw * 2))
        screen.blit(self.text, (self.w / 2 + self.x - 12 * len(self.msg) / 2, self.h / 2 + self.y - self.tsize / 2 - 5))

    def load(self):
        pass