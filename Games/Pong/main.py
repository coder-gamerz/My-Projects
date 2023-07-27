import pygame
import pandas as pd
import matplotlib.pyplot as plt
from sys import exit
from random import uniform, choice, randint
from math import cos, sin, radians
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import sys

RESOLUTION = (1280, 720)
WIDTH, HEIGHT = RESOLUTION


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 20, 20)

        self.ball_speed = 500
        self.ball_direction = 45
        self.collision_timer = 180

    def degreecorrect(self):
        while self.ball_direction >= 360:
            self.ball_direction -= 360

        while self.ball_direction <= 0:
            self.ball_direction += 360

    def move(self, deltatime):
        self.ball.x += cos(radians(self.ball_direction)) * (self.ball_speed * deltatime)
        self.ball.y += sin(radians(self.ball_direction)) * (self.ball_speed * deltatime)

        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_direction *= -1
            if self.ball_direction == 0:
                self.ball_direction += 20

            elif self.ball_direction == 180:
                self.ball_direction -= 20

            elif self.ball_direction == 90 or self.ball_direction == 270:
                self.ball_direction += choice([-20, 20])

            self.degreecorrect()

        if self.ball.left <= 0:
            self.points_player += 1
            self.ball.x = WIDTH / 2 - 15
            self.ball.y = HEIGHT / 2 - 15
            self.ball_direction = 45
            self.ball_speed = 500

        elif self.ball.right >= WIDTH:
            self.points_AI += 1
            self.ball.x = WIDTH / 2 - 15
            self.ball.y = HEIGHT / 2 - 15
            self.ball_direction = 45
            self.ball_speed = 500

    def collide_detect(self, player, AI):
        if self.collision_timer <= 0:
            if self.ball.colliderect(player):
                if player.centery > 25 < self.ball.centery < player.centery + 25:
                    self.ball_direction = self.ball_direction * -1 - 180
                    self.degreecorrect()
                    print("middle")
                elif self.ball.centery < player.centery - 25:
                    self.ball_direction = self.ball_direction * -1 - 180
                    self.degreecorrect()
                    self.ball_direction = round(uniform(self.ball_direction, 250))
                    round(self.ball_direction)
                    print("top")
                elif self.ball.centery > player.centery + 25:
                    self.ball_direction = self.ball_direction * -1 - 180
                    self.degreecorrect()
                    self.ball_direction = round(uniform(self.ball_direction, 110))
                    print("bottom")

                self.collision_timer = 180
                self.ball_speed += 20
                print("new angle: " + str(self.ball_direction))

            elif self.ball.colliderect(AI):
                if AI.centery > 25 < self.ball.centery < AI.centery + 25:
                    self.ball_direction = self.ball_direction * -1 - 180
                    self.degreecorrect()
                    print("middle")
                elif self.ball.centery < AI.centery - 25:
                    self.ball_direction = self.ball_direction * -1 - 180
                    self.degreecorrect()
                    self.ball_direction = round(uniform(self.ball_direction, 290))
                    print("top")
                elif self.ball.centery > AI.centery + 25:
                    self.ball_direction = self.ball_direction * -1 - 180
                    self.degreecorrect()
                    if 360 >= self.ball_direction >= 270:
                        self.ball_direction = round(uniform(self.ball_direction, 430))
                    elif 0 <= self.ball_direction <= 90:
                        self.ball_direction = round(uniform(self.ball_direction, 70))
                    self.degreecorrect()
                    print("bottom")

                self.collision_timer = 180
                self.ball_speed += 20
                print("new angle: " + str(self.ball_direction))
        else:
            self.collision_timer -= 1

    def return_pos(self):
        return self.ball.centery, self.ball.centerx

    def return_direction(self):
        return self.ball_direction


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player = pygame.Rect(WIDTH - 50, HEIGHT / 2 - 70, 20, 150)
        self.player_speed = 0

    def move(self, deltatime):
        self.player.y += (self.player_speed * deltatime)

        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= HEIGHT:
            self.player.bottom = HEIGHT


