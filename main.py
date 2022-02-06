import os
import pygame
import pygame_textinput

from map import Map
from geocoder import Geocoder
from funcs import check_button

if __name__ == '__main__':
    coords = "37.530887,55.703118"
    mp = Map(coords)

    pygame.init()
    screen = pygame.display.set_mode((600, 550))
    screen.fill((255, 255, 255))
    screen.blit(pygame.image.load(mp.map_file), (0, 100))
    finder = pygame.image.load('data/finder.png')
    earth = pygame.image.load('data/earth.png')
    spacecraft = pygame.image.load('data/spacecraft.png')
    map_img = pygame.image.load('data/map.png')
    screen.blit(finder, (535, 50))
    screen.blit(map_img, (10, 5))
    screen.blit(spacecraft, (60, 5))
    screen.blit(earth, (130, 5))
    pygame.display.flip()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 60)
    textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
    textinput.cursor_width = 2
    rect_input = pygame.Rect(10, 50, 520, 42)
    keys_to_funcs = [pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
    run = True
    while run:
        screen.fill((255, 255, 255))
        events = pygame.event.get()
        textinput.update(events)
        screen.blit(textinput.surface, (13, 56))
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key in keys_to_funcs:
                mp.map_update_by_keys(event)
            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                if check_button(x, y, 535, 50, finder.get_width(), finder.get_height(), event):
                    geo = Geocoder(textinput.value)
                    coords = geo.get_coords_from_json()
                    mp.map_add_mark(coords)
                if check_button(x, y, 10, 5, map_img.get_width(), map_img.get_height(), event):
                    mp.map_change_type("map")
                if check_button(x, y, 60, 5, spacecraft.get_width(), spacecraft.get_height(), event):
                    mp.map_change_type("sat")
                if check_button(x, y, 130, 5, earth.get_width(), earth.get_height(), event):
                    mp.map_change_type("sat,skl")
        pygame.draw.rect(screen, (0, 0, 0), rect_input, 1)
        screen.blit(pygame.image.load(mp.map_file), (0, 100))
        screen.blit(finder, (535, 50))
        screen.blit(map_img, (10, 5))
        screen.blit(spacecraft, (60, 5))
        screen.blit(earth, (130, 5))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    os.remove(mp.map_file)
