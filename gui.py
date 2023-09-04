import os
import sys

import pygame


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Button:
    def __init__(self, screen, rect: (int, int, int, int), text, color, font, color_text=(255, 255, 255)):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.text = text
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.screen = screen
        self.color_text = color_text
        self.font = font

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        text = self.font.render(self.text, 1, self.color_text)
        self.screen.blit(text,
                         (self.x + self.w / 2 - text.get_width() / 2, self.y + self.h / 2 - text.get_height() / 2))

    def is_clicked(self, pos):
        if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
            return True
        else:
            return False


class Rect:
    def __init__(self, screen, coordinates: (int, int, int, int), color=(255, 255, 255)):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.w = coordinates[2]
        self.h = coordinates[3]
        self.screen = screen
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))
