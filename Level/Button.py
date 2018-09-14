# -*- coding: UTF-8 -*-

import pygame
import os
import platform
import re
import GeneticAlgorithm
from Level import Player, Dots


class Button(object):

    def __init__(self, msg, x, y, w, h, bw, tsize):
        self.msg = msg
        self.capt = self.msg
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
        self.captext = self.font.render(self.msg, False, (0, 0, 0))

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.bw, self.y + self.bw, self.w - self.bw * 2, self.h - self.bw * 2))
        screen.blit(self.captext, (self.w / 2 + self.x - 14 * len(self.capt) / 2, self.h / 2 + self.y - self.tsize / 2 - 5))


class LoadButton(Button):

    def __init__(self):
        Button.__init__(self, 'Load', 30, 30, 150, 75, 10, 30)
        self.clicked = False

    def click(self, map):
        self.clicked = True
        file_path = os.path.dirname(os.path.realpath(__file__))
        whichos = platform.system()
        if whichos == 'Linux':
            direct = '/saves'
        elif whichos == 'Windows':
            direct = '\\saves'
        else:
            print('You are running on an unrecognized Operating System!\n' + whichos)
            direct = '/saves'
        files = os.listdir(file_path + direct)
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
        restart(map)


class FileButton(Button):

    def __init__(self, msg, x, y):
        Button.__init__(self, msg, x, y, 145, 40, 2, 25)

    def text(self):
        self.font = pygame.font.SysFont('Arial', self.tsize)
        self.capt = re.sub('\.txt', '', self.msg)
        self.captext = self.font.render(self.capt, False, (0, 0, 0))

    def click(self, map):
        load(map, self.msg)

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.bw, self.y + self.bw, self.w - self.bw * 2, self.h - self.bw * 2))
        screen.blit(self.captext, (self.w / 2 + self.x - 11 * len(self.capt) / 2, self.h / 2 + self.y - self.tsize / 2 - 2))


class AlgoButton(Button):

    def __init__(self):
        Button.__init__(self, 'Start Algorithm', 333, 30, 280, 75, 10, 30)
        self.clicked = False

    def click(self, map):
        if map.name == '':
            map.texts.append(('You have to load a map first!', 300, 350))
        else:
            self.clicked = True
            x = self.x
            y = self.y + self.h + 2
            map.buttons.append(GenButton(x, y))

    def unclick(self, map):
        map.buttons = list(filter(lambda x: not isinstance(x, GenButton), map.buttons))
        self.clicked = False


class GenButton(Button):

    def __init__(self, x, y):
        Button.__init__(self, 'Genetic', x, y, 125, 40, 5, 25)

    def text(self):
        self.font = pygame.font.SysFont('Arial', self.tsize)
        self.capt = re.sub('\.txt', '', self.msg)
        self.captext = self.font.render(self.capt, False, (0, 0, 0))

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.bw, self.y + self.bw, self.w - self.bw * 2, self.h - self.bw * 2))
        screen.blit(self.captext, (self.w / 2 + self.x - 11 * len(self.capt) / 2, self.h / 2 + self.y - self.tsize / 2 - 2))

    def click(self, map):
        map.buttons.append(VisibleButton())
        map.is_bot = True
        map.get_time()
        restart(map, map.name)
        map.bot = GeneticAlgorithm.GenAI(map)


class VisibleButton(Button):

    def __init__(self):
        Button.__init__(self, 'See best', 700, 30, 200, 75, 10, 30)
        self.active = False

    def click(self, map):
        if self.active:
            self.capt = 'See best'
            self.msg = 'See best'
        else:
            self.capt = 'See all'
            self.msg = 'See all'
        self.text()
        map.see_all = not map.see_all
        self.active = not self.active


def restart(map, name=''):
    if name == '':
        name = map.name
    map.name = ''
    map.goal_reached = False
    map.goals = list()
    map.lines_x = list()
    map.lines_y = list()
    map.tiles = list()
    map.dots = list()
    load(map, name)
    map.buttons = list(filter(lambda x: not isinstance(x, RestartButton), map.buttons))
    map.texts = list(filter(lambda x: not x[0] == 'Geschafft!', map.texts))


def load(map, Savename):
    if map.name != '':
        restart(map, name=Savename)
        return
    file_path = os.path.dirname(os.path.realpath(__file__))
    map.texts = list()
    map.name = Savename
    whichos = platform.system()
    if whichos == 'Linux':
        direct = '/saves/'
    elif whichos == 'Windows':
        direct = '\\saves\\'
    else:
        print('You are running on an unrecognized Operating System!\n' + whichos)
        direct = '/saves/'
    f = open(file_path + direct + Savename, 'r')
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
                        coords.append(int(temp)*52-19-26)
                        temp = ''
                    else:
                        temp += l
                coords.append(int(temp)*52-26-19)
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
                        x = int(temp)*52-26-8
                        temp = ''
                    elif l == ';':
                        moves.append((x, int(temp)*52-26-8))
                        temp = ''
                        x = int
                    else:
                        temp += l
                map.dots.append(Dots.LineDot(map, moves))
        map.tiles.append(row)
    map.players = list()
    if not map.is_bot:
        map.players.append(Player.Player(map))
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

    merge_lines(map)

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
                merge_lines(map)
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
                merge_lines(map)
