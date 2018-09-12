# -*- coding: UTF-8 -*-

import pygame
from Level import Tileset, Button, Player
import datetime


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
        self.player_x = -200
        self.player_y = -200
        self.goals = list()
        self.name = ''
        self.is_bot = False
        self.goal_reached = False
        self.texts = list()
        self.font = pygame.font.SysFont('Comic Sans MS', 40)
        self.started = False
        self.time = list()

        self.lines_x = list()
        self.lines_y = list()

        # Mapsize in Tiles
        self.width = 22
        self.height = 16

        # Erstellen einer leeren Liste der Tiles
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
        for player in self.players:
            screen.blit(self.tileset.image, (player.x, player.y), player.rect)
        for dot in self.dots:
            dot.render(screen)
        for player in self.players:
            for dot in self.dots:
                if dot.x-38 < player.x < dot.x+15 and dot.y-38 < player.y < dot.y+15:
                    player.fail()
        for string in self.texts:
            text = self.font.render(string[0], False, (0, 0, 0))
            screen.blit(text, (string[1], string[2]))
        for button in self.buttons:
            button.render(screen)
    # Tastendrücke verarbeiten:

    def handle_input(self, key):
        if not self.is_bot and not self.goal_reached:
            if not self.started and self.name != '':
                self.time()
            player = self.players[0]
            if key == pygame.K_LEFT:
                player.move_left()
            elif key == pygame.K_RIGHT:
                player.move_right()
            elif key == pygame.K_UP:
                player.move_up()
            elif key == pygame.K_DOWN:
                player.move_down()

    def time(self):
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
            if button.clicked and whathit is not None:
                if not isinstance(button, whathit):
                    button.unclick(self)
            elif button.clicked:
                button.unclick(self)

    def fail(self):
        self.texts.append(('Aww you failed :(', 375, 150))
        self.buttons.append(Button.RestartButton())
        self.goal_reached = True

    def done(self, time):
        text = ''
        if time[0] != 0:
            text += '%d days and '
        text += '%d:%d:%d:%d' % (time[1], time[2], time[3], time[4])
        self.texts.append(('You won! Your Time: '+text, 225, 150))
        self.buttons.append(Button.RestartButton())
        self.goal_reached = True
        self.started = False

    def move(self):
        if not self.is_bot:
            return
        if len(self.players) == 0:
            self.finished()
        for player in self.players:
            move = player.moves[player.count_moves]
            if move == 0:
                player.move_up()
            elif move == 1:
                player.move_right()
            elif move == 2:
                player.move_down()
            else:
                player.move_left()

    def finished(self):
        pass
