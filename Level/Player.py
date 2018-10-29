# -*- coding: UTF-8 -*-

import pygame
import datetime
import numpy


class Player(object):

    def __init__(self, map):
        self.count_moves = 0
        self.time = list()
        self.finish_time = list()
        self.time_in_seconds = int
        self.map = map
        self.x = map.player_x
        self.y = map.player_y
        self.speed = 4
        self.rect = pygame.rect.Rect(6, 58, 38, 38)
        self.goal_reached = False

    def move_up(self):
        self.y -= self.speed
        for line in self.map.lines_x:
            if line[1] <= self.y + self.speed:
                if self.y <= line[1] and self.x <= line[0][1] and self.x+38 > line[0][0]:
                    self.y = line[1]+2
        self.check_goal()

    def move_down(self):
        self.y += self.speed
        for line in self.map.lines_x:
            if line[1] >= self.y+38 - self.speed:
                if self.y+38 >= line[1] and self.x <= line[0][1] and self.x+38 > line[0][0]:
                    self.y = line[1]-38
        self.check_goal()

    def move_right(self):
        self.x += self.speed
        for line in self.map.lines_y:
            if line[0] >= self.x+38 - self.speed:
                if self.x+38 >= line[0] and self.y <= line[1][1] and self.y+38 > line[1][0]:
                    self.x = line[0]-38
        self.check_goal()

    def move_left(self):
        self.x -= self.speed
        for line in self.map.lines_y:
            if line[0] <= self.x + self.speed:
                if self.x <= line[0] and self.y <= line[1][1] and self.y+38 > line[1][0]:
                    self.x = line[0]+2
        self.check_goal()

    def check_goal(self):
        for goal in self.map.goals:
            if (goal[0]*52-38 < self.x < (goal[0]+1)*52)  and (goal[1]*52-38 < self.y < (goal[1]+1)*52):
                self.get_time()
                sec = self.time[0]*24
                sec = (sec + self.time[1])*60
                sec = (sec + self.time[2]) * 60
                sec += self.time[3]
                sec += self.time[4]/1000000
                self.time_in_seconds = sec
                if not self.map.is_bot:
                    self.map.done(self.time)
                else:
                    self.goal_reached = True
                return
        if self.map.is_bot:
            self.count_moves += 1
            self.fitness_func()

    def fail(self):
        if not self.map.is_bot:
            self.map.fail()
        else:
            self.failed = True
            self.map.players = list(filter(lambda x: x != self, self.map.players))

    def get_time(self):
        now = str(datetime.datetime.now())
        self.finish_time = list(
            map(lambda x: int(x), (now[:4], now[5:7], now[8:10], now[11:13], now[14:16], now[17:19], now[20:26])))
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

    def __str__(self):
        string = ''
        string += 'player number %d\n' % self.map.bot.players.index(self)
        return string


