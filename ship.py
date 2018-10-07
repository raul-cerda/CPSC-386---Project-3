# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders
import pygame
from pygame.sprite import Sprite


# save a spriteSheet to begin and save each sprite to array (0 = ship, 1 and 2 = blow up)
class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.all_frames = []
        self.sheet = pygame.image.load('images/shipSheet.png')
        self.image = pygame.Surface((55, 40))
        self.image.set_colorkey((0, 0, 0))

        self.image.blit(self.sheet, (0, 0), (0, 0, 55, 40))
        self.all_frames.append(self.image)
        self.image = pygame.Surface((55, 40))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.sheet, (0, 0), (0, 40, 55, 40))
        self.all_frames.append(self.image)
        self.image = pygame.Surface((55, 40))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.sheet, (0, 0), (0, 80, 55, 40))
        self.all_frames.append(self.image)
        self.image = pygame.Surface((55, 40))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.sheet, (0, 0), (0, 120, 55, 40))
        self.all_frames.append(self.image)

        self.image = self.all_frames[0]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False
        self.exploding = False
        self.explosion_frame = 1

    def update(self):
        if not self.exploding:
            self.image = self.all_frames[0]
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

            self.rect.centerx = self.center
        else:
            if self.explosion_frame == 1:
                self.explosion_frame = 2
                self.image = self.all_frames[self.explosion_frame]
            elif self.explosion_frame == 2:
                self.explosion_frame = 3
                self.image = self.all_frames[self.explosion_frame]
            elif self.explosion_frame == 3:
                self.explosion_frame = 1
                self.image = self.all_frames[self.explosion_frame]
            pygame.time.delay(100)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
