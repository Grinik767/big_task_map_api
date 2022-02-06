import os
import pygame
import pygame_textinput

from map import Map
from geocoder import Geocoder
from funcs import check_button, coords_start

if __name__ == '__main__':
    coords = coords_start
    mp = Map(coords)
    address = ""

    pygame.init()
    font = pygame.font.SysFont("Arial", 18)
    font_tick = pygame.font.SysFont("Arial", 35, bold=True)
    screen = pygame.display.set_mode((600, 600))
    screen.fill((255, 255, 255))
    screen.blit(pygame.image.load(mp.map_file), (0, 150))
    finder = pygame.image.load('data/finder.png')
    earth = pygame.image.load('data/earth.png')
    spacecraft = pygame.image.load('data/spacecraft.png')
    map_img = pygame.image.load('data/map.png')
    reset = pygame.image.load('data/recet.png')
    screen.blit(finder, (535, 50))
    screen.blit(map_img, (10, 5))
    screen.blit(spacecraft, (60, 5))
    screen.blit(earth, (130, 5))
    screen.blit(reset, (5, 155))
    pygame.display.flip()
    clock = pygame.time.Clock()

    manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 60)
    textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
    textinput.cursor_width = 2
    rect_input = pygame.Rect(10, 50, 520, 42)
    tick = "+"
    tick_c = True
    postal = "Прописывать индекс в адресе"
    text_postal = font.render(postal, True, (0, 0, 0))
    rect_tick = pygame.Rect(195, 5, 30, 30)

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
                if check_button(x, y, 535, 50, finder.get_width(), finder.get_height(), event) and textinput.value:
                    geo = Geocoder(textinput.value)
                    coords = geo.get_coords_from_json()
                    address = geo.get_address_from_json()
                    if tick_c:
                        address += f"; Индекс: {geo.get_postal_code_from_json()}"
                    mp.map_add_mark(coords)
                if check_button(x, y, 10, 5, map_img.get_width(), map_img.get_height(), event):
                    mp.map_change_type("map")
                if check_button(x, y, 60, 5, spacecraft.get_width(), spacecraft.get_height(), event):
                    mp.map_change_type("sat")
                if check_button(x, y, 130, 5, earth.get_width(), earth.get_height(), event):
                    mp.map_change_type("sat,skl")
                if check_button(x, y, 5, 155, reset.get_width(), reset.get_height(), event):
                    textinput.value = ""
                    mp.clear_map()
                    address = ""
                if check_button(x, y, 195, 5, rect_tick.width, rect_tick.height, event):
                    if tick_c:
                        tick = ""
                    else:
                        tick = "+"
                    tick_c = not tick_c
        pygame.draw.rect(screen, (0, 0, 0), rect_input, 1)
        screen.blit(pygame.image.load(mp.map_file), (0, 150))
        screen.blit(finder, (535, 50))
        screen.blit(map_img, (10, 5))
        screen.blit(spacecraft, (60, 5))
        screen.blit(earth, (130, 5))
        screen.blit(reset, (5, 155))
        text_address = font.render(address, True, (0, 0, 0))
        screen.blit(text_address, (5, 105))

        pygame.draw.rect(screen, (0, 0, 0), rect_tick, 1)
        text_tick = font_tick.render(tick, True, (0, 0, 255))
        screen.blit(text_tick, (202, 0))
        screen.blit(text_postal, (230, 10))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    os.remove(mp.map_file)
