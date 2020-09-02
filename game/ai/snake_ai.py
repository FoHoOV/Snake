from random import randint

import pygame

from game import SnakeGame


class SnakeAI:

    def __init__(self):
        self.snake = SnakeGame.game_manager.snake
        self.targeted_food_block = None

    def move(self):
        if self.targeted_food_block == None and len(SnakeGame.game_manager.state.food_blocks) > 0:
            self.targeted_food_block = SnakeGame.game_manager.state.food_blocks[0]
        if self.targeted_food_block and self.targeted_food_block in SnakeGame.game_manager.state.food_blocks:
            pressed_keys = []
            if self.targeted_food_block.position.x > self.snake[0].position.x:
                pressed_keys.append(pygame.K_RIGHT)
            elif self.targeted_food_block.position.x != self.snake[0].position.x:
                pressed_keys.append(pygame.K_LEFT)
            if self.targeted_food_block.position.y > self.snake[0].position.y:
                pressed_keys.append(pygame.K_DOWN)
            elif self.targeted_food_block.position.y != self.snake[0].position.y:
                pressed_keys.append(pygame.K_UP)

            self.snake.draw(pressed_keys)

        else:
            self.targeted_food_block = None
