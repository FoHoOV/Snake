import pygame

from game import SnakeGame
from game.shape.shape import SnakeBlock


class SnakeAI:

    def __init__(self):
        self.snake = SnakeGame.game_manager.snake
        self.targeted_food_block = None

    def has_target(self):
        return not (self.targeted_food_block is None)

    def create_target_if_exists(self):
        if self.targeted_food_block is None and len(SnakeGame.game_manager.state.food_blocks) > 0:
            self.targeted_food_block = SnakeGame.game_manager.state.food_blocks[0]

    def _will_hit_itself(self, next_move_block):
        for snake_block in self.snake.snake_blocks[1:]:
            if next_move_block.is_collided_with_block(snake_block):
                return True

    def move(self):
        if self.targeted_food_block and self.targeted_food_block in SnakeGame.game_manager.state.food_blocks:
            pressed_keys = []
            if self.targeted_food_block.position.x > self.snake[0].position.x:
                block = SnakeBlock(self.snake, -1, self.snake[0].position.x + self.snake[0].position.velocity,
                                   self.snake[0].position.y)
                if not self._will_hit_itself(block):
                    pressed_keys.append(pygame.K_RIGHT)
            elif self.targeted_food_block.position.x + self.targeted_food_block.width <= self.snake[0].position.x:
                block = SnakeBlock(self.snake, -1, self.snake[0].position.x - self.snake[0].position.velocity,
                                   self.snake[0].position.y)
                if not self._will_hit_itself(block):
                    pressed_keys.append(pygame.K_LEFT)
            if self.targeted_food_block.position.y > self.snake[0].position.y:
                block = SnakeBlock(self.snake, -1, self.snake[0].position.x,
                                   self.snake[0].position.y + self.snake[0].position.velocity)
                if not self._will_hit_itself(block):
                    pressed_keys.append(pygame.K_DOWN)
            elif self.targeted_food_block.position.y + self.targeted_food_block.height <= self.snake[0].position.y:
                block = SnakeBlock(self.snake, -1, self.snake[0].position.x,
                                   self.snake[0].position.y - self.snake[0].position.velocity)
                if not self._will_hit_itself(block):
                    pressed_keys.append(pygame.K_UP)

            self.snake.draw(pressed_keys)

        else:
            self.targeted_food_block = None
