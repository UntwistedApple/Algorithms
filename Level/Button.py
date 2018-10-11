# -*- coding: UTF-8 -*-

from Level import Player, Dots, Line
import pygame
import numpy
import os
import platform
import re
import GeneticAlgorithm


numpy.seterr(divide='raise', invalid='raise')


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
        files = os.listdir(file_path + direct)[::-1]
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
            map.buttons.append(GenButton())

    def unclick(self, map):
        map.buttons = list(filter(lambda x: not isinstance(x, GenButton), map.buttons))
        self.clicked = False


class fitnessbutton(Button):

    def __init__(self):
        pass            # TODO!


class GenButton(Button):

    def __init__(self):
        Button.__init__(self, 'Genetic', 333, 107, 150, 40, 5, 25)

    def text(self):
        self.font = pygame.font.SysFont('Arial', self.tsize)
        self.capt = re.sub('\.txt', '', self.msg)
        self.captext = self.font.render(self.capt, False, (0, 0, 0))

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.bw, self.y + self.bw, self.w - self.bw * 2, self.h - self.bw * 2))
        screen.blit(self.captext, (self.w / 2 + self.x - 12 * len(self.capt) / 2, self.h / 2 + self.y - self.tsize / 2 - 2))

    def click(self, map):
        self.clicked = True
        map.buttons.append(GenButton_1())
        map.buttons.append(GenButton_2())
        map.buttons.append(GenButton_3())

    def fitness_buttons(self, map):
        pass            # TODO!

    def unclick(self, map):
        self.clicked = False
        map.buttons = list(filter(lambda x: not isinstance(x, (GenButton_1, GenButton_2, GenButton_3)), map.buttons))


class GenButton_1(GenButton):

    def __init__(self):
        GenButton.__init__(self)
        self.x = 333
        self.y = 149
        self.msg = 'Genetic V1'
        self.text()

    def click(self, map):
        map.buttons.append(VisibleButton())
        map.is_bot = True
        map.get_time()
        restart(map, map.name)
        map.bot = GeneticAlgorithm.GenAI(map)


class GenButton_2(GenButton):

    def __init__(self):
        GenButton.__init__(self)
        self.x = 333
        self.y = 191
        self.msg = 'Genetic V2'
        self.text()

    def click(self, map):
        map.buttons.append(VisibleButton())
        map.is_bot = True
        map.get_time()
        restart(map, map.name)
        map.bot = GeneticAlgorithm.GenAI_2(map)


class GenButton_3(GenButton):

    def __init__(self):
        GenButton.__init__(self)
        self.x = 333
        self.y = 233
        self.msg = 'Genetic V3'
        self.text()

    def click(self, map):
        map.buttons.append(VisibleButton())
        map.is_bot = True
        map.get_time()
        restart(map, map.name)
        map.bot = GeneticAlgorithm.GenAI_3(map)


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
    map.collisions, map.worked, map.way = (list(), list(), list())
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
                        map.coords.append((int(temp) - 1) * 52 + 1)
                        coords.append(int(temp) * 52 - 19 - 26)
                        temp = ''
                    else:
                        temp += l
                map.coords.append((int(temp) - 1) * 52 + 1)
                coords.append(int(temp) * 52 - 26 - 19)
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

    # Da ich gleich bestimmte Ecken benötige, muss ich sie erst suchen
    find_ideal_line(map)
    for line in map.shortest_lines:
        line.path = 0
        for line2 in map.shortest_lines[:map.shortest_lines.index(line)]:
            line.path += line2.length


