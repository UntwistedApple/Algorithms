# -*- coding: UTF-8 -*-

import pygame
import os
import Player
import platform
import Dots

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
        screen.blit(self.text, (self.w / 2 + self.x - 12 * len(self.msg) / 2 - 5, self.h / 2 + self.y - self.tsize / 2 - 5))


class LoadButton(Button):

    def __init__(self):
        Button.__init__(self, 'Load', 30, 30, 150, 75, 10, 30)
        self.clicked = False

    def click(self, map):
        self.clicked = True
        whichos = platform.system()
        if whichos == 'Linux':
            direct = '/saves'
        elif whichos == 'Windows':
            direct = '\\saves'
        else:
            print('You are running on an unrecognized Operating System!\n' + whichos)
            direct = '/saves'
        files = os.listdir(os.getcwd() + direct)
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


class RestartButton(Button):

    def __init__(self):
        Button.__init__(self, 'Restart', 945, 30, 150, 75, 10, 30)

    def click(self, map):
        map.goal_reached = False
        load(map, map.name)
        map.buttons = list(filter(lambda x: not isinstance(x, RestartButton), map.buttons))
        map.texts = list(filter(lambda x: not x[0] == 'Geschafft!', map.texts))

class FileButton(Button):

    def __init__(self, msg, x, y):
        Button.__init__(self, msg, x, y, 150 + 10, 40, 2, 25)

    def text(self):
        self.font = pygame.font.SysFont('Arial', self.tsize)
        self.text = self.font.render(self.msg, False, (0, 0, 0))

    def click(self, map):
        load(map, self.msg)


def load(map, Savename):
    map.name = Savename
    whichos = platform.system()
    if whichos == 'Linux':
        direct = '/saves/'
    elif whichos == 'Windows':
        direct = '\\saves\\'
    else:
        print('You are running on an unrecognized Operating System!\n' + whichos)
        direct = '/saves/'
    f = open(os.getcwd() + direct + Savename, 'r')
    lines = f.readlines()
    map.tiles = list()
    for line in lines:
        row = list()
        for char in line:
            if char == 'e':
                row.append(None)
            elif char == 'l':
                row.append('light')
            elif char == 'd':
                row.append('dark')
            elif char == 'g':
                row.append('goal')
            elif char == 's':
                row.append('start')
            elif char == '#':
                temp = ''
                coords = list()
                for l in line:
                    if l in '#;':
                        continue
                    elif l == ',':
                        coords.append(int(temp))
                        temp = ''
                    else:
                        temp += l
                coords.append(int(temp))
                map.player_x = coords[0]
                map.player_y = coords[1]
                break
            elif char == 'L':
                temp = ''
                x = int
                moves = list()
                for l in line:
                    if l == 'L':
                        continue
                    elif l == ',':
                        x = int(temp)
                        temp = ''
                    elif l == ';':
                        moves.append((x, int(temp)))
                        temp = ''
                        x = int
                    else:
                        temp += l
                map.dots.append(Dots.LineDot(map, moves))
        map.tiles.append(row)
    map.players = list()
    map.players.append(Player.Player(map))
    map.buttons = list(filter(lambda x: not isinstance(x, FileButton), map.buttons))
    for j in range(len(map.tiles)):
        for i in range(len(map.tiles[j])):
            if map.tiles[j][i] is not None:
                if j > 0:
                    if map.tiles[j - 1][i] is None:
                        map.lines_x.append(((i * 52, (i + 1) * 52), j * 52))
                if j < (map.height - 1):
                    if map.tiles[j + 1][i] is None:
                        map.lines_x.append(((i * 52, (i + 1) * 52), (j + 1) * 52))
                if i > 0:
                    if map.tiles[j][i - 1] is None:
                        map.lines_y.append((i * 52, (j * 52, (j + 1) * 52)))
                if i < (map.width - 1):
                    if map.tiles[j][i + 1] is None:
                        map.lines_y.append(((i + 1) * 52, (j * 52, (j + 1) * 52)))

    while merge_lines(map):
        pass

    for j in range(len(map.tiles)):
        for i in range(len(map.tiles[j])):
            if map.tiles[j][i] == 'goal':
                map.goals.append((i, j))


def merge_lines(map):
    for line in map.lines_x:
        for line2 in map.lines_x:
            if line[0][1] == line2[0][0] and line[1] == line2[1]:
                newline = ((line[0][0], line2[0][1]), line[1])
                newlines = list()
                newlines.append(newline)
                for _ in map.lines_x:
                    if _ not in (line, line2):
                        newlines.append(_)
                map.lines_x = newlines
                return True
    for line in map.lines_y:
        for line2 in map.lines_y:
            if line[1][1] == line2[1][0] and line[0] == line2[0]:
                newline = (line[0], (line[1][0], line2[1][1]))
                newlines = list()
                newlines.append(newline)
                for _ in map.lines_y:
                    if _ not in (line, line2):
                        newlines.append(_)
                map.lines_y = newlines
                return True
    return False
