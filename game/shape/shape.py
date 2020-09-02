from threading import Timer

from game import pygame, SnakeGame
from game.movement.coordiantes import Position, Direction
from game.movement.movement import Movement
from game.state.game_state import GameState


class ShapeColors:
    RED_COLOR = (255, 0, 0)
    PINK_COLOR = (253, 10, 206)
    GREEN_COLOR = (0, 255, 0)
    BLUE_COLOR = (0, 0, 255)
    PURPLE_COLOR = (106, 10, 206)
    BLUE_PURPLE_COLOR = (80, 3, 255)
    WHITE_COLOR = (255, 255, 255)


class Size:
    def __init__(self, height, width, r=0):
        """r defaults to zero if the shape is not a circle"""
        self.height = height
        self.width = width
        self.r = r

    def is_circle(self):
        return False if self.r == 0 else True


class Shape:
    # corner 10.10 / food 15-15 / snake

    # base types
    CIRCLE = "circle"
    BLOCK = "block"

    # in order to create new types follow this convention => "shape_name + _ + base_type "

    # blocks
    SNAKE_BLOCK = 'snake_block'
    FOOD_BLOCK = 'food_block'
    SPEED_BLOCK = 'speed_block'
    CORNERS_BLOCK = 'corner_block'
    # circles
    SNAKE_CIRCLE = 'snake_circle'

    def __init__(self, type: str, color=None):

        if type.find("circle") > 0:
            self.base_type = Shape.CIRCLE

        elif type.find("block") > 0:
            self.base_type = Shape.BLOCK

        self.type = type
        if color:
            self.color = color
        else:

            if self.base_type == Shape.BLOCK:
                if type == Shape.SNAKE_BLOCK:
                    self.color = ShapeColors.PURPLE_COLOR
                elif type == Shape.FOOD_BLOCK:
                    self.color = ShapeColors.GREEN_COLOR
                elif type == Shape.SPEED_BLOCK:
                    self.color = ShapeColors.RED_COLOR
                elif type == Shape.CORNERS_BLOCK:
                    self.color = ShapeColors.WHITE_COLOR

            elif self.base_type == Shape.CIRCLE:
                if type == Shape.SNAKE_CIRCLE:
                    self.color = ShapeColors.PINK_COLOR

        if self.base_type == Shape.BLOCK:
            if type == Shape.SNAKE_BLOCK:
                self.width = 15
                self.height = 15
            elif type == Shape.FOOD_BLOCK:
                self.width = 15
                self.height = 15
            elif type == Shape.SPEED_BLOCK:
                self.width = 15
                self.height = 15
            elif type == Shape.CORNERS_BLOCK:
                self.width = 8
                self.height = 8
        elif self.base_type == Shape.CIRCLE:
            if type == Shape.SNAKE_CIRCLE:
                self.radios = 15

    def draw(self, **kwargs):
        if self.type == Shape.SNAKE_CIRCLE:
            pygame.draw.circle(SnakeGame.game_manager.window, self.color,
                               (int(kwargs['x']), int(kwargs['y'])), int(self.width / 2))
        else:
            pygame.draw.rect(SnakeGame.game_manager.window, self.color,
                             (kwargs['x'], kwargs['y'], self.width, self.height))

    @staticmethod
    def get_size_n(shape_type):
        """:returns a Size Object"""
        size = Shape.get_size(shape_type)
        if len(size) == 3:
            return Size(height=size[0], width=size[1], r=size[2])
        return Size(height=size[0], width=size[1])

    @staticmethod
    def get_size(shape_type):
        """:returns a list with following pattern: list[0]=height list[1]=width list[2]=r(if its given)"""

        # circles
        if shape_type == Shape.SNAKE_CIRCLE:
            return [15, 15, 15]

        # blocks
        if shape_type == Shape.SNAKE_BLOCK:
            return [15, 15]
        elif shape_type == Shape.FOOD_BLOCK:
            return [15, 15]
        elif shape_type == Shape.SPEED_BLOCK:
            return [15, 15]
        elif shape_type == Shape.CORNERS_BLOCK:
            return [8, 8]


