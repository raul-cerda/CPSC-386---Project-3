# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame
from pygame.sprite import Sprite


# aliens are all same class, only separated by an int representing type of alien
class Alien(Sprite):
    def __init__(self, ai_settings, screen, alien_type, current_frame):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.ufo_sound = pygame.mixer.Sound('sounds/ufo_sound.wav')
        self.ufo_sound.set_volume(0.3)

        self.alien_type = alien_type
        self.current_frame = current_frame
        self.set_for_deletion = False
        self.time_of_death = 0
        self.pause = False

        if self.alien_type == 0:
            self.alien_imgs = [pygame.image.load('images/alien4.png'), pygame.image.load('images/alien4.png')]
            self.image = self.alien_imgs[current_frame]
        elif self.alien_type == 1:
            self.alien_imgs = [pygame.image.load('images/alien1.png'), pygame.image.load('images/alien1a.png')]
            self.image = self.alien_imgs[current_frame]
        elif self.alien_type == 2:
            self.alien_imgs = [pygame.image.load('images/alien2.png'), pygame.image.load('images/alien2a.png')]
            self.image = self.alien_imgs[current_frame]
        else:
            self.alien_imgs = [pygame.image.load('images/alien3.png'), pygame.image.load('images/alien3a.png')]
            self.image = self.alien_imgs[current_frame]

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.pause:
            self.ai_settings.alien_speed_factor = 0

        if self.alien_type == 0:
            self.x += self.ai_settings.alien_speed_factor / 2
        else:
            self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        if self.set_for_deletion and pygame.time.get_ticks() - self.time_of_death >= 100 and self.alien_type != 0:
            self.kill()
        elif self.set_for_deletion and pygame.time.get_ticks() - self.time_of_death >= 300:
            self.kill()

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0 and self.alien_type != 0:
            return True
        return False

    def switch_img(self):
        if self.current_frame == 0:
            self.current_frame = 1
            self.image = self.alien_imgs[self.current_frame]
        elif self.current_frame == 1:
            self.current_frame = 0
            self.image = self.alien_imgs[self.current_frame]

    def explode(self, stats):
        self.current_frame = 2
        if self.alien_type == 0:
            font = pygame.font.SysFont(None, 40)
            self.image = font.render(str(stats.last_ufo_points), True, (255, 255, 255))
        else:
            self.image = pygame.image.load('images/alienExplode.png')
        self.set_for_deletion = True
        self.time_of_death = pygame.time.get_ticks()
