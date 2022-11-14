import random
from Objects.GameDisign import GameSurface
from Objects.SnakeObject import Snake
from Objects.FoodObject import SnakeFood
from Objects.color_mapper import color_mapper


def game_play():
    food = meat.empty_spaces(snake.snake_body)
    target = meat.food_place = food
    special_food = False
    while True:
        game.play = not snake.dead if not game.welcome else False
        new_direction = game.controls()
        if new_direction == 'RERUN':
            game.__init__()
            snake.__init__()
        elif new_direction == 'PAUSE':
            while not game.controls():
                game.play = False
                game.pause = True
                game.run()
        else:
            if game.play:
                meat.food_color = meat.special_food(special_food)
                meat.display_food(game.screen, special_food)
                snake.snake_direction(new_direction)
                if snake.display_snake(game.screen, target):
                    if special_food:
                        game.pepper += 1
                        game.game_speed += 5
                        snake.upgraded_snake = True
                        snake.snake_color = color_mapper('red')
                    else:
                        game.apple += 1
                        if snake.upgraded_snake:
                            game.game_speed = 10
                            snake.upgraded_snake = False
                            snake.snake_color = snake.default_snake_color
                    target = meat.empty_spaces(snake.snake_body)
                    meat.food_place = target
                    special_food = random.choice([True, False, False, False])
            else:
                if snake.dead:
                    game.pause = False
        game.run()


if __name__ == '__main__':
    game = GameSurface()
    snake = Snake()
    meat = SnakeFood()
    game_play()