def find_corners(game_map):
    # Wir suchen nach Ecken die "spitz" in die Karte hineinzeigen, also Ecken um die herum nur ein leeres tile ist
    corners = list()

    # Hier sammle ich alle Enden von allen Linien zusammen
    for line in unify_lines(game_map.lines_x, game_map.lines_y):
        #  Allerdings keine doppelt
        if line[0] not in corners:
            corners.append(line[0])
        if line[1] not in corners:
            corners.append(line[1])
    # Hier werden die Ecken aussortiert, bei denen die is_right_corner Funktion ein False zurückgibt
    corners = list(filter(lambda x: is_right_corner(game_map, (int(x[0] / 52), int(x[1] / 52))), corners))

    corner_objects = list()
    for corner in corners:
        corner_objects.append(Line.Corner(corner[0], corner[1]))
    return corner_objects


def is_right_corner(map, coords):
    # Wir suchen nach Ecken die genau ein None-tile um sich herum haben
    nones = 0

    # Die Koordinaten einer Ecke sind die gleichen wie die des Feldes rechts-unten davon. Ich fange aber links oben an
    # zu suchen, also x-1 und y-1
    x = coords[0]-1
    y = coords[1]-1
    # Die beisen for-loops sorgen dafür dass jedes Nachbartile der Ecke überprüft wird
    for i in range(2):
        for j in range(2):
            if map.tiles[y+j][x+i] is None:
                # Für jedes NoneType-tile wird der counter um 1 erhöht
                nones += 1
    # steht der counter am ende auf 1 wird True zurückgegeben, ansonsten False
    return nones == 1


glo_map = None


def find_ideal_line(map):
    global glo_map
    glo_map = map
    # Das Ziel ist ein zufälliges goal-type tile
    stop = False
    for j in range(len(map.tiles)):
        if stop: break
        for i in range(len(map.tiles[j])):
            if stop: break
            if map.tiles[j][i] == 'goal':
                target = (i*52, j*52)
                stop = True

    lines = unify_lines(map.lines_x, map.lines_y)

    # Wenn ein direkter Weg vom Start zum Ziel möglich ist, ist der natürlich der Schnellste
    #if test_line_collision((map.player_x, map.player_y), (target[0], target[1]), lines):
    #    return (map.player_x, map.player_y), (target[0], target[1])
    find_way_over_corners((map.coords[0], map.coords[1]), lines, target, find_corners(map), list())
    map.shortest_lines = shortest_lines
    for line in shortest_lines:
        stuetz = numpy.array(line.start)
        streck = numpy.array(line.end) - stuetz
        ind = numpy.ma.sqrt(streck[0]**2+streck[1]**2) / 25
        x, y = stuetz
        for i in range(int(ind)+1):
            map.way.append((x, y))
            x += streck[0]/ind
            y += streck[1]/ind


shortest_way = None
shortest_lines = list()


def find_way_over_corners(start, lines, target, corners, my_lines):
    global shortest_way, shortest_lines, glo_map
    if test_line_collision(start, target, lines):
        for corner in corners:
            collision = test_line_collision(start, corner.coords, lines)
            if not collision:
                glo_map.worked.append(corner.coords)
                line = Line.Line(start, corner.coords)
                already_used = sum(map(lambda x: x.length, my_lines))
                needed = already_used + line.length
                if corner.reached_minimum is not None:
                    if needed < corner.reached_minimum:
                        corner.reached_minimum = needed
                        print(list(map(lambda x: x.length, my_lines + [line])))
                        find_way_over_corners(corner.coords, lines, target, corners, my_lines + [line])
                else:
                    corner.reached_minimum = needed
                    find_way_over_corners(corner.coords, lines, target, corners, my_lines + [line])
    else:
        line = Line.Line(start, target)
        if shortest_way is None:
            shortest_way = sum(map(lambda x: x.length, my_lines+[line]))
            shortest_lines = my_lines+[line]
        else:
            my_way = sum(map(lambda x: x.length, my_lines+[line]))
            if my_way < shortest_way:
                shortest_way = my_way
                shortest_lines = my_lines+[line]