class AI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.AI = pygame.Rect(30, HEIGHT / 2 - 70, 20, 150)
        self.AI_speed = 360

        self.prediction = None

        self.training_data = [[50, 150], [400, 200], [100, 110], [210, 190]]

        self.target_values = [1, 0, 1, 0]

        self.model = LogisticRegression()
        self.model.fit(preprocessing.normalize(self.training_data), self.target_values)

        # show diagramm of maschine learning
        # self._visualize_data_relationship()

    def move(self, ball, deltatime):
        self.prediction = self.model.predict(preprocessing.normalize([[self.AI.centery, ball.centery]]))

        if self.prediction == 0:
            self.move_up(deltatime)

        elif self.prediction == 1:
            self.move_down(deltatime)

    def move_up(self, deltatime):
        if self.AI.top >= 0:
            self.AI.centery -= (self.AI_speed * deltatime)

    def move_down(self, deltatime):
        if self.AI.bottom <= HEIGHT:
            self.AI.centery += (self.AI_speed * deltatime)

    def _visualize_data_relationship(self):
        random_inputs = []
        predictions = []

        for _ in range(0, 1000):
            y_paddle = randint(1, 300)
            y_ball = randint(1, 300)
            random_inputs.append([y_paddle, y_ball])

            predictions.append(self.model.predict([[y_paddle, y_ball]]))

        df = pd.DataFrame(random_inputs, columns=['y_center_paddle', 'y_center_ball'])
        df['action'] = predictions

        ax1 = df[df['action'] == 0].plot(kind='scatter', x='y_center_paddle', y='y_center_ball', s=100, color='blue')
        df[df['action'] == 1].plot(kind='scatter', x='y_center_paddle', y='y_center_ball', s=100, color='magenta',
                                   ax=ax1)

        plt.legend(labels=['Move UP', 'Move DOWN'])

        plt.title('Relationship between Y position of paddle center and Y position of ball center', size=24)
        plt.xlabel('Y position of paddle center', size=18)
        plt.ylabel('Y position of ball center', size=18)

        plt.show()


class Main(Player, Ball, AI):
    def __init__(self):
        super().__init__()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.light_grey = (200, 200, 200)
        self.background_color = (40, 40, 40)

        pygame.init()

        self.FPS = 170
        self.deltatime = 1 / self.FPS

        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Pong")
        self.icon = pygame.image.load("icon.png")
        pygame.display.set_icon(self.icon)

        background = pygame.Surface(self.screen.get_size())
        background.convert()
        background.fill(self.background_color)

        self.points_AI = 0
        self.points_player = 0
        self.score = None

        self.font = pygame.font.SysFont(None, 100)

        self.clock = pygame.time.Clock()

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player_speed -= 360
                    if event.key == pygame.K_DOWN:
                        self.player_speed += 360
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player_speed += 360
                    if event.key == pygame.K_DOWN:
                        self.player_speed -= 360

            self.score = self.font.render("{:<20}".format(str(self.points_AI)) + str(self.points_player), True,
                                          self.WHITE)

            self.screen.fill(self.background_color)
            self.screen.blit(self.score, (WIDTH / 2 - self.score.get_width() / 2, 10))

            pygame.draw.aaline(self.screen, self.light_grey, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
            pygame.draw.rect(self.screen, self.WHITE, self.player)
            pygame.draw.ellipse(self.screen, self.RED, self.ball)
            pygame.draw.rect(self.screen, self.WHITE, self.AI)

            pygame.display.flip()

            Player.move(self, self.deltatime)
            Ball.move(self, self.deltatime)
            AI.move(self, self.ball, self.deltatime)

            Ball.collide_detect(self, self.player, self.AI)

            self.clock.tick(self.FPS)

            if self.points_AI == 10:
                print('AI won!')
                sys.exit(0)

            if self.points_player == 10:
                print('You won!')
                sys.exit(0)

class Menu(object):
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.background_color = (40, 40, 40)

        pygame.init()

        self.run_menu = True

        self.cursor_pos = None

        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Pong")
        self.icon = pygame.image.load("icon.png")
        pygame.display.set_icon(self.icon)

        background = pygame.Surface(self.screen.get_size())
        background.convert()
        background.fill(self.background_color)

        self.clock = pygame.time.Clock()

        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

        self.font = pygame.font.SysFont(None, 50)

        self.logo = pygame.image.load("Pong_logo.png")

        self.text_start = self.font.render("Start Game", True, self.WHITE)

        self.logo_rect = self.logo.get_rect()
        self.start_rect = self.text_start.get_rect()

        self.logo_rect.centerx = WIDTH / 2
        self.logo_rect.centery = HEIGHT / 2 - 100

        self.start_rect.centerx = WIDTH / 2
        self.start_rect.centery = HEIGHT - 150

    def check_cursor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                self.cursor_pos = pygame.mouse.get_pos()
                self.check_input()

    def runmenu(self):
        while self.run_menu is True:
            self.check_cursor()
            self.screen.fill(self.background_color)

            self.screen.blit(self.logo, self.logo_rect)
            self.screen.blit(self.text_start, self.start_rect)

            pygame.display.flip()

    def check_input(self):
        if self.start_rect.collidepoint(self.cursor_pos):
            self.run_menu = False
            main = Main()
            main.run()


if __name__ == '__main__':
    menu = Menu()
    menu.runmenu()
