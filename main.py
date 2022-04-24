import pygame
from pygame import mixer
import sys
import math
import random
from Button import Button

# initialize pygame
pygame.init()
mixer.init()

# create a screen
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

# icon
game_icon = pygame.image.load("game_icon.png")
pygame.display.set_icon(game_icon)


# game font
def get_font(size):
    return pygame.font.Font('font.ttf', size)


def run_game():
    # clear screen
    screen.fill("black")

    # load image background
    background = pygame.image.load('game_background.png')

    # title
    pygame.display.set_caption("Space Invanders: The other side")

    # sounds
    sound_background = mixer.Sound('background.wav')
    sound_shoot = mixer.Sound('shoot.wav')
    sound_explosion = mixer.Sound('explosion.wav')
    sound_background.play(-1)

    # player
    class Player:
        def __init__(self):
            self.image = pygame.image.load('game_player.png')
            self.x = 400
            self.y = 25
            self.size = 64

            self.speed_x = 0
            self.speed_y = 0
            self.general_speed = 8

        def draw(self):
            screen.blit(self.image, (self.x, self.y))

        def move(self):
            self.x += self.speed_x
            self.y += self.speed_y

        def keep_inside(self, screen):
            screen_x, screen_y = screen.get_size()
            if (self.x < 0):
                self.x = 0
            elif (self.x + 64 > screen_x):
                self.x = screen_x - self.size

            if (self.y < 0):
                self.y = 0
            elif (self.y + 64 > screen_y):
                self.y = screen_y - self.size

        def move_event_get(self, events):
            for event in events:
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_d):
                        self.speed_x = self.general_speed
                    elif (event.key == pygame.K_a):
                        self.speed_x = -self.general_speed
                    elif (event.key == pygame.K_w):
                        self.speed_y = -self.general_speed
                    elif (event.key == pygame.K_s):
                        self.speed_y = self.general_speed
                elif (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_a):
                        self.speed_x = 0
                    elif (event.key == pygame.K_d):
                        self.speed_x = 0
                    elif (event.key == pygame.K_w):
                        self.speed_y = 0
                    elif (event.key == pygame.K_s):
                        self.speed_y = 0

        def reset(self):
            self.x = random.randint(0, 800) // 8 * 8
            self.y = 25

            self.speed_x = 0
            self.speed_y = 0
            self.general_speed = 8

    # enemy bullet
    class Enemy_bullet:
        def __init__(self):
            self.image = pygame.image.load('game_enemy_bullet.png')
            self.x = 0
            self.y = 0
            self.size = 64

            self.speed = 20
            self.state = "ready"

        def move(self):
            if (self.y <= 0 - self.size):
                self.state = "ready"
            elif (self.state == "fire"):
                self.y -= self.speed

        def draw_and_fire(self, enemy_x, enemy_y):
            if (self.state == "ready"):
                self.state = "fire"
                self.x = enemy_x
                self.y = enemy_y - 75  # 75 - distance for enemy
                screen.blit(self.image, (self.x, self.y))
                sound_shoot.play()
            else:
                screen.blit(self.image, (self.x, self.y))

    # enemy
    class Enemy:
        def __init__(self):
            self.image = pygame.image.load('game_enemy.png')
            self.x = 400
            self.y = 500

            self.speed = 4

        def draw(self):
            screen.blit(self.image, (self.x, self.y))

        def move(self, player_x):
            if (self.x < player_x):
                self.x += self.speed
            elif (self.x > player_x):
                self.x -= self.speed

        def reset(self):
            self.x = 400
            self.y = 500

            self.speed = 4

    class Game_events:
        def __init__(self):
            self.collision_constant = 45  # maximum distance between two objects to consider as collisions

        def is_collision(self, obj1_x, obj1_y, obj2_x, obj2_y):
            distance = math.sqrt(math.pow(obj1_x - obj2_x, 2) + math.pow(obj1_y - obj2_y, 2))

            if (distance <= self.collision_constant):
                return True
            else:
                return False

        def collision_player_enemy_bullet(self, score, player, enemy, enemy_bullet, obj1_x, obj1_y, obj2_x, obj2_y):
            if (self.is_collision(obj1_x, obj1_y, obj2_x, obj2_y)):
                enemy_bullet.state = "ready"
                score.value = 0
                player.reset()
                enemy.reset()
                sound_explosion.play()

        def collision_player_enemy(self, score, player, enemy, enemy_bullet, obj1_x, obj1_y, obj2_x, obj2_y):
            if (self.is_collision(obj1_x, obj1_y, obj2_x, obj2_y)):
                enemy_bullet.state = "ready"
                score.value += 1
                player.reset()
                enemy.reset()
                sound_explosion.play()

    class Score:
        def __init__(self):
            self.value = 0
            self.font = get_font(16)

            self.x = 10
            self.y = 10

        def draw(self):
            self.score = self.font.render("Score: " + str(self.value), True, "white")
            screen.blit(self.score, (self.x, self.y))

    # declare obj
    pause_button = Button(screen_size[0] - 120, 30, "Pause", get_font(16), 16, "green", "white")

    player = Player()
    enemy = Enemy()
    enemy_bullet = Enemy_bullet()
    game_events = Game_events()
    score = Score()
    clk = pygame.time.Clock()

    # game loop
    while True:
        # game rules

        # player rules
        player.move()
        player.keep_inside(screen)

        # enemy rules
        enemy.move(player.x)
        enemy_bullet.move()
        enemy_bullet.draw_and_fire(enemy.x, enemy.y)

        game_events.collision_player_enemy_bullet(score, player, enemy, enemy_bullet, player.x, player.y,
                                                  enemy_bullet.x,
                                                  enemy_bullet.y)
        game_events.collision_player_enemy(score, player, enemy, enemy_bullet, player.x, player.y, enemy.x, enemy.y)

        # mouse postion
        mouse_postion = pygame.mouse.get_pos()

        # draw
        player.draw()
        enemy.draw()
        score.draw()
        pause_button.update(screen)
        pause_button.hovering(mouse_postion)

        # events
        event_get = pygame.event.get()
        player.move_event_get(event_get)

        for event in event_get:
            if (event.type == pygame.QUIT):
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (pause_button.check_for_input):
                    pause_menu(sound_background)

        # screen update
        clk.tick(30)
        pygame.display.update()
        screen.blit(background, (0, 0))

        # value = 1
        # if(value == 1):
        # break


