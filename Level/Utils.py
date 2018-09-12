# -*- coding: UTF-8 -*-

import pygame
import os
import platform

# Hilfsfunktion, um ein Bild zu laden:


def load_image(filename, colorkey=None):
    file_path = os.path.dirname(os.path.realpath(__file__))
    whichos = platform.system()
    if whichos == 'Linux':
        direct = '/'
    elif whichos == 'Windows':
        direct = '\\'
    else:
        print('You are running on an unrecognized Operating System!\n' + whichos)
        direct = '/'
    # Pygame das Bild laden lassen.
    image = pygame.image.load(file_path + direct + filename)
    # Das Pixelformat der Surface an den Bildschirm (genauer: die screen-Surface) anpassen.
    # Dabei die passende Funktion verwenden, je nach dem, ob wir ein Bild mit Alpha-Kanal haben oder nicht.
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image.set_alpha(None)
        # image = image.convert_alpha()
    # Colorkey des Bildes setzen, falls nicht None.
    # Bei -1 den Pixel im Bild an Position (0, 0) als Colorkey verwenden.
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    return image
