# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame


class Settings:
    # bsse settings shared between every session
    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 660   # 576
        self.bg_color = (50, 0, 50)
        self.current_song = 0
        self.bg_music = [pygame.mixer.Sound('sounds/bg_music.wav'), pygame.mixer.Sound('sounds/bg_music1.wav'),
                         pygame.mixer.Sound('sounds/bg_music2.wav')]
        self.bg_music[self.current_song].set_volume(1.0)

        self.ship_limit = 3

        self.bullet_width = 5
        self.bullet_height = 20
        self.bullets_allowed = 3

        self.fleet_drop_speed = 20

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.fleet_created_at = 0
        self.ufo_created_at = 0

        self.animate_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.animate_event, 1300)

        # dynamic settings that change with level
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.7
        self.backup_alien_speed = 0.7
        self.fleet_direction = 1
        self.alien_points = 10

        self.initialize_dynamic_settings()

    # settings that increase with each level
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.7
        self.backup_alien_speed = 0.7

        self.fleet_direction = 1

        self.alien_points = 10

    # increases difficulty
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.backup_alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
