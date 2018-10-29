# -*- coding: UTF-8 -*-

import pygame
from Level import Tilemap

# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten
if not pygame.font: print('Error pygame.font module couldn\'t be loaded!')
if not pygame.mixer: print('Error pygame.mixer module couldn\'t be loaded!')


def main():
    try:
        # Fenster erstellen (wir bekommen eine Surface, die den Bildschirm repräsentiert)
        pygame.init()
        screen = pygame.display.set_mode((22*52, 16*52))

        pygame.display.set_caption("Hardest Game on Earth")
        pygame.mouse.set_visible(1)
        # Wiederholte Tastendrücke
        pygame.key.set_repeat(1, 30)

        # Clock-Objekt wegen Framebegrenzung
        clock = pygame.time.Clock()

        map = Tilemap.Tilemap()

        running = True

        while running:
            clock.tick(map.max_fps)
            # screen-Surface (Hintergrund) füllen
            screen.fill((180, 181, 254))
            # Alle Events bearbeiten
            for event in pygame.event.get():
                # Spiel beenden auf QUIT-Event
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Escape -> QUIT-Event in Event-Warteschlange
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    map.handle_input(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    map.clicked()
            map.render(screen)
            map.move()
            # Screen anzeigen
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()
# Starter wenn es manuell ausgeführt wird
