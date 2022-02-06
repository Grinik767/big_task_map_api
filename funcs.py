import pygame

coords_start = "37.530887,55.703118"


def check_button(x, y, xb, yb, w, h, event):
    if xb <= x <= xb + w and yb <= y <= yb + h:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False
