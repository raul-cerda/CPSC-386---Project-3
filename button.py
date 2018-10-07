# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame.font


# manages start button
class Button:
    def __init__(self, screen, msg, but_type):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.but_type = but_type

        self.width, self.height = 200, 50
        self.button_color = 0, 255, 0
        self.text_color = 255, 255, 255
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = int(self.screen_rect.centery * 1.55)
        if but_type == 2:
            self.rect.y += 75

        self.msg_image = None
        self.msg_image_rect = None

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.msg_image, self.msg_image_rect)
