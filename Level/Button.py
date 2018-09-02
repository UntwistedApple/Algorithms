# -*- coding: UTF-8 -*-

import pygame
import os
import Player


class Button(object):

    def __init__(self, msg, x, y, w, h, bw, tsize):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self. h = h
        self.bw = bw
        self.tsize = tsize
        self.text()
        self.clicked = False

    def unclick(self, *args):
        pass

    def text(self):
        self.font = pygame.font.SysFont('Comic Sans MS', self.tsize)
        self.text = self.font.render(self.msg, False, (0, 0, 0))

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.bw, self.y + self.bw, self.w - self.bw * 2, self.h - self.bw * 2))
        screen.blit(self.text, (self.w / 2 + self.x - 12 * len(self.msg) / 2, self.h / 2 + self.y - self.tsize / 2 - 5))


class LoadButton(Button):

    def __init__(self, msg, x, y):
        Button.__init__(self, msg, x, y, 150, 75, 10, 30)
        self.clicked = False

    def click(self, map):
        self.clicked = True
        files = os.listdir(os.getcwd() + '\\saves')
        x = self.x + self.w + 5
        y = self.y
        for file in files:
            map.buttons.append(FileButton(file, x, y))
            y += 40
            if y > 400:
                y = self.y
                x += 100

    def unclick(self, map):
        map.buttons = list(filter(lambda x: not isinstance(x, FileButton), map.buttons))
        self.clicked = False


class FileButton(Button):

    def __init__(self, msg, x, y):
        Button.__init__(self, msg, x, y, 150 + 10, 40, 2, 25)

    def text(self):
        self.font = pygame.font.SysFont('Arial', self.tsize)
        self.text = self.font.render(self.msg, False, (0, 0, 0))

    def click(self, map):
        f = open(os.getcwd() + '\\saves\\' + self.msg, 'r')
        lines = f.readlines()
        map.tiles = list()
        for line in lines:
            row = list()
            for char in line:
                if char == 'e':
                    row.append('empty')
                elif char == 'l':
                    row.append('light')
                elif char == 'd':
                    row.append('dark')
                elif char == 'g':
                    row.append('goal')
                elif char == '#':
                    temp = ''
                    coords = list()
                    for l in line:
                        if l == '#':
                            continue
                        elif l == ',':
                            coords.append(int(temp))
                            temp = ''
                        else:
                            temp += l
                    coords.append(int(temp))
                    map.player_x = coords[0]
                    map.player_y = coords[1]
            map.tiles.append(row)
        map.players = list()
        map.players.append(Player.Player(map))
        map.buttons = list(filter(lambda x: not isinstance(x, FileButton), map.buttons))
