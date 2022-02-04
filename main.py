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


if __name__ == '__main__':
    coords = "37.530887,55.703118"
    mp = Map(coords)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(mp.map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(mp.map_file)
