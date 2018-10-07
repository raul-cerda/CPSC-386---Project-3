# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


# Main game loop with initializations
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    play_button = Button(screen, "PLAY GAME", 1)
    score_button = Button(screen, "HIGH SCORES", 2)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    ai_bullets = Group()
    bunkers = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, score_button, ship, aliens, bullets, ai_bullets,
                        bunkers)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, ship, sb, aliens, bullets, ai_bullets, bunkers)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, ai_bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, score_button, ai_bullets,
                         bunkers)


run_game()