class PlayerOld(Player):

    def __init__(self, map):
        Player.__init__(self, map)
        self.visible = False
        self.fitness = 0
        self.failed = False
        self.moves = list()
        self.goal_reached = False
        self.visited = list()
        self.new_fields = 0
        self.move_at_last_new = 0
        self.highest_point = 0

    def fitness_func(self):
        if not ((self.x + 1) // 52, (self.y + 1) // 52) in self.visited:
            self.new_fields += 1
            self.visited.append(((self.x + 1) // 52, (self.y + 1) // 52))
            self.move_at_last_new = self.count_moves
        if not ((self.x + 37) // 52, (self.y + 1) // 52) in self.visited:
            self.new_fields += 1
            self.visited.append(((self.x + 37) // 52, (self.y + 1) // 52))
            self.move_at_last_new = self.count_moves
        if not ((self.x + 1) // 52, (self.y + 37) // 52) in self.visited:
            self.new_fields += 1
            self.visited.append(((self.x + 1) // 52, (self.y + 37) // 52))
            self.move_at_last_new = self.count_moves
        if not ((self.x + 37) // 52, (self.y + 37) // 52) in self.visited:
            self.new_fields += 1
            self.visited.append(((self.x + 37) // 52, (self.y + 37) // 52))
            self.move_at_last_new = self.count_moves


class PlayerNew(Player):

    def __init__(self, map):
        Player.__init__(self, map)
        self.move_at_last_new = 0
        self.visible = False
        self.fitness = 0
        self.failed = False
        self.moves = list()
        self.progress = 0
        self.closest_line = None
        self.closest_dist = None
        closest = None
        for line in self.map.shortest_lines:
            coll = self.line_collision((self.x, self.y), line)
            if coll:
                dist = numpy.ma.sqrt((coll[0]-self.x)**2+(coll[1]-self.y)**2)
                if closest is None or closest > dist:
                    closest = dist
                    self.closest_line = line
        if self.closest_line is None:
            for line in self.map.shortest_lines:
                dist = numpy.ma.sqrt((line.start[0]-self.x)**2+(line.start[1]-self.y)**2)
                if self.closest_dist is None or self.closest_dist > dist:
                    self.closest_line = line
                    self.closest_dist = dist
            """last_line = self.map.shortest_lines[::-1][:1]
            dist = numpy.ma.sqrt((last_line.end[0]-self.x)**2+(last_line.end[1]-self.y)**2)
            if closest > dist:
                self.closest_line = last_line
                self.closest_dist = dist"""

    def fitness_func(self):
        coll = self.line_collision((self.x, self.y), self.closest_line)

        ind = self.map.shortest_lines.index(self.closest_line)

        if ind != len(self.map.shortest_lines)-1:
            next_line = self.map.shortest_lines[ind + 1]
        else:
            next_line = None

        if ind != 0:
            line_before = self.map.shortest_lines[ind - 1]
        else:
            line_before = None

        if self.map.players.index(self) == 15 and self.count_moves == self.map.bot.move_count-5:
            print('Closest line:', self.closest_line)
            print('Line before:', line_before)
        # Die Linie danach und die davor

        if coll:
            pythagoras = numpy.ma.sqrt((coll[0]-self.closest_line.start[0])**2 +
                                       (coll[1]-self.closest_line.start[1]))
            self_path = self.closest_line.path + pythagoras

            self.closest_dist = None
            # Sollte eine Kollision vorhanden sein, setze ich self.closest_dist auf None da diese Variable ein
            # Indikator dafür ist ob ich die letzte Kollision mit einem Punkt oder einer Line war

        else:

            # Sollte ich keine Kollision mit der aktuellen besten Linie errechnen, ist
            # der player schon bei der nächsten oder bei der letzten Linie oder dazwischen

            closest = None

            for line in (next_line, line_before):

                if line is not None:

                    # Ich prüfe sowohl die Linie davor als auch die Linie danach

                    coll = self.line_collision((self.x, self.y), line)
                    if coll:
                        pythagoras = numpy.ma.sqrt((coll[0] - line.start[0]) ** 2 +
                                                   (coll[1] - line.start[1]))

                        if closest is None or closest > pythagoras:
                            closest = pythagoras
                            self_path = line.path + pythagoras
                            self.closest_dist = None

                        break
            if closest is None:

                # Wenn es mit keiner Linie eine Kollision gab

                self.closest_dist = None

                for line in self.map.shortest_lines:
                    dist = numpy.ma.sqrt((line.start[0] - self.x) ** 2 + (line.start[1] - self.y) ** 2)
                    if self.closest_dist is None or self.closest_dist > dist:
                        self.closest_line = line
                        self.closest_dist = dist
                        self_path = self.closest_line.path
        """all_length = 0
        for line in self.map.shortest_lines:
            all_length += line.length
            coll = self.line_collision((self.x, self.y), line)
            if coll:
                dist = abs(coll[0] - self.x) + abs(coll[1] - self.y)
                # Viel schneller als den Satz den Pytagoras zu nutzen (Wurzeln ziehen dauert ewig), aber ungenauer...

                # dist = numpy.ma.sqrt((coll[0]-self.x)**2+(coll[1]-self.y)**2)
                # Ich probiere es trotzdme mal..
                if closest is None or closest < dist:
                    closest = dist
                    self.closest_line = line
                    closest_coll = coll"""

        last_line = self.map.shortest_lines[::-1][0]

        all_length = last_line.path + last_line.length

        if self.closest_dist is not None:
            all_length += self.closest_dist
            # So wird der progress niedriger je weiter der palyer sich von dem nächsten Eckpunkt entfernt
            # Denn sobald er sehr nah dran ist, ist die Wahrscheinlichkeit relativ hoch die nächste Linie zu erreichen

        progress = self_path / all_length
        if self.progress < progress:
            self.progress = progress
            self.move_at_last_new = self.count_moves

        fitness = progress * 10
        # Vielleicht verändere ich die fitness noch weiter, außerdem ist es übersichtlicher

        return fitness

    def line_collision(self, start, line):

        # Das ist eine Abwandlung der Level.Button.test_line_collision funktion

        stuetz1 = numpy.array(start)
        # Der stützvektor ist die Position des Players

        if line.m is None:
            if line.end[1] < start[1] < line.start[1] or line.start[1] < start[1] < line.end[1]:
                return line.start[0], start[1]
            else:
                return False
        elif line.m == 0:
            if line.end[0] < start[0] < line.start[0] or line.start[0] < start[0] < line.end[0]:
                return start[0], line.start[1]
            else:
                return False
        streck1 = numpy.array((1, -1/line.m))
        # Der Streckvektor ist eine Senkrechte zu der zu vergleichenden Linie,
        # die durch den Player führt

        # Wir vergleichen diesmal nur mit einer einzigen Linie
        stuetz2 = numpy.array((line.start[0], line.start[1]))
        streck2 = numpy.array((line.end[0], line.end[1])) - stuetz2
        # Wieder vektoren deklarieren

        # Die Linien schneiden sich sicher. Jegliche Kontrolle wäre sinnlos

        # Vorhin haben wir ja die Vektoren deklariert...
        # Damit haben wir: stuetz1 + r * streck1 = stuetz2 + s * streck2
        # --> stuetz1 - stuetz2 = s * streck2 + r * (-streck1)
        # Damit kommen wir auf ein lineares Gleichungssystem, das wir mit NumPy lösen können:

        # In den Kombinationen werden die Vektoren manuell zu neuen zusammengefügt, mit denen dann gerechnet werden kann
        kombi_1 = numpy.array((streck2[0], -streck1[0]))
        kombi_2 = numpy.array((streck2[1], -streck1[1]))

        res = numpy.linalg.solve((kombi_1, kombi_2), (stuetz1 - stuetz2))

        # Da meine Streckvektoren immer die gesamte Strecke sind, kann der Punkt nur auf der Strecke liegen wenn die
        # Multiplikatoren zwischen 0 und 1 liegen.
        if not (0 <= res[0] <= 1):
            return False

        # s1 und s2 müssten gleich sein, ich kontrolliere jedoch anfangs sicherheitshalber mit
        # (Wenn sie dies lesen können hab ich vergessen es zu löschen :D)
        s1 = list(map(lambda x: round(x, 10), list(res[0] * streck2 + stuetz2)))
        s2 = list(map(lambda x: round(x, 10), list(res[1] * streck1 + stuetz1)))
        if s1 == s2:
            return s1
        else:
            # Sollten s1 und s2 jedoch nicht gleich sein, interessiert mich brennend warum und ich raise einen Error

            print('''start: %s
                  line: %s
                  s1: %s
                  s2: %s''' % (start, line, s1, s2))
            raise ValueError('Wenn sie diesen Error sehen hab ich (Oder das Sturmtief Fabienne) die Matrix kaputt'
                             'gemacht, denn dieser Error kann eigentlich gar nicht auftreten.')
        raise IndexError('There are no Lines in that map! Dude, WTF?')

    def __str__(self):
        string = super().__str__()
        string += '%d moves\n' % len(self.moves)
        string += 'moves: %s\n' % self.moves
        string += 'move number %d' % self.count_moves
        return string
