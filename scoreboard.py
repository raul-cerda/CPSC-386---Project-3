# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame.font
from pygame.sprite import Group
from ship import Ship


# displays all HUD elements like score and level
# final function shows high score list on start screen
class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = 100, 100, 100
        self.font = pygame.font.SysFont(None, 48)

        self.ships = None
        self.level_image = None
        self.level_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.score_image = None
        self.score_rect = None

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        level_msg = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_msg, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_leaderboard(self):
        lb_text = "HIGH SCORES"
        lb_image = self.font.render(lb_text, True, (0, 255, 0))
        lb_rect = lb_image.get_rect()
        lb_rect.centerx = self.screen_rect.centerx
        lb_rect.centery = self.screen_rect.centery - 100

        score1 = str(int(self.stats.high_scores[0]))
        score1 = self.font.render(score1, True, (255, 255, 255))
        score1_rect = score1.get_rect()
        score1_rect.centerx = self.screen_rect.centerx
        score1_rect.centery = self.screen_rect.centery - 50

        score2 = str(int(self.stats.high_scores[1]))
        score2 = self.font.render(score2, True, (255, 255, 255))
        score2_rect = score2.get_rect()
        score2_rect.centerx = self.screen_rect.centerx
        score2_rect.centery = self.screen_rect.centery

        score3 = str(int(self.stats.high_scores[2]))
        score3 = self.font.render(score3, True, (255, 255, 255))
        score3_rect = score3.get_rect()
        score3_rect.centerx = self.screen_rect.centerx
        score3_rect.centery = self.screen_rect.centery + 50

        self.screen.fill((0, 0, 0))
        self.screen.blit(lb_image, lb_rect)
        self.screen.blit(score1, score1_rect)
        self.screen.blit(score2, score2_rect)
        self.screen.blit(score3, score3_rect)
