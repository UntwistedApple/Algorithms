# -*- coding: UTF-8 -*-

import pygame
from Level import Tileset, Button, Player
import datetime
import GeneticAlgorithm
import config as cnf

config = cnf.read()


# Die Tilemap Klasse verwaltet die Tile-Daten, die das Aussehen der Karte beschreiben


class Tilemap(object):

    def __init__(self):
        # neues Tileset
        self.tileset = Tileset.Tileset('template.png', (255, 0, 255), 52, 52)
        self.tileset.add_tile('dark', 0, 0)
        self.tileset.add_tile('light', 52, 0)
        self.tileset.add_tile('start', 104, 0)
        self.tileset.add_tile('goal', 104, 0)
        self.tileset.add_tile('player', 0, 52)
        self.max_fps = config['max_fps_when_playing']
        self.player_x = -200  # TODO: Den ganzen Blödsinn hier in n dictionary umschreiben?
        self.player_y = -200
        self.goals = list()
        self.name = ''
        self.see_all = True
        self.is_bot = False
        self.goal_reached = False
        self.in_constants = False
        self.texts = list()
        self.done_text = None
        self.help_text = None
        self.font = pygame.font.SysFont('Arial', 40)  # Comic Sans MS
        self.started = False
        self.time = list()
        self.bot = None
        self.new_fitness = True
        self.shortest_lines = list()
        self.coords = list()
        self.which_move = 0

        self.lines_x = list()
        self.lines_y = list()
        self.ideal_line = list()
        self.worked = list()
        self.way = list()

        # Mapsize in Tiles
        self.width = 22
        self.height = 16

        # Leere Liste der Tiles
        self.tiles = list()

        self.dots = list()

        for i in range(0, self.height):
            self.tiles.append(list())
            for j in range(0, self.width):
                self.tiles[i].append('empty')

        self.buttons = list()
        self.buttons.append(Button.LoadButton())
        self.buttons.append(Button.AlgoButton())

        self.players = list()
        self.players.append(Player.Player(self))


    # Hier rendern wir den sichtbaren Teil der Karte.

    def render(self, screen):
        if self.is_bot:
            self.max_fps = config['max_fps_bot']
        else:
            self.max_fps = config['max_fps_when_playing']
        # Zeilenweise durch die Tiles durchgehen.
        for y in range(0, int(screen.get_height() / self.tileset.tile_height) + 1):
            if y >= self.height or y < 0:
                continue
            # Die aktuelle Zeile zum einfacheren Zugriff speichern.
            line = self.tiles[y]
            # Und jetzt spaltenweise die Tiles rendern.
            for x in range(0, int(screen.get_width() / self.tileset.tile_width) + 1):
                if x >= self.width or x < 0:
                    continue
                # Wir versuchen, die Daten des Tiles zu bekommen.
                tilename = line[x]
                tile = self.tileset.get_tile(tilename)
                # Falls das nicht fehlschlägt können wir das Tile auf die screen-Surface blitten.
                if tile is not None:
                    screen.blit(self.tileset.image, (x * self.tileset.tile_width, y * self.tileset.tile_height), tile.rect)
        for line in self.lines_x:
            pygame.draw.rect(screen, (0, 0, 0), (line[0][0]+2, line[1], line[0][1]-line[0][0]-2, 2))
        for line in self.lines_y:
            pygame.draw.rect(screen, (0, 0, 0), (line[0], line[1][0], 2, line[1][1]-line[1][0]+2))
        #for collision in self.collisions:
        #    pygame.draw.rect(screen, (200, 0, 0), (collision[0]-1, collision[1]-1, 4, 4))
        #for worked in self.worked:
        #    pygame.draw.rect(screen, (0, 200, 0), (worked[0] - 1, worked[1] - 1, 4, 4))
        #for bread in self.way:
        #    pygame.draw.rect(screen, (0, 0, 200), (bread[0] - 1, bread[1] - 1, 3, 3))
        if self.is_bot:
            if self.players[0].count_moves < len(self.bot.constant_moves):
                self.in_constants = True
            else:
                self.in_constants = False
        for player in self.players:
            if self.see_all and not self.in_constants or player.visible:
                screen.blit(self.tileset.image, (player.x, player.y), player.rect)
        for dot in self.dots:
            dot.render(screen)
        if not self.in_constants:
            for player in self.players:
                for dot in self.dots:
                    if dot.x-38 < player.x < dot.x+15 and dot.y-38 < player.y < dot.y+15:
                        player.fail()
        if self.help_text is not None:
            text = pygame.font.SysFont('Arial', 20).render(self.help_text[0], False, (0, 0, 0))
            screen.blit(text, (self.help_text[1], self.help_text[2]))
        if self.done_text is not None and self.done_text not in self.texts:
            self.texts.append(self.done_text)
        for string in self.texts:
            text = self.font.render(string[0], False, (0, 0, 0))
            screen.blit(text, (string[1], string[2]))
        if isinstance(self.bot, GeneticAlgorithm.GenAI_2):
            text = pygame.font.SysFont('Arial', 40).render('%d / %d'
                                                           % (self.bot.generation, self.bot.generations_per_change),
                                                           False, (0, 0, 0))
            screen.blit(text, (20, 130))
            text = pygame.font.SysFont('Arial', 40).render('%d / %d'
                                                           % (self.which_move, self.bot.moves_per_change),
                                                           False, (0, 0, 0))
            screen.blit(text, (20, 165))
            text = pygame.font.SysFont('Arial', 40).render(str(self.bot.generation // self.bot.generations_per_change),
                                                           False, (0, 0, 0))
            screen.blit(text, (20, 200))
        elif isinstance(self.bot, GeneticAlgorithm.GenAI):
            text = pygame.font.SysFont('Arial', 40).render(str(self.bot.generation), False, (0, 0, 0))
            screen.blit(text, (20, 130))
            text = pygame.font.SysFont('Arial', 40).render(str(self.which_move), False, (0, 0, 0))
            screen.blit(text, (20, 165))
        for button in self.buttons:
            button.render(screen)
    # Tastendrücke verarbeiten:

    def handle_input(self, key):
        if not self.is_bot and not self.goal_reached:
            if not self.started and self.name != '':
                self.get_time()
            player = self.players[0]
            if key == pygame.K_LEFT:
                player.move_left()
            elif key == pygame.K_RIGHT:
                player.move_right()
            elif key == pygame.K_UP:
                player.move_up()
            elif key == pygame.K_DOWN:
                player.move_down()

    def get_time(self):
        self.started = True
        now = str(datetime.datetime.now())
        self.time = list(
            map(lambda x: int(x), (now[:4], now[5:7], now[8:10], now[11:13], now[14:16], now[17:19], now[20:26])))

    def clicked(self):
        pos = pygame.mouse.get_pos()
        whathit = None
        for button in self.buttons:
            if button.x < pos[0] < button.x + button.w and button.y < pos[1] < button.y + button.h:
                whathit = type(button)
                if not button.clicked:
                    button.click(self)
                else:
                    button.unclick(self)

        for button in self.buttons:
            # Jeder Button

            if button.clicked and whathit is not None:
                # Der geklickt ist, falls auf etwas geklickt wurde

                if not isinstance(button, whathit): #whathit != type(button)
                    # Auf den aber nicht selbst geklickt wurde

                    if whathit in (Button.GenButton_1, Button.GenButton_2, Button.GenButton_3):
                        if type(button) not in (Button.GenButton, Button.AlgoButton):
                            button.unclick(self)

                    elif whathit == Button.GenButton:
                        if not isinstance(button, Button.AlgoButton):
                            button.unclick(self)

                    else:
                        button.unclick(self)
            elif button.clicked:
                button.unclick(self)

    def fail(self):
        self.texts.append(('Aww you failed :(', 375, 150))
        self.buttons.append(Button.RestartButton())
        self.goal_reached = True

    def done(self, time):
        text = '%d days and '
        text += '%d:%d:%d:%d' % (time[1], time[2], time[3], time[4])
        self.texts.append(('You won! Your Time: '+text, 225, 150))
        self.buttons.append(Button.RestartButton())
        self.goal_reached = True
        self.started = False

    def move(self):
        self.which_move += 1
        if not self.is_bot:
            return
        if len(self.players) == 0:
            self.finished()
        if self.which_move >= self.bot.move_count:
            self.finished()
            return
        for player in self.players:
            try:
                move = player.moves[player.count_moves]
            except IndexError:
                msg = '\nError occured\nMove number %s\n%s\nPlayer 0:\n%s\nPlayer 67:\n%s\n' % (
                    self.which_move, player, self.players[0], self.players[67])
                print(msg)
                raise
            if move == 0:
                player.move_up()
            elif move == 1:
                player.move_right()
            elif move == 2:
                player.move_down()
            else:
                player.move_left()

    def finished(self):
        self.bot.finished()
