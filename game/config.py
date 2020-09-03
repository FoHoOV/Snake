from game.movement.coordiantes import Direction
from game.shape.shape import Shape, SnakeShapes


class Config:
    def __init__(self):
        """created with some defaults that can be changed if desired"""
        self.WIN_WIDTH = 900
        self.WIN_HEIGHT = 900

        self.CORNERS_BLOCK_HEIGHT = Shape.get_size(Shape.CORNERS_BLOCK)[0]
        self.CORNERS_BLOCK_WIDTH = Shape.get_size(Shape.CORNERS_BLOCK)[0]

        self.INITIAL_SNAKE_LENGTH = 19
        self.MOVE_FOOD_BLOCKS=True
        self.MAX_FOOD_BLOCKS_LENGTH = 2
        self.MAX_SPEED_BLOCKS_LENGTH = 2

        self.INITIAL_DIRECTION = Direction.LEFT

        self.SNAKE_SHAPE = SnakeShapes.HORIZONTALLY

        self.FPS = 60
        self.AI = True
        self.EASY_MODE = True
