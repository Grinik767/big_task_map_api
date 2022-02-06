import pygame
import requests


class Map:
    def __init__(self, coords):
        self.coords = coords
        self.map_type = 'map'
        self.spn = '0.002,0.002'
        self.map_file = "map.png"
        self.response = None
        self.need_mark = False
        self.mark_coords = ""
        self.reload_map()

    def map_request(self):
        server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": self.coords,
            "spn": self.spn,
            "l": self.map_type}
        if self.need_mark:
            params["pt"] = f"{self.mark_coords},pm2dbl"
        response = requests.get(server, params=params)
        if response:
            self.response = response

    def map_to_img(self):
        if self.response:
            with open(self.map_file, "wb") as file:
                file.write(self.response.content)

    def reload_map(self):
        self.map_request()
        self.map_to_img()

    def map_update_by_keys(self, event):
        step_spn = list(map(float, self.spn.split(',')))
        coords = list(map(float, self.coords.split(",")))

        if event.key == pygame.K_PAGEUP:
            if step_spn[0] - 0.005 >= 0.002:
                step_spn[0] -= 0.005
                step_spn[1] -= 0.005
        if event.key == pygame.K_PAGEDOWN:
            if step_spn[0] + 0.005 <= 10:
                step_spn[0] += 0.005
                step_spn[1] += 0.005

        if event.key == pygame.K_UP:
            coords[1] += 2 * step_spn[1]
        if event.key == pygame.K_DOWN:
            coords[1] -= 2 * step_spn[1]

        if event.key == pygame.K_RIGHT:
            coords[0] += 2 * step_spn[0]
        if event.key == pygame.K_LEFT:
            coords[0] -= 2 * step_spn[0]

        self.coords = ','.join(list(map(str, coords)))
        self.spn = ','.join(list(map(str, step_spn)))
        self.reload_map()

    def map_update(self, new_coords):
        self.coords = new_coords
        self.need_mark = True
        self.mark_coords = new_coords
        self.reload_map()
