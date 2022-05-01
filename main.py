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

# clock
clk = pygame.time.Clock()

# game sounds
sound_shoot = mixer.Sound('shoot.wav')
sound_explosion = mixer.Sound('explosion.wav')


# player object
class Player:
    def __init__(self, path_image):
        self.image = pygame.image.load(path_image)
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

    # keep inside the screen
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

    # event get keys to move
    def move_event_get(self, events, key_left, key_right, key_up, key_down):
        for event in events:
            if (event.type == pygame.KEYDOWN):
                if (event.key == key_right):
                    self.speed_x = self.general_speed
                elif (event.key == key_left):
                    self.speed_x = -self.general_speed
                elif (event.key == key_up):
                    self.speed_y = -self.general_speed
                elif (event.key == key_down):
                    self.speed_y = self.general_speed
            elif (event.type == pygame.KEYUP):
                if (event.key == key_left):
                    self.speed_x = 0
                elif (event.key == key_right):
                    self.speed_x = 0
                elif (event.key == key_up):
                    self.speed_y = 0
                elif (event.key == key_down):
                    self.speed_y = 0

    # when the player dies
    def reset(self):
        self.x = random.randint(0, 800) // 8 * 8
        self.y = 25

        self.speed_x = 0
        self.speed_y = 0
        self.general_speed = 8

    # nickname
    def put_nickname(self, nick):
        self.nickname = get_font(8).render(nick, True, "green")
        self.dest_nickname = self.nickname.get_rect(center=(self.x + 32, self.y))
        screen.blit(self.nickname, self.dest_nickname)


# enemy bullet object
class Enemy_bullet:
    def __init__(self):
        self.image = pygame.image.load('game_enemy_bullet.png')
        self.x = 0
        self.y = 0
        self.size = 64

        self.speed = 20
        self.state = "ready"

    # move and set the bullet state = "ready"
    def move(self):
        if (self.y <= 0 - self.size):
            self.state = "ready"
        elif (self.state == "fire"):
            self.y -= self.speed

    # draw the bullet and fire the bullet
    def draw_and_fire(self, enemy_x, enemy_y):
        if (self.state == "ready"):
            self.state = "fire"
            self.x = enemy_x
            self.y = enemy_y - 75  # 75 - distance for enemy
            screen.blit(self.image, (self.x, self.y))
            sound_shoot.play()
        else:
            screen.blit(self.image, (self.x, self.y))


# enemy object
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('game_enemy.png')
        self.x = x
        self.y = y

        self.speed = 4

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    # follow the player
    def move(self, player_x):
        if (self.x < player_x):
            self.x += self.speed
        elif (self.x > player_x):
            self.x -= self.speed

    # when the enemy is destroyed
    def reset(self):
        self.x = random.randint(0, 800) // 8 * 8
        self.y = 500

        self.speed = 4


# game events object
class Game_events:
    def __init__(self):
        self.collision_constant = 45  # maximum distance between two objects to consider as collisions

    def is_collision(self, obj1_x, obj1_y, obj2_x, obj2_y):
        distance = math.sqrt(math.pow(obj1_x - obj2_x, 2) + math.pow(obj1_y - obj2_y, 2))

        if (distance <= self.collision_constant):
            return True
        else:
            return False

    # collision between player and enemy bullet
    def collision_players_enemy_bullet(self, score, player1, player2, enemy1, enemy2, enemy_bullet1, enemy_bullet2,
                                      obj1_x, obj1_y, obj2_x, obj2_y):
        if (self.is_collision(obj1_x, obj1_y, obj2_x, obj2_y)):
            enemy_bullet1.state = "ready"
            enemy_bullet2.state = "ready"
            score.value = 0

            player1.reset()
            player2.reset()

            enemy1.reset()
            enemy2.reset()

            sound_explosion.play()

    # collision between player and enemy
    def collision_players_enemy(self, score, player1, player2, enemy1, enemy2, enemy_bullet1, enemy_bullet2, obj1_x,
                               obj1_y, obj2_x, obj2_y):
        if (self.is_collision(obj1_x, obj1_y, obj2_x, obj2_y)):
            enemy_bullet1.state = "ready"
            enemy_bullet2.state = "ready"
            score.value += 1

            player1.reset()
            player2.reset()

            enemy1.reset()
            enemy2.reset()

            sound_explosion.play()

    def collision_player_enemy_bullet(self, score, player, enemy, enemy_bullet, obj1_x, obj1_y, obj2_x, obj2_y):
        if (self.is_collision(obj1_x, obj1_y, obj2_x, obj2_y)):
            enemy_bullet.state = "ready"
            score.value = 0
            player.reset()
            enemy.reset()
            sound_explosion.play()

        # collision between player and enemy

    def collision_player_enemy(self, score, player, enemy, enemy_bullet, obj1_x, obj1_y, obj2_x, obj2_y):
        if (self.is_collision(obj1_x, obj1_y, obj2_x, obj2_y)):
            enemy_bullet.state = "ready"
            score.value += 1
            player.reset()
            enemy.reset()
            sound_explosion.play()


