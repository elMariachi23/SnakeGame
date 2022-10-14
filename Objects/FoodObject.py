import sys
import pygame
import random
import os
import configparser
from Objects.color_mapper import color_mapper


class SnakeFood:
    def __init__(self):
        """
        Параметры
        """
        self.conf = self.config()
        self.apple = pygame.image.load('media/apple.png')
        self.chili = pygame.image.load('media/chili.png')
        self.food_color = color_mapper(self.conf.get('FOOD', 'food_color'))
        self.width = int(self.conf.get('GAME', 'resolution').split('x')[0])
        self.height = int(self.conf.get('GAME', 'resolution').split('x')[1]) - 30
        self.food_place = None
        self.spaces = list()
        for x in range(1, self.width // 10):
            for y in range(1, self.height // 10):
                self.spaces.append([x * 10, y * 10])

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

    def empty_spaces(self, used_places):
        """
        Метод поиска пустых ячеек на поле, для отображения еды
        :param used_places: список использованных ячеек (занятых змеей)
        :return: Место для отображения еды
        """
        if len(self.spaces) <= len(used_places) - 1:
            print('Передоз')
            pygame.quit()
            sys.exit()
        else:
            empty_space = [space for space in self.spaces if space not in used_places]
            food_place = random.choice(empty_space)
            return food_place

    def display_food(self, place, chili=False):
        """
        Метод отображения еды на поле
        :param place: место для отображения ([10, 10])
        :param chili: флаг определения необходимости отобразить перец
        :return:
        """
        food = self.apple if not chili else self.chili
        place.blit(food, (self.food_place[0] - 10, self.food_place[1] - 10))

    def special_food(self, flag=False):
        if flag:
            food_color = color_mapper('Red')
        else:
            food_color = color_mapper(self.conf.get('FOOD', 'food_color'))
        return food_color