def unify_lines(lines_x, lines_y):
    # Einfach eine Funktion um alle x- und y-Linien in eine universelle Form zu schreiben
    lines = list()
    for line in lines_x + lines_y:
        try:
            lines.append(((line[0][0], line[1]), (line[0][1], line[1])))
        except TypeError:
            lines.append(((line[0], line[1][0]), (line[0], line[1][1])))
    return lines


def test_line_collision(start, end, lines):
    global glo_map

    # Lösen mit einem linearen Gleichungssystem
    # Ich arbeite mit NumPy arrays weil diese Addition und Subtraktion erlauben

    stuetz1 = numpy.array(start)
    # Der stützvektor ist der Startpunkt der Geraden

    streck1 = numpy.array(numpy.array(end)-numpy.array(start))
    # Der Streckvektor ist der Vektor vom Start zum Ziel

    # Wir schauen nach Kollisionen mit jeder einzigen Linie..
    for line in lines:
        stuetz2 = numpy.array((line[0][0], line[0][1]))
        streck2 = numpy.array((line[1][0], line[1][1])) - stuetz2
        # Wieder vektoren deklarieren

        # Hier kontrolliere ich, ob die Steigungen gleich und die Strecken damit parallel sind oder aufeinender liegen
        # Was von beidem sie tun ist unwichtig, ich zähle keines von beidem als Kollision
        try:
            f = streck1[0]/streck2[0]
        except FloatingPointError:
            # Da ich nicht durch 0 teilen kann muss ich diesen Teil hardcoded, also "manuell" kontrollieren
            if streck1[1] == streck2[1]:
                continue
            else:
                f = False
        try:
            ff = streck1[1]/streck2[1]
        except FloatingPointError:
            if streck1[1] == streck2[1]:
                continue
            else:
                ff = None

        # Sind die Quotienten (Oder faktoren, deshalb f und ff) gleich, sind auch die Steigungen gleich.
        if ff == f:
            continue

        # Vorhin haben wir ja die Vektoren deklariert...
        # Damit haben wir: stuetz1 + r * streck1 = stuetz2 + s * streck2
        # --> stuetz1 - stuetz2 = s * streck2 - r * (-streck1)
        # Damit kommen wir auf ein lineares Gleichungssystem, das wir mit NumPy lösen können:

        # Sollte entweder der x- oder der y- Wert der beiden Streckvektoren gleich sein, sind sie zwangsweise parallel
        # und das zähle ich ja nicht unter schneiden.
        if streck2[0] == streck1[0] or streck2[1] == streck1[1]:
            continue

        # In den Kombinationen werden die Vektoren manuell zu neuen zusammengefügt, mit denen dann gerechnet werden kann
        kombi_1 = numpy.array((streck2[0], -streck1[0]))
        kombi_2 = numpy.array((streck2[1], -streck1[1]))

        res = numpy.linalg.solve((kombi_1, kombi_2), (stuetz1-stuetz2))

        # Da meine Streckvektoren immer die gesamte Strecke sind, kann der Punkt nur auf der Strecke liegen wenn die
        # Multiplikatoren zwischen 0 und 1 liegen.
        con = False
        for _ in res:
            if not(0 <= _ <= 1):
                con = True
        if con:
            continue

        # s1 und s2 müssen gleich sein, ich kontrolliere jedoch anfangs sicherheitshalber mit
        # (Wenn sie dies lesen können hab ich vergessen es zu löschen :D)
        s1 = list(map(lambda x: round(x, 10), list(res[0] * streck2 + stuetz2)))
        s2 = list(map(lambda x: round(x, 10), list(res[1] * streck1 + stuetz1)))
        if s1 == s2:
            if not (int(s1[0]), int(s1[1])) in (end, start):
                try:
                    #glo_map.collisions.append(s1)
                    pass
                except:
                    pass
                return s1
            else:
                continue
        else:
            # Sollten s1 und s2 jedoch nicht gleich sein, interessiert mich brennend warum und ich raise einen Error
            raise ValueError
            return False
    return False


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
