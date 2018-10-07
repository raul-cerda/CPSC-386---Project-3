# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders

import sys
from time import sleep
import pygame
import random
from bullet import Bullet
from alien import Alien
from button import Button
from bunker import Bunker


# check for any special events like explosions or key presses
def check_events(ai_setting, screen, stats, sb, play_button, score_button, ship, aliens, bullets, ai_bullets, bunkers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_setting, screen, ship, bullets, ai_bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, score_button, ship, aliens, bullets, m_x,
                              m_y, bunkers)
        elif event.type == ai_setting.animate_event:
            for alien in aliens:
                alien.switch_img()

        elif event.type == pygame.USEREVENT + 2:          # resumes aliens after a pause by ship explosion
            for alien in aliens:
                alien.pause = False
            ai_setting.alien_speed_factor = ai_setting.backup_alien_speed
            ship.exploding = False

        elif event.type == pygame.USEREVENT + 3 and stats.game_active:        # catches events for alien shot firing
            for alien in aliens:
                if random.randint(1, 100) == 1:
                    fire_bullet(ai_setting, screen, alien, bullets, ai_bullets, False)


# check for mouse input
def check_play_button(ai_setting, screen, stats, sb, play_button, score_button, ship, aliens, bullets, m_x, m_y,
                      bunkers):
    button_clicked = play_button.rect.collidepoint(m_x, m_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, ship, aliens)
        create_bunkers(ai_setting, screen, bunkers)
        ship.center_ship()
        ai_setting.bg_music[0].play(loops=-1)
    else:
        button_clicked = score_button.rect.collidepoint(m_x, m_y)
        if button_clicked and not stats.game_active:
            sb.show_leaderboard()
            pygame.display.flip()
            sleep(3.3)


def check_keydown_events(event, ai_setting, screen, ship, bullets, ai_bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, ship, bullets, ai_bullets, True)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


# draw all the game objects
def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button, score_button, ai_bullets, bunkers):
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in ai_bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    bunkers.draw(screen)

    if not stats.game_active:
        show_menu(ai_setting, screen, play_button, score_button)
    pygame.display.flip()


def create_bunkers(ai_setting, screen, bunkers):
    for i in range(1, 6):
        new_bunker = Bunker(ai_setting, screen)
        new_bunker.rect.left = screen.get_rect().right/6 * i
        bunkers.add(new_bunker)


def show_menu(ai_setting, screen, play_button, score_button):
    screen.fill((0, 0, 0), screen.get_rect())
    play_button.draw_button()
    score_button.draw_button()

    y = screen.get_rect().centery - 50
    for i in range(1, 4):
        example = Alien(ai_setting, screen, i, 0)
        example.rect.centerx = screen.get_rect().centerx - 125
        example.rect.centery = y
        y += 50
        example.blitme()
    example = Alien(ai_setting, screen, 0, 0)
    example.rect.centerx = screen.get_rect().centerx - 125
    example.rect.centery = y
    example.blitme()

    display_point_values(screen)
    display_title(screen)


def display_point_values(screen):
    first = Button(screen, "=  10 PTS", 1)
    first.rect.centery = screen.get_rect().centery - 50
    first.prep_msg('=  10 PTS')
    sec = Button(screen, "=  20 PTS", 1)
    sec.rect.centery = screen.get_rect().centery
    sec.prep_msg('=  20 PTS')
    third = Button(screen, "=  40 PTS", 1)
    third.rect.centery = screen.get_rect().centery + 50
    third.prep_msg('=  40 PTS')
    four = Button(screen, " = ???", 1)
    four.rect.centery = screen.get_rect().centery + 100
    four.prep_msg('  = ???')

    first.draw_button()
    sec.draw_button()
    third.draw_button()
    four.draw_button()


def display_title(screen):
    title = Button(screen, "SPACE", 1)
    title.font = pygame.font.SysFont(None, 130)
    title.rect.centery = screen.get_rect().centery - 230
    title.prep_msg('SPACE')

    s_title = Button(screen, "INVADERS", 1)
    s_title.font = pygame.font.SysFont(None, 75)
    s_title.text_color = (0, 225, 0)
    s_title.rect.centery = screen.get_rect().centery - 170
    s_title.prep_msg('INVADERS')

    title.draw_button()
    s_title.draw_button()


def update_bullets(ai_setting, screen, stats, ship, sb, aliens, bullets, ai_bullets, bunkers):
    bullets.update()
    ai_bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for bullet in ai_bullets.copy():
        if bullet.rect.top >= screen.get_rect().bottom:
            ai_bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, stats, ship, sb, aliens, bullets, ai_bullets)
    check_bullet_ship_collisions(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets)
    check_bullet_bunker_collisions(bullets, ai_bullets, bunkers)


# increases score depending on alien type hit, ufo give random bigger score
def check_bullet_alien_collisions(ai_setting, screen, stats, ship, sb, aliens, bullets, ai_bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for alients in collisions.values():
            if alients[0].alien_type == 1:
                stats.score += ai_setting.alien_points * len(alients)
            elif alients[0].alien_type == 2:
                stats.score += ai_setting.alien_points * 2 * len(alients)
            elif alients[0].alien_type == 3:
                stats.score += ai_setting.alien_points * 4 * len(alients)
            else:
                stats.last_ufo_points = ai_setting.alien_points * random.randint(10, 20)
                stats.score += stats.last_ufo_points
                alients[0].ufo_sound.stop()
            for alien in alients:
                alien.explode(stats)
        sb.prep_score()
        pew = pygame.mixer.Sound("sounds/alien_boom.wav")
        pew.play()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, ship, aliens)
        ai_setting.bg_music[0].play(loops=-1)