# score object
class Score:
    def __init__(self):
        self.value = 0
        self.font = get_font(16)

        self.x = 10
        self.y = 10

    def draw(self):
        self.score = self.font.render("Score: " + str(self.value), True, "white")
        screen.blit(self.score, (self.x, self.y))


# game font
def get_font(size):
    return pygame.font.Font('font.ttf', size)


# game screens
def one_player_game():
    # load image background
    background = pygame.image.load('game_background.png')

    # title
    pygame.display.set_caption("Space Invanders: The other side")

    # load sounds and play background music
    sound_background = mixer.Sound('background.wav')
    sound_background.play(-1)

    # declare obj
    pause_button = Button(screen_size[0] - 120, 30, "Pause", get_font(16), 16, "green", "white")
    player = Player('game_player1.png')
    enemy = Enemy(400, 500)
    enemy_bullet = Enemy_bullet()
    game_events = Game_events()
    score = Score()

    # game loop
    while True:
        # game rules
        player.move()
        player.keep_inside(screen)

        enemy.move(player.x)
        enemy_bullet.move()
        enemy_bullet.draw_and_fire(enemy.x, enemy.y)

        game_events.collision_player_enemy_bullet(score, player, enemy, enemy_bullet, player.x, player.y,
                                                  enemy_bullet.x, enemy_bullet.y)
        game_events.collision_player_enemy(score, player, enemy, enemy_bullet, player.x, player.y, enemy.x, enemy.y)

        # mouse position
        mouse_position = pygame.mouse.get_pos()

        # draw
        player.draw()
        player.put_nickname("Player")
        enemy.draw()
        score.draw()
        pause_button.update(screen)
        pause_button.hovering(mouse_position)

        # events
        event_get = pygame.event.get()
        player.move_event_get(event_get, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)

        for event in event_get:
            if (event.type == pygame.QUIT):
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (pause_button.check_for_input(mouse_position)):
                    pause_menu(sound_background)

        # screen update
        clk.tick(30)
        pygame.display.update()
        screen.blit(background, (0, 0))


