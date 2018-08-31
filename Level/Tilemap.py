# -*- coding: UTF-8 -*-

import pygame
import random
import Tileset
import Button

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
        self.player_x = 3 * self.tileset.tile_width
        self.player_y = 3 * self.tileset.tile_height

        # Die Größe der Maps in Tiles.
        self.width = 30
        self.height = 25

        # Erstellen einer leeren Liste für die Tile Daten.
        self.tiles = list()

        # Manuelles Befüllen der Tile-Liste:
        # Jedes Feld bekommt ein zufälliges Tile zugewiesen.
        for i in range(0, self.height):
            self.tiles.append(list())
            for j in range(0, self.width):
                x = random.randint(0, 3)
                if x == 0:
                    self.tiles[i].append('dark')
                elif x == 1:
                    self.tiles[i].append('light')
                elif x == 2:
                    self.tiles[i].append('goal')
                else:
                    self.tiles[i].append('empty')
        self.player = self.tileset.get_tile('player')

        self.buttons = list()
        self.buttons.append(Button.Button('Load', 30, 30, 150, 75, 10, 30, Button.Button.load))


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
        screen.blit(self.tileset.image, (self.player_x, self.player_y), self.player.rect)
        for button in self.buttons:
            button.render(screen)
    # Tastendrücke verarbeiten:

    def handle_input(self, key, screen):
        # Pfeiltaste links oder rechts erhöht bzw. verringert die x-Position der Kamera.
        if key == pygame.K_LEFT:
            self.player_x -= 6
            screen.blit(self.tileset.image, (self.player_x, self.player_y), self.player.rect)
        if key == pygame.K_RIGHT:
            self.player_x += 6
            screen.blit(self.tileset.image, (self.player_x, self.player_y), self.player.rect)
        # Und das gleiche nochmal für die y-Position.
        if key == pygame.K_UP:
            self.player_y -= 6
            screen.blit(self.tileset.image, (self.player_x, self.player_y), self.player.rect)
        if key == pygame.K_DOWN:
            self.player_y += 6
            screen.blit(self.tileset.image, (self.player_x, self.player_y), self.player.rect)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.x < pos[0] < button.x + button.w and button.y < pos[1] < button.y + button.h:
                button.click(button)
