# -*- coding: UTF-8 -*-

import TileType
import Utils


class Tileset:
    # Im Konstruktor laden wir die Grafik
    # und erstellen ein leeres Dictionary für die Tile-Typen.
    def __init__(self, image, colorkey, tile_width, tile_height):
        self.image = Utils.load_image(image, colorkey)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_types = dict()

    # Tile-Typ in Liste einfügen

    def add_tile(self, name, start_x, start_y):
        self.tile_types[name] = TileType.TileType(name, start_x, start_y, self.tile_width, self.tile_height)

    # Tile-Typ in Liste suchen/finden

    def get_tile(self, name):
        try:
            return self.tile_types[name]
        except KeyError:
            return None
