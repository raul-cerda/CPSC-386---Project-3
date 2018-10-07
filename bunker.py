# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame
from pygame.sprite import Sprite


# aliens are all same class, only separated by an int representing type of alien
class Bunker(Sprite):
    def __init__(self, ai_settings, screen):
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/bunker.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = screen.get_rect().left + 120
        self.rect.y = screen.get_rect().bottom - 115

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def damage_bot(self, bullet_x):
        pix_arr = pygame.PixelArray(self.image)
        pix_x = bullet_x - self.rect.left
        if pix_arr[pix_x, 39] != (0, 0, 0, 0):
            for y in range(39, 30, -1):
                for x in range(pix_x - 6, pix_x + 6):
                    try:
                        pix_arr[x, y] = (0, 0, 0, 0)
                    except IndexError:
                        pass
        pix_arr.close()

    def damage_top(self, bullet_x):
        pix_arr = pygame.PixelArray(self.image)
        pix_x = bullet_x - self.rect.left
        if pix_arr[pix_x, 39] != (0, 0, 0, 0):
            for y in range(0, 10):
                for x in range(pix_x - 6, pix_x + 6):
                    try:
                        pix_arr[x, y] = (0, 0, 0, 0)
                    except IndexError:
                        pass
        pix_arr.close()