def two_player_game():
    # load image background
    background = pygame.image.load('game_background.png')

    # title
    pygame.display.set_caption("Space Invanders: The other side")

    # load sounds and play background music
    sound_background = mixer.Sound('background.wav')
    sound_background.play(-1)

    # declare obj
    pause_button = Button(screen_size[0] - 120, 30, "Pause", get_font(16), 16, "green", "white")
    player1 = Player("game_player1.png")
    player2 = Player("game_player2.png")
    enemy1 = Enemy(200, 500)
    enemy2 = Enemy(600, 500)
    enemy1_bullet = Enemy_bullet()
    enemy2_bullet = Enemy_bullet()
    game_events = Game_events()
    score = Score()

    # game loop
    while True:
        # game rules
        player1.move()
        player1.keep_inside(screen)

        player2.move()
        player2.keep_inside(screen)

        enemy1.move(player1.x)
        enemy1_bullet.move()
        enemy1_bullet.draw_and_fire(enemy1.x, enemy1.y)

        enemy2.move(player2.x)
        enemy2_bullet.move()
        enemy2_bullet.draw_and_fire(enemy2.x, enemy2.y)

        # self, score, player1, player2, enemy1, enemy2, enemy_bullet1, enemy_bullet2, obj1_x, obj1_y, obj2_x, obj2_y
        game_events.collision_players_enemy_bullet(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                                  player1.x, player1.y, enemy1_bullet.x, enemy1_bullet.y)
        game_events.collision_players_enemy_bullet(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                                  player1.x, player1.y, enemy2_bullet.x, enemy2_bullet.y)
        game_events.collision_players_enemy(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                           player1.x, player1.y, enemy1.x, enemy1.y)
        game_events.collision_players_enemy(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                           player1.x, player1.y, enemy2.x, enemy2.y)

        game_events.collision_players_enemy_bullet(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                                  player2.x, player2.y, enemy1_bullet.x, enemy1_bullet.y)
        game_events.collision_players_enemy_bullet(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                                  player2.x, player2.y, enemy2_bullet.x, enemy2_bullet.y)
        game_events.collision_players_enemy(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                           player2.x, player2.y, enemy1.x, enemy1.y)
        game_events.collision_players_enemy(score, player1, player2, enemy1, enemy2, enemy1_bullet, enemy2_bullet,
                                           player2.x, player2.y, enemy2.x, enemy2.y)

        # mouse postion
        mouse_position = pygame.mouse.get_pos()

        # draw
        player1.draw()
        player2.draw()

        player1.put_nickname("Player 1")
        player2.put_nickname("Player 2")

        enemy1.draw()
        enemy2.draw()

        score.draw()

        pause_button.update(screen)
        pause_button.hovering(mouse_position)

        # events
        event_get = pygame.event.get()
        player1.move_event_get(event_get, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        player2.move_event_get(event_get, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

        for event in event_get:
            if (event.type == pygame.QUIT):
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (pause_button.check_for_input(mouse_position)):
                    pause_menu(sound_background)

        # screen update
        clk.tick(30)
        pygame.display.update()
        screen.blit(background, (0, 0))


def main_menu():
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
    one_player_button = Button(screen_size[0] / 2, 250, "1 Player", get_font(24), 24, "green", "white")
    two_player_button = Button(screen_size[0] / 2, 300, "2 players", get_font(24), 24, "green", "white")
    exit_button = Button(screen_size[0] / 2, 350, "Exit", get_font(24), 24, "green", "white")

    while True:
        # background
        screen.blit(background, (0, 0))

        # draw title game
        screen.blit(menu_title_p1, menu_title_p1_rect)
        screen.blit(menu_title_p2, menu_title_p2_rect)

        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # buttons events
        one_player_button.update(screen)
        one_player_button.hovering(mouse_pos)

        two_player_button.update(screen)
        two_player_button.hovering(mouse_pos)

        exit_button.update(screen)
        exit_button.hovering(mouse_pos)
        # events menu
        event_get = pygame.event.get()
        for event in event_get:
            if (event.type == pygame.QUIT):
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (one_player_button.check_for_input(mouse_pos)):
                    sound_background.stop()
                    one_player_game()
                elif (two_player_button.check_for_input(mouse_pos)):
                    sound_background.stop()
                    two_player_game()
                elif (exit_button.check_for_input(mouse_pos)):
                    sys.exit()

        # screen update
        clk.tick(30)
        pygame.display.update()


def pause_menu(sound_background):
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

        # draw menu title
        screen.blit(menu_title, menu_title_rect)

        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # buttons events
        pause_button.update(screen)
        pause_button.hovering(mouse_pos)

        exit_button.update(screen)
        exit_button.hovering(mouse_pos)

        menu_button.update(screen)
        menu_button.hovering(mouse_pos)

        # events pause menu
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
        clk.tick(30)
        pygame.display.update()


if (__name__ == '__main__'):
    main_menu()