def check_bullet_ship_collisions(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets):
    collisions = pygame.sprite.spritecollideany(ship, ai_bullets)
    if collisions:
        ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets)


def check_bullet_bunker_collisions(bullets, ai_bullets, bunkers):
    collisions = pygame.sprite.groupcollide(bunkers, bullets, False, True)
    if collisions:
        for bullets in collisions.values():
            x = bullets[0].rect.x
            list(collisions.keys())[0].damage_bot(x)

    collisions = pygame.sprite.groupcollide(bunkers, ai_bullets, False, True)
    if collisions:
        for bullets in collisions.values():
            x = bullets[0].rect.x
            list(collisions.keys())[0].damage_top(x)


# checks if player is allowed another bullet onscreen first and creates alien shots as well
def fire_bullet(ai_setting, screen, ship, bullets, ai_bullets, ship_fired):
    if len(bullets) < ai_setting.bullets_allowed and ship_fired:
        new_bullet = Bullet(ai_setting, screen, ship, True)
        bullets.add(new_bullet)
        pew = pygame.mixer.Sound("sounds/bullet_pew.wav")
        pew.play(maxtime=500)
    elif not ship_fired:
        new_bullet = Bullet(ai_setting, screen, ship, False)
        ai_bullets.add(new_bullet)
        pew = pygame.mixer.Sound("sounds/alien_pew.wav")
        pew.play(maxtime=500)


# next four functions contains math for creating alien fleet that fits onscreen
def get_number_aliens_x(ai_setting, alien_width):
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_setting, ship_height, alien_height):
    available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_setting, screen, aliens, alien_number, row_number, alien_type, current_frame):
    alien = Alien(ai_setting, screen, alien_type, current_frame)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    ai_setting.current_song = 0
    ai_setting.bg_music[1].stop()
    ai_setting.bg_music[2].stop()
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)
    ai_setting.fleet_created_at = pygame.time.get_ticks()
    current_type = 1
    current_frame = 0
    alien = Alien(ai_setting, screen, current_type, 0)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)

    alien_type_counter = 0
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            if current_frame == 1:
                current_frame = 0
            elif current_frame == 0:
                current_frame = 1
            create_alien(ai_setting, screen, aliens, alien_number, row_number, current_type, current_frame)
            alien_type_counter += 1
            if alien_type_counter >= number_aliens_x * 2:
                current_type += 1
                alien_type_counter = 0


def create_ufo(ai_setting, screen, aliens):
    ufo = Alien(ai_setting, screen, 0, 0)
    ufo.rect.right = 0
    ufo.rect.top = 10
    ufo.x = ufo.rect.x
    ufo.y = ufo.rect.y
    ufo.ufo_sound.play(loops=-1)
    aliens.add(ufo)


def check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets)
            break


# checks time elapsed since fleet spawn and previous ufo to decide if new ufo should be allowed
def update_aliens(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets):
    if (pygame.time.get_ticks() - ai_setting.fleet_created_at) > 10000:
        if pygame.time.get_ticks() - ai_setting.ufo_created_at > 10000 and random.randint(1, 2500) == 1:
            create_ufo(ai_setting, screen, aliens)
            ai_setting.ufo_created_at = pygame.time.get_ticks()
    check_fleet_edges(ai_setting, aliens)
    if len(aliens) == 35 and ai_setting.current_song != 1:
        ai_setting.bg_music[0].stop()
        ai_setting.bg_music[1].play(loops=-1)
        ai_setting.current_song = 1
    if len(aliens) == 20 and ai_setting.current_song != 2:
        ai_setting.bg_music[1].stop()
        print('woo')
        ai_setting.bg_music[2].play(loops=-1)
        ai_setting.current_song = 2
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets)
    check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets)


def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges() and alien.alien_type != 0:
            change_fleet_direction(ai_setting, aliens)
            break
        elif alien.check_edges() and alien.alien_type == 0:
            alien.ufo_sound.stop()
            alien.remove(aliens)
            alien.kill()


def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.alien_type != 0:
            alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


# directions for when ship is hit
def ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets, ai_bullets):
    if stats.ships_left > 0:
        ship.exploding = True
        pew = pygame.mixer.Sound("sounds/ship_boom.ogg")
        pew.play()
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        ai_bullets.empty()
        create_fleet(ai_setting, screen, ship, aliens)
        for alien in aliens:
            alien.pause = True
        pygame.time.set_timer(pygame.USEREVENT + 2, 1500)
        ship.center_ship()
        ai_setting.bg_music[0].stop()
        ai_setting.bg_music[1].stop()
        ai_setting.bg_music[2].stop()
        ai_setting.bg_music[0].play(loops=-1)
        ai_setting.current_song = 0
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        ai_setting.bg_music[0].stop()
        ai_setting.bg_music[1].stop()
        ai_setting.bg_music[2].stop()


# compares current and high score, also saves scores to text file
def check_high_score(stats, sb):
    stats.new_high_score(stats.score)
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
