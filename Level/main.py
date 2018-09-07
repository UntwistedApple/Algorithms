# -*- coding: UTF-8 -*-

import pygame
import Tilemap


# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten
if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')


def main():
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
        clock.tick(30)
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
        # Screen anzeigen
        pygame.display.flip()


if __name__ == '__main__':
    main()
# Starter wenn es manuell ausgeführt wird
