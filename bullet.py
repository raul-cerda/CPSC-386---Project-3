# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame
from pygame.sprite import Sprite


# bullet created at tip of ship and moves up y axis
class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship, ship_bullet):
        super(Bullet, self).__init__()
        self.screen = screen
        self.ship_bullet = ship_bullet

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.image = pygame.Surface((ai_settings.bullet_width, ai_settings.bullet_height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        if ship_bullet:
            self.color = (200, 255, 91)
        else:
            self.color = (255, 255, 255)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        if self.ship_bullet:
            self.y -= self.speed_factor
            self.rect.y = self.y
        else:
            self.y += self.speed_factor
            self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