class SnakeShapes:
    VERTICALLY = 'vertically'
    HORIZONTALLY = 'horizontally'

    def __init__(self, shape: str):
        self.shape = shape


class BlockPosition(Position):
    def __init__(self, x, y, velocity, direction):
        super(BlockPosition, self).__init__(x, y, velocity, direction)
        if velocity:
            self.velocity = velocity
        else:
            self.velocity = SnakeBlock.DEFAULT_VELOCITY
        self.is_jumping_horizontally = False
        self.is_jumping_vertically = False


class SnakeBlock(Shape):
    # change the parentheses at the end for changing the margin (positive values only)
    BLOCK_MARGIN = 2 * max(Shape.get_size(Shape.SNAKE_BLOCK)[0], Shape.get_size(Shape.SNAKE_BLOCK)[1])
    DEFAULT_VELOCITY = 3

    def __init__(self, snake_ref, index, x, y, direction=Direction.LEFT):
        super(SnakeBlock, self).__init__(Shape.SNAKE_BLOCK)
        self.index = index
        self.snake_ref = snake_ref
        # 3d_argument is starting_direction
        if index == 0:
            self.position = BlockPosition(x, y, SnakeBlock.DEFAULT_VELOCITY,
                                          direction)
        elif index > 0:
            self.position = BlockPosition(x, y, self.snake_ref[index - 1].position.velocity,
                                          direction)
        else:
            self.position = BlockPosition(x, y, 0,
                                          direction)
        self.positions_to_go = self.create_first_positions_to_go()

    def create_first_positions_to_go(self) -> list:
        if self.index > 0:
            next_hops = []
            last_snake = self.snake_ref[self.index - 1]
            if last_snake.position.direction == Direction.RIGHT:
                next_x_position = last_snake.position.x
                next_hops.append([
                    BlockPosition(self.position.x + self.position.velocity, self.position.y,
                                  self.position.velocity, Direction.RIGHT)])
                while next_hops[-1][0].x < next_x_position:
                    next_hops.append([
                        BlockPosition(next_hops[-1][0].x + self.position.velocity, self.position.y,
                                      self.position.velocity, Direction.RIGHT)])
            elif last_snake.position.direction == Direction.LEFT:
                next_x_position = last_snake.position.x
                next_hops.append([
                    BlockPosition(self.position.x - self.position.velocity, self.position.y,
                                  self.position.velocity, Direction.LEFT)])
                while next_hops[-1][0].x > next_x_position:
                    next_hops.append([
                        BlockPosition(next_hops[-1][0].x - self.position.velocity, self.position.y,
                                      self.position.velocity,
                                      Direction.LEFT)])
            elif last_snake.position.direction == Direction.TOP:
                next_y_position = last_snake.position.y
                next_hops.append([
                    BlockPosition(self.position.x, self.position.y - self.position.velocity,
                                  self.position.velocity, Direction.TOP)])
                while next_hops[-1][0].y > next_y_position:
                    next_hops.append([
                        BlockPosition(self.position.x, next_hops[-1][0].y - self.position.velocity,
                                      self.position.velocity, Direction.TOP)])
            elif last_snake.position.direction == Direction.BOTTOM:
                next_y_position = last_snake.position.y
                next_hops.append([
                    BlockPosition(self.position.x, self.position.y + self.position.velocity,
                                  self.position.velocity, Direction.BOTTOM)])
                while next_hops[-1][0].y < next_y_position:
                    next_hops.append([
                        BlockPosition(self.position.x, next_hops[-1][0].y + self.position.velocity,
                                      self.position.velocity,
                                      Direction.BOTTOM)])
            return next_hops
        else:
            return [None]

    def draw(self, **kwargs):
        if self.position.is_jumping_horizontally:
            super(SnakeBlock, self).draw(x=self.position.tmp_x_horizontal, y=self.position.tmp_y_horizontal)
        if self.position.is_jumping_vertically:
            super(SnakeBlock, self).draw(x=self.position.tmp_x_vertical, y=self.position.tmp_y_vertical)
        super(SnakeBlock, self).draw(x=self.position.x, y=self.position.y)
        if not SnakeGame.game_manager.state.is_paused:
            self.check_snake_state()

    def check_snake_state(self):
        speeds_to_delete = []
        foods_to_delete = []

        for food_coordinates in SnakeGame.game_manager.state.food_blocks_coordinates:
            if self.is_hit_this_block(SnakeBlock(self.snake_ref, -1, food_coordinates[0], food_coordinates[1])):
                self.snake_ref.food_blocks_eaten += 1
                foods_to_delete.append(food_coordinates)
        if len(foods_to_delete) > 0:
            SnakeGame.game_manager.state.food_blocks_coordinates = [food_block for food_block in
                                                                    SnakeGame.game_manager.state.food_blocks_coordinates
                                                                    if
                                                                    food_block not in foods_to_delete]
        for speed_coordinates in SnakeGame.game_manager.state.speed_blocks_coordinates:
            if self.is_hit_this_block(SnakeBlock(self.snake_ref, -1, speed_coordinates[0], speed_coordinates[1])):
                speeds_to_delete.append(speed_coordinates)

        if len(speeds_to_delete) > 0:
            self.snake_ref.change_snake_speed = True
            SnakeGame.game_manager.state.speed_blocks_coordinates = [speed_block for speed_block in
                                                                     SnakeGame.game_manager.state.speed_blocks_coordinates
                                                                     if
                                                                     speed_block not in speeds_to_delete]

        if self.index == len(self.snake_ref) - 1:
            if self.snake_ref.food_blocks_eaten > 0:
                last_snake = self
                # since it is a square then it doesn't matter if its whether width or height
                starting_margin = SnakeBlock.BLOCK_MARGIN + (
                        ((last_snake.width + SnakeBlock.BLOCK_MARGIN) / SnakeBlock.DEFAULT_VELOCITY)
                        * (last_snake.position.velocity - SnakeBlock.DEFAULT_VELOCITY))
                if last_snake.position.direction == Direction.TOP:
                    self.snake_ref.append(SnakeBlock(self.snake_ref, last_snake.index + 1, last_snake.position.x,
                                                     last_snake.position.y + last_snake.height + starting_margin,
                                                     last_snake.position.direction))
                elif last_snake.position.direction == Direction.BOTTOM:
                    self.snake_ref.append(SnakeBlock(self.snake_ref, last_snake.index + 1, last_snake.position.x,
                                                     last_snake.position.y - last_snake.height - starting_margin,
                                                     last_snake.position.direction))
                elif last_snake.position.direction == Direction.RIGHT:
                    self.snake_ref.append(
                        SnakeBlock(self.snake_ref, last_snake.index + 1,
                                   last_snake.position.x - last_snake.width - starting_margin,
                                   last_snake.position.y, last_snake.position.direction))
                elif last_snake.position.direction == Direction.LEFT:
                    self.snake_ref.append(
                        SnakeBlock(self.snake_ref, last_snake.index + 1,
                                   last_snake.position.x + last_snake.width + starting_margin,
                                   last_snake.position.y, last_snake.position.direction))
                self.snake_ref.food_blocks_eaten -= 1
            self.snake_ref.food_blocks_eaten = 0

            if self.snake_ref.change_snake_speed:
                self.snake_ref.change_velocity()
                self.snake_ref.change_snake_speed = False

    # to check top-right corner for exp u should say res[0]==SnakeBlock.RIGHT and res[1]=SankeBlock.TOP
    # index [0] => for LEFT or RIGHT state
    # index [1] => for TOP or BOTTOM state
    # index [2] => to indicate if its at corners or not
    def get_corners_state(self) -> list:
        result = [None, None, False]
        if self.position.y + self.height >= SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT or (
                self.position.tmp_y_vertical != 0 and
                self.position.tmp_y_vertical >= SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT) or (
                self.position.tmp_y_horizontal != 0 and
                self.position.tmp_y_horizontal >= SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT):
            result[1] = Direction.BOTTOM
            result[2] = True
        elif self.position.y <= SnakeGame.config.CORNERS_BLOCK_HEIGHT or (
                self.position.tmp_y_vertical != 0 and self.position.tmp_y_vertical <= SnakeGame.config.CORNERS_BLOCK_HEIGHT) or (
                self.position.tmp_y_horizontal != 0 and self.position.tmp_y_horizontal <= SnakeGame.config.CORNERS_BLOCK_HEIGHT):
            result[1] = Direction.TOP
            result[2] = True

        if self.position.x + self.width >= SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH or (
                self.position.tmp_x_vertical != 0 and
                self.position.tmp_x_vertical >= SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH) or (
                self.position.tmp_x_horizontal != 0 and
                self.position.tmp_x_horizontal >= SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH):
            result[0] = Direction.RIGHT
            result[2] = True
        elif self.position.x <= SnakeGame.config.CORNERS_BLOCK_WIDTH or (
                self.position.tmp_x_vertical != 0 and self.position.tmp_x_vertical <= SnakeGame.config.CORNERS_BLOCK_WIDTH) or (
                self.position.tmp_x_horizontal != 0 and self.position.tmp_x_horizontal <= SnakeGame.config.CORNERS_BLOCK_HEIGHT):
            result[0] = Direction.LEFT
            result[2] = True

        return result

    def is_hit_at_corners(self) -> bool:
        corners_state = self.get_corners_state()
        if corners_state[0] and corners_state[1]:
            return True
        return False

    def is_hit_this_block(self, snake_block) -> bool:
        result = False

        def check_equality_state(snake_block_x, self_x, snake_block_y, self_y) -> bool:
            is_x_in_between = False
            is_y_in_between = False

            if ((snake_block_x < self_x < snake_block_x + snake_block.width) or (
                    snake_block_x < self_x + self.width < snake_block_x + snake_block.width)) or (
                    self_x - snake_block_x == 0):
                is_x_in_between = True
            if ((snake_block_y < self_y < snake_block_y + snake_block.height) or (
                    snake_block_y < self_y + self.height < snake_block_y + snake_block.height)) or (
                    self_y - snake_block_y == 0):
                is_y_in_between = True

            return is_x_in_between and is_y_in_between

        if check_equality_state(snake_block.position.x, self.position.x, snake_block.position.y, self.position.y):
            result = True

        if self.position.is_jumping_horizontally and check_equality_state(snake_block.position.x,
                                                                          self.position.tmp_x_horizontal,
                                                                          snake_block.position.y,
                                                                          self.position.tmp_y_horizontal):
            result = True

        if self.position.is_jumping_vertically and check_equality_state(snake_block.position.x,
                                                                        self.position.tmp_x_vertical,
                                                                        snake_block.position.y,
                                                                        self.position.tmp_y_vertical):
            result = True

        if snake_block.position.is_jumping_horizontally and check_equality_state(snake_block.position.tmp_x_horizontal,
                                                                                 self.position.x,
                                                                                 snake_block.position.tmp_y_horizontal,
                                                                                 self.position.y):
            result = True

        if snake_block.position.is_jumping_vertically and check_equality_state(snake_block.position.tmp_x_vertical,
                                                                               self.position.x,
                                                                               snake_block.position.tmp_y_vertical,
                                                                               self.position.y):
            result = True

        if snake_block.position.is_jumping_horizontally and self.position.is_jumping_horizontally and \
                check_equality_state(snake_block.position.tmp_x_horizontal, self.position.tmp_x_horizontal
                    , snake_block.position.tmp_y_horizontal, self.position.tmp_y_horizontal):
            result = True

        if snake_block.position.is_jumping_vertically and self.position.is_jumping_vertically and check_equality_state(
                snake_block.position.tmp_x_vertical, self.position.tmp_x_vertical, snake_block.position.tmp_y_vertical,
                self.position.tmp_y_vertical):
            result = True

        return result

    def __repr__(self):
        print(
            f'x: {self.position.x}, y: {self.position.y}, vel: {self.position.velocity}, dir: {self.position.direction}'
        )

    # for debugging purposes
    def print_current_block_position(self):
        print('----tmp')
        print('tmp_x_vertical: ', self.position.tmp_x_vertical)
        print('tmp_y_vertical: ', self.position.tmp_y_vertical)
        print('tmp_x_horizontal: ', self.position.tmp_x_horizontal)
        print('tmp_y_horizontal: ', self.position.tmp_y_horizontal)
        print("----main")
        print('x: ', self.position.x)
        print('y: ', self.position.y)
        print('vel', self.position.velocity)
        print('direction: ', self.position.direction)
        print("---------------------------")