def main_menu():
    # clear screen
    # screen.fill("black")

    # load image background
    background = pygame.image.load('menu_background.jpg')
    background = pygame.transform.scale(background, (800, 600))

    # title
    pygame.display.set_caption("Menu")

    # sounds
    sound_background = mixer.Sound('menu_background.mp3')
    sound_background.play(-1)

    # menu title
    menu_title_p1 = get_font(40).render("Space Invaders:", True, "green")
    menu_title_p2 = get_font(32).render("The Other Side", True, "green")
    menu_title_p1_rect = menu_title_p1.get_rect(center=(screen_size[0] / 2, 50))
    menu_title_p2_rect = menu_title_p2.get_rect(center=(screen_size[0] / 2, 50 + 45))

    # declare buttons
    play_button = Button(screen_size[0] / 2, 250, "Play", get_font(24), 24, "green", "white")
    exit_button = Button(screen_size[0] / 2, 300, "Exit", get_font(24), 24, "green", "white")

    while True:
        # background
        screen.blit(background, (0, 0))

        # menu title
        screen.blit(menu_title_p1, menu_title_p1_rect)
        screen.blit(menu_title_p2, menu_title_p2_rect)

        # mouse position
        mouse_pos = pygame.mouse.get_pos()

        # buttons
        play_button.update(screen)
        play_button.hovering(mouse_pos)

        exit_button.update(screen)
        exit_button.hovering(mouse_pos)

        # events
        event_get = pygame.event.get()
        for event in event_get:
            if (event.type == pygame.QUIT):
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (play_button.check_for_input(mouse_pos)):
                    sound_background.stop()
                    run_game()
                elif (exit_button.check_for_input(mouse_pos)):
                    sys.exit()

        # screen update
        pygame.display.update()


def pause_menu(sound_background):
    # clear screen
    # screen.fill("black")

    # load image background
    background = pygame.image.load('menu_background.jpg')
    background = pygame.transform.scale(background, (800, 600))

    # title
    pygame.display.set_caption("Menu")

    # menu title
    menu_title = get_font(40).render("Pause", True, "green")
    menu_title_rect = menu_title.get_rect(center=(screen_size[0] / 2, 50))

    # declare buttons
    pause_button = Button(screen_size[0] / 2, 250, "Return", get_font(24), 24, "green", "white")
    menu_button = Button(screen_size[0] / 2, 300, "Menu", get_font(24), 24, "green", "white")
    exit_button = Button(screen_size[0] / 2, 350, "Exit", get_font(24), 24, "green", "white")

    is_pause = True
    while is_pause:
        # background
        screen.blit(background, (0, 0))

        # menu title
        screen.blit(menu_title, menu_title_rect)

        # mouse position
        mouse_pos = pygame.mouse.get_pos()

        # buttons
        pause_button.update(screen)
        pause_button.hovering(mouse_pos)

        exit_button.update(screen)
        exit_button.hovering(mouse_pos)

        menu_button.update(screen)
        menu_button.hovering(mouse_pos)

        # events
        event_get = pygame.event.get()
        for event in event_get:
            if (event.type == pygame.QUIT):
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (pause_button.check_for_input(mouse_pos)):
                    is_pause = False
                elif (exit_button.check_for_input(mouse_pos)):
                    sys.exit()
                elif (menu_button.check_for_input(mouse_pos)):
                    sound_background.stop()
                    main_menu()

        # screen update
        pygame.display.update()


if (__name__ == '__main__'):
    main_menu()