from random import randint

from game import SnakeGame


class Position:
    DEFAULT_VELOCITY = 1

    def __init__(self, x, y, velocity, direction):
        self.x = x
        self.y = y
        self.direction = direction

        if velocity:
            self.velocity = velocity
        else:
            self.velocity = Position.DEFAULT_VELOCITY
        # tmp values are for if the block is at corners so it should have two blocks to show at the same time
        # one for the left corner and the other one for the right corner{horizontal} (or top and bottom{vertical})
        self.tmp_x_vertical = 0
        self.tmp_y_vertical = 0
        self.tmp_x_horizontal = 0
        self.tmp_y_horizontal = 0
        self.is_jumping_horizontally = False
        self.is_jumping_vertically = False

    @staticmethod
    def random_position_generator() -> list:
        return [randint(0, SnakeGame.config.WIN_WIDTH), randint(0, SnakeGame.config.WIN_HEIGHT)]

    def __repr__(self):
        return f'x: {self.x}, y:{self.y},vel: {self.velocity} ,dir: {self.direction}'


class Direction:
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'
    FIXED = 'fixed'