class Snake:

    def __init__(self, snake_length, initial_direction):
        self.food_blocks_eaten = 0
        self.change_snake_speed = False
        self.snake_blocks = [
            SnakeBlock(self, 0, SnakeGame.config.WIN_WIDTH / 2, SnakeGame.config.WIN_HEIGHT / 2, initial_direction)]
        self.snake_blocks[0].color = ShapeColors.BLUE_PURPLE_COLOR
        if snake_length > 1:
            if SnakeGame.config.SNAKE_SHAPE == SnakeShapes.VERTICALLY:
                if initial_direction == Direction.TOP:
                    for i in range(1, snake_length):
                        self.snake_blocks.append(
                            SnakeBlock(self, i, SnakeGame.config.WIN_WIDTH / 2,
                                       SnakeGame.config.WIN_HEIGHT / 2 + (i * Shape.get_size(Shape.SNAKE_BLOCK)[
                                           1]) + i * SnakeBlock.BLOCK_MARGIN, initial_direction))
                    else:
                        for i in range(1, snake_length):
                            self.snake_blocks.append(
                                SnakeBlock(self, i, SnakeGame.config.WIN_WIDTH / 2,
                                           SnakeGame.config.WIN_HEIGHT / 2 - (
                                                   i * Shape.get_size(Shape.SNAKE_BLOCK)[1]) -
                                           i * SnakeBlock.BLOCK_MARGIN, initial_direction))
            elif SnakeGame.config.SNAKE_SHAPE == SnakeShapes.HORIZONTALLY:
                if initial_direction == Direction.LEFT:
                    for i in range(1, snake_length):
                        self.snake_blocks.append(
                            SnakeBlock(self, i, SnakeGame.config.WIN_WIDTH / 2 + (
                                    i * Shape.get_size(Shape.SNAKE_BLOCK)[0]) + i * SnakeBlock.BLOCK_MARGIN,
                                       SnakeGame.config.WIN_HEIGHT / 2, initial_direction))
                else:
                    for i in range(1, snake_length):
                        self.snake_blocks.append(
                            SnakeBlock(self, i, SnakeGame.config.WIN_WIDTH / 2 - (
                                    i * Shape.get_size(Shape.SNAKE_BLOCK)[0]) - i * SnakeBlock.BLOCK_MARGIN,
                                       SnakeGame.config.WIN_HEIGHT / 2, initial_direction))

    def draw(self, pressed_keys, **kwargs):
        for snake_block in self.snake_blocks:
            snake_block.draw(**kwargs)
            if snake_block.index == 0:
                if snake_block.is_hit_at_corners():
                    SnakeGame.game_manager.state.set_loosing_state(GameState.HIT_CORNERS)
                if pressed_keys:
                    for pressed_key in pressed_keys:
                        if pressed_key == pygame.K_RIGHT:
                            self.update_block_position(snake_block,
                                                       snake_block.position.velocity, True)
                        if pressed_key == pygame.K_LEFT:
                            self.update_block_position(snake_block,
                                                       -snake_block.position.velocity, True)
                        if pressed_key == pygame.K_UP:
                            self.update_block_position(snake_block,
                                                       -snake_block.position.velocity, False)
                        if pressed_key == pygame.K_DOWN:
                            self.update_block_position(snake_block,
                                                       snake_block.position.velocity, False)
                else:
                    if snake_block.position.direction == Direction.TOP:
                        self.update_block_position(snake_block,
                                                   -snake_block.position.velocity, False)
                    elif snake_block.position.direction == Direction.BOTTOM:
                        self.update_block_position(snake_block, snake_block.position.velocity,
                                                   False)
                    elif snake_block.position.direction == Direction.RIGHT:
                        self.update_block_position(snake_block, snake_block.position.velocity,
                                                   True)
                    elif snake_block.position.direction == Direction.LEFT:
                        self.update_block_position(snake_block,
                                                   -snake_block.position.velocity, True)
            else:
                if snake_block.is_hit_this_block(self.snake_blocks[0]):
                    SnakeGame.game_manager.state.set_loosing_state(GameState.HIT_IT_SELF)
                for position in snake_block.positions_to_go[0]:
                    if position.direction == Direction.TOP:
                        self.update_block_position(snake_block, -position.velocity, False)
                    elif position.direction == Direction.BOTTOM:
                        self.update_block_position(snake_block, position.velocity, False)
                    elif position.direction == Direction.RIGHT:
                        self.update_block_position(snake_block, position.velocity, True)
                    elif position.direction == Direction.LEFT:
                        self.update_block_position(snake_block, -position.velocity, True)
                del snake_block.positions_to_go[0]
            if snake_block.index + 1 < len(self.snake_blocks):
                if not self.snake_blocks[snake_block.index + 1].positions_to_go[-1]:
                    del self.snake_blocks[snake_block.index + 1].positions_to_go[-1]

    def change_velocity(self, time_limit: int = 15):

        def reset_velocity():
            self[0].position.velocity = SnakeBlock.DEFAULT_VELOCITY

        self[0].position.velocity += 1
        # TODO: change this handler to be local to every Snake class
        if SnakeGame.game_manager.handler:
            if SnakeGame.game_manager.handler.is_alive():
                SnakeGame.game_manager.handler.cancel()
        SnakeGame.game_manager.handler = Timer(time_limit, reset_velocity)
        SnakeGame.game_manager.handler.start()

    def update_block_position(self, snake_block, changing_value, is_horizontal):
        Movement.update_position(Shape.SNAKE_BLOCK, snake_block.position, changing_value, is_horizontal)
        if snake_block.index + 1 < len(self.snake_blocks) and len(self.snake_blocks) > 1:
            next_snake = self.snake_blocks[snake_block.index + 1]
            if next_snake.positions_to_go[-1]:
                next_snake.positions_to_go.append(
                    [BlockPosition(snake_block.position.x, snake_block.position.y, snake_block.position.velocity,
                                   snake_block.position.direction)])
                # this None is because to be sure that we are adding elements into the same index
                next_snake.positions_to_go.append(None)
            else:
                next_snake.positions_to_go[-2].append(
                    BlockPosition(snake_block.position.x, snake_block.position.y, snake_block.position.velocity,
                                  snake_block.position.direction))

    def append(self, snake_block: SnakeBlock):
        self.snake_blocks.append(snake_block)

    def __getitem__(self, item):
        return self.snake_blocks[item]

    def __len__(self):
        return len(self.snake_blocks)
