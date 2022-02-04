import os

import pygame
import requests


class Map:
    def __init__(self, coords):
        self.coords = coords
        self.map_type = 'map'
        self.spn = '0.002,0.002'
        self.map_file = "map.png"
        self.response = None
        self.map_request()
        self.map_to_img()

    def map_request(self):
        server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": self.coords,
            "spn": self.spn,
            "l": self.map_type}
        response = requests.get(server, params=params)
        if response:
            self.response = response

    def map_to_img(self):
        if self.response:
            with open(self.map_file, "wb") as file:
                file.write(self.response.content)

    def map_update(self, event):
        step_spn = list(map(float, self.spn.split(',')))
        if event.key == pygame.K_PAGEUP:
            if step_spn[0] - 0.005 >= 0.002:
                step_spn[0] -= 0.005
                step_spn[1] -= 0.005
        if event.key == pygame.K_PAGEDOWN:
            if step_spn[0] + 0.005 <= 10:
                step_spn[0] += 0.005
                step_spn[1] += 0.005
        self.spn = ','.join(list((map(str, step_spn))))
        self.map_request()
        self.map_to_img()


if __name__ == '__main__':
    coords = "37.530887,55.703118"
    mp = Map(coords)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(mp.map_file), (0, 0))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                mp.map_update(event)
        screen.blit(pygame.image.load(mp.map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(mp.map_file)
