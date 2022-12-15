import configparser
import os
import sys

import pygame

from Objects.color_mapper import color_mapper


class GameSurface:
    """
    Класс игрового окружения
    """
    def __init__(self):
        """
        Метод получения параметров игры и создания необходимых настроек
        """
        self.conf = self.config()
        self.width = int(self.conf.get('GAME', 'resolution').split('x')[0])
        self.height = int(self.conf.get('GAME', 'resolution').split('x')[1])
        self.welcome = True
        self.play = False
        self.pause = False
        pygame.init()
        pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SNAKE")
        self.game_time = pygame.time.Clock()
        self.apple = 0
        self.pepper = 0
        self.score_text = pygame.font.Font(None, 24)
        self.game_over_text = pygame.font.Font(None, 46)
        self.game_speed = int(self.conf.get('GAME', 'fps'))
        self.mouse = pygame.mouse.get_pos()

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

    def run(self):
        """
        Метод обновления экрана/смены кадра
        :return:
        """
        if self.play:
            self.show_score()
        elif self.welcome:
            self.welcome_screen()
        elif self.pause:
            self.pause_screen()
        else:
            self.game_over()
        pygame.display.flip()
        self.game_time.tick(self.game_speed)
        self.screen.fill(color_mapper(self.conf.get('GAME', 'background_color')))

    def show_score(self):
        """
        Отображения текста информации (Кол-во очков)
        :return:
        """
        score = 'Съедено: яблок {} и перцев {}, Скорость: {}fps'.format(str(self.apple), str(self.pepper),
                                                                        str(self.game_speed))
        self.screen.blit(self.score_text.render(score, 1,
                                                color_mapper(self.conf.get('GAME', 'info_text_color'))),
                                               (10, self.height - 20))
        pygame.draw.line(self.screen, color_mapper(self.conf.get('GAME', 'info_text_color')),
                         (0, self.height - 30), (self.width, self.height - 30), 3)

    def game_over(self):
        """
        Метод отображения окна завершения
        :return:
        """
        text = 'Поражение :( Нажмите "R" для рестарта'
        score = 'Счет: {}'.format(str(self.apple + self.pepper))
        self.screen.blit(self.game_over_text.render(text, 1,
                                                    color_mapper(self.conf.get('GAME', 'info_text_color'))),
                         (40, self.height // 2))
        self.screen.blit(self.score_text.render(score, 1,
                                                color_mapper('green')),
                         ((self.width // 2) - 40, (self.height // 2) + 40))

    def welcome_screen(self):
        """
        Экран приветствия
        :return:
        """
        welcome_text = 'Привет! Начнем?!'
        center_width = (self.width // 2) - 150
        center_height = (self.height // 2) - 25
        if center_height >= 0 and center_width >= 0:
            button = pygame.rect.Rect(center_width, center_height, 300, 50)
        else:
            button = pygame.rect.Rect(10, 100, 300, 50)

        button_color = color_mapper(self.conf.get('GAME', 'info_text_color')) \
            if not button.collidepoint(pygame.mouse.get_pos()) else color_mapper('White')
        pygame.draw.rect(self.screen, button_color,
                         button, 5)
        self.screen.blit(self.game_over_text.render(welcome_text, 1, button_color),
                         (button.x + 15, button.y + 10))

        if button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (1, 0, 0):
            self.welcome = False
            self.play = True

    def pause_screen(self):
        """
        Экран паузы
        :return:
        """
        pause_text = "Пауза"
        info = 'Счет {}; Скорость {}'.format(str(self.apple + self.pepper), self.game_speed)
        pause_text = self.game_over_text.render(pause_text, 1, color_mapper(self.conf.get('GAME', 'info_text_color')))
        info = self.score_text.render(info, 1, color_mapper(self.conf.get('GAME', 'info_text_color')))
        continue_text = self.score_text.render('Чтобы продолжить нажмите любую клавишу или ESC для выхода', 1,
                                               color_mapper(self.conf.get('GAME', 'info_text_color')))
        self.screen.blit(pause_text, ((self.width // 2) - (pause_text.get_size()[0] // 2), self.height // 2))
        self.screen.blit(info, ((self.width // 2) - (info.get_size()[0] // 2), (self.height // 2) + 40))
        self.screen.blit(continue_text, ((self.width // 2) - (continue_text.get_size()[0] // 2),
                                         (self.height // 2) + 60))

    @staticmethod
    def controls():
        """
        Метод получения нажатия клавиш во время игры
        :return: Направление движения, в зависимости от нажатия клавиши
        """
        change_direction = None
        for action in pygame.event.get():

            if action.type == pygame.KEYDOWN:
                if action.key == pygame.K_RIGHT:
                    change_direction = "RIGHT"
                elif action.key == pygame.K_LEFT:
                    change_direction = "LEFT"
                elif action.key == pygame.K_UP:
                    change_direction = "UP"
                elif action.key == pygame.K_DOWN:
                    change_direction = "DOWN"
                elif action.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif action.key == pygame.K_r:
                    change_direction = 'RERUN'
                elif action.key == pygame.K_p:
                    change_direction = 'PAUSE'
            elif action.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif action.type == pygame.MOUSEBUTTONDOWN:
                # print('CLICK: {}'.format(pygame.mouse.get_pos()))
                pass
            else:
                pass
        return change_direction
