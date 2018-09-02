# -*- coding: UTF-8 -*-

import pygame
import random
import Tileset
import Button
import Player

# Die Tilemap Klasse verwaltet die Tile-Daten, die das Aussehen der Karte beschreiben


class Tilemap(object):

    def __init__(self, screen):
        # neues Tileset
        self.tileset = Tileset.Tileset('template.png', (255, 0, 255), 52, 52)
        self.tileset.add_tile('dark', 0, 0)
        self.tileset.add_tile('light', 52, 0)
        self.tileset.add_tile('goal', 104, 0)
        self.tileset.add_tile('player', 0, 52)
        self.tileset.add_tile('empty', 52, 52)
        self.player_x = -200
        self.player_y = -200

        self.lines = list()

        # Mapsize in Tiles
        self.width = 30
        self.height = 25

        # Erstellen einer leeren Liste der Tiles
        self.tiles = list()

        self.player = self.tileset.get_tile('player')

        for i in range(0, self.height):
            self.tiles.append(list())
            for j in range(0, self.width):
                self.tiles[i].append('empty')

        self.buttons = list()
        self.buttons.append(Button.LoadButton('Load', 30, 30))

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
        for player in self.players:
            screen.blit(self.tileset.image, (player.x, player.y), player.rect)
        #screen.blit(self.tileset.image, (self.player_x, self.player_y), self.player.rect)
        for button in self.buttons:
            button.render(screen)
    # Tastendrücke verarbeiten:

    def handle_input(self, key, screen):
        if len(self.players) == 1:
            player = self.players[0]
            if key == pygame.K_LEFT:
                player.move_left()
            if key == pygame.K_RIGHT:
                player.move_right()
            if key == pygame.K_UP:
                player.move_up()
            if key == pygame.K_DOWN:
                player.move_down()

    def clicked(self):
        pos = pygame.mouse.get_pos()
        hit = False
        for button in self.buttons:
            if button.x < pos[0] < button.x + button.w and button.y < pos[1] < button.y + button.h:
                hit = True
                if not button.clicked:
                    button.click(self)
                else:
                    button.unclick(self)
        if not hit:
            for button in self.buttons:
                if button.clicked:
                    button.unclick(self)
