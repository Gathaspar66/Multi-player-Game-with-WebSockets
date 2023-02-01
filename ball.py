import pygame

from MultiGame import configuration


class Ball:

    def __init__(self):
        logo = pygame.image.load("ball.png")
        self.square = logo.get_rect()
        self.a = 1
        self.b = 1
        self.speed = 5

    def movement(self):
        if self.square.left < 0:
            self.a = -self.a

        if self.square.right > configuration.width:
            self.a = -self.a

        if self.square.top < 0:
            self.b = -self.b

        if self.square.bottom > configuration.height:
            self.b = -self.b

        self.square.left = self.square.left + self.a * self.speed
        self.square.top = self.square.top + self.b * self.speed

        return self.square.left, self.square.top

    def check_collision(self, data, ball_pos):

        if (ball_pos[0] > data['position'][0] and ball_pos[0] < data['position'][0] + 11) and \
                (ball_pos[1] > data['position'][1] and ball_pos[1] < data['position'][1] + 100):
            self.a = -self.a
            self.square.left = self.square.left + self.a * self.speed
            self.square.top = self.square.top + self.b * self.speed
