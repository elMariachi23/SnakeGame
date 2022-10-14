import random
import configparser
import os
from Objects.color_mapper import color_mapper
import pygame


class Snake:
    """
    Класс персонажа (Змеи)
    """
    def __init__(self):
        """
        Параметры отображения персонажа
        """
        self.conf = self.config()
        self.width = int(self.conf.get('GAME', 'resolution').split('x')[0])
        self.height = int(self.conf.get('GAME', 'resolution').split('x')[1]) - 30
        self.snake_color = color_mapper(self.conf.get('SNAKE', 'snake_color'))
        self.head_pos = [random.randrange(10, self.width - 20, 10),
                         random.randrange(10, self.height - 20, 10)]
        self.snake_body = [[self.head_pos[0], self.head_pos[1], 0]]
        self.upgraded_snake = False
        self.been_through_the_wall = False
        self.last_direction = "RIGHT"
        self.first = True
        # self.direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.direction = None
        self.dead = False

    @staticmethod
    def config():
        """
        Метод чтения параметров конфиг-файла
        :return: Объект чтения конфига
        """
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   '..', 'configuration.ini')
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def move_snake(self):
        """
        Метод движения змеи
        :return:
        """
        if self.direction == 'UP':
            if self.been_through_the_wall:
                self.been_through_the_wall = False
            else:
                self.head_pos[1] -= 10
        elif self.direction == 'DOWN':
            if self.been_through_the_wall:
                self.been_through_the_wall = False
            else:
                self.head_pos[1] += 10
        elif self.direction == 'LEFT':
            if self.been_through_the_wall:
                self.been_through_the_wall = False
            else:
                self.head_pos[0] -= 10
        elif self.direction == 'RIGHT':
            if self.been_through_the_wall:
                self.been_through_the_wall = False
            else:
                self.head_pos[0] += 10
        else:
            pass

    def snake_direction(self, new_direction):
        """
        Метод направления движения змеи
        :param new_direction: Новое направление
        :return: Перемещение змеи
        """
        if new_direction:
            if any((new_direction == "RIGHT" and self.direction != "LEFT",
                    new_direction == "LEFT" and self.direction != "RIGHT",
                    new_direction == "UP" and self.direction != "DOWN",
                    new_direction == "DOWN" and self.direction != "UP")):
                self.direction = new_direction
        self.move_snake()

    def display_snake(self, screen, food_place=None):
        """
        Отрисовка змеи
        :param screen: Место для отрисовки
        :param food_place: Место нахождения еды, при наличии
        :return: Результат успешности потребления еды
        """
        feeded = False
        self.snake_rules()
        # print(self.snake_body)
        self.snake_body.insert(0, [self.head_pos[0], self.head_pos[1], 0])
        for body in self.snake_body:
            if body[0] == food_place[0] and body[1] == food_place[1] or body[-1] == 1:
                pygame.draw.circle(screen, self.snake_color, (body[0], body[1]), 9)
            else:
                pygame.draw.circle(screen, self.snake_color, (body[0], body[1]), 6)

        if food_place:
            if self.head_pos[0] == food_place[0] and self.head_pos[1] == food_place[1]:
                # print('Поела')
                feeded = True
                self.snake_body[0][-1] = 1
            else:
                self.snake_body.pop()
        else:
            self.snake_body.pop()
        # print(self.snake_body)
        return feeded

    def snake_rules(self):
        """
        Правила жизни змеи (Столкновения)
        :return:
        """
        if self.head_pos[0] >= self.width:
            # print('Столкновение с права')
            if self.upgraded_snake:
                self.head_pos[0] -= (self.width - 10)
                self.been_through_the_wall = True
            else:
                self.dead = True
        elif self.head_pos[0] <= 0:
            # print('Столкновение с лева')
            if self.upgraded_snake:
                self.head_pos[0] += (self.width - 10)
                self.been_through_the_wall = True
            else:
                self.dead = True
        elif self.head_pos[1] >= self.height:
            # print('Столкновение с низу')
            if self.upgraded_snake:
                self.head_pos[1] = 10
                self.been_through_the_wall = True
            else:
                self.dead = True
        elif self.head_pos[1] <= 0:
            # print('Столкновение с верху')
            if self.upgraded_snake:
                self.head_pos[1] += (self.height - 10)
                self.been_through_the_wall = True
            else:
                self.dead = True
        else:
            pass

        # self.auto_pilot()
        if self.direction:
            for body_part in self.snake_body[1:]:
                if body_part[0] == self.head_pos[0] and body_part[1] == self.head_pos[1]:
                    # print('Закусили')
                    self.dead = True

    def auto_pilot(self):
        """
        Метод автопилотирования змеи, для тестирования
        :return:
        """
        # Автопилот
        if self.direction == 'DOWN':
            if not self.first:
                if self.last_direction == 'RIGHT':
                    self.direction = 'LEFT'
                    self.last_direction = 'LEFT'
                    self.first = True
                elif self.last_direction == 'LEFT':
                    self.direction = 'RIGHT'
                    self.last_direction = 'RIGHT'
                    self.first = True
                else:
                    print('BAD')
                    pass
            else:
                self.first = False
