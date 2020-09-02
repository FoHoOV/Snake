from game import SnakeGame
from game.movement.coordiantes import Direction


class Movement:

    @staticmethod
    def reset_tmp_horizontal_values(position):
        position.tmp_x_horizontal = 0
        position.tmp_y_horizontal = 0
        position.is_jumping_horizontally = False

    @staticmethod
    def reset_tmp_vertical_values(position):
        position.tmp_x_vertical = 0
        position.tmp_y_vertical = 0
        position.is_jumping_vertically = False

    @classmethod
    def update_x(cls, shape_type, position, value: int, is_vertical: bool):
        from game.shape.shape import Shape
        if is_vertical:  # indicates that the block is moving vertically
            if position.is_jumping_horizontally:
                position.tmp_y_horizontal = position.tmp_y_horizontal + value
                if position.tmp_y_horizontal > SnakeGame.config.WIN_HEIGHT:
                    position.tmp_y_horizontal = value
                elif position.tmp_y_horizontal < 0:
                    position.tmp_y_horizontal = SnakeGame.config.WIN_HEIGHT + value
        else:
            position.x = position.x + value
            if value > 0:
                cls.update_direction(position, Direction.RIGHT)
            else:
                cls.update_direction(position, Direction.LEFT)
            if position.x + Shape.get_size_n(shape_type).width > SnakeGame.config.WIN_WIDTH:  # right corner
                if not position.is_jumping_horizontally:
                    position.is_jumping_horizontally = True
                    position.tmp_x_horizontal = position.x - SnakeGame.config.WIN_WIDTH
                    position.tmp_y_horizontal = position.y
                else:
                    position.tmp_x_horizontal = position.tmp_x_horizontal + value
            elif position.x < 0:  # left corner
                if not position.is_jumping_horizontally:
                    position.is_jumping_horizontally = True
                    position.tmp_x_horizontal = SnakeGame.config.WIN_WIDTH + position.x
                    position.tmp_y_horizontal = position.y
                else:
                    position.tmp_x_horizontal = position.tmp_x_horizontal + value
            else:
                cls.reset_tmp_horizontal_values(position)
            if position.is_jumping_horizontally:
                if 0 <= position.tmp_x_horizontal <= SnakeGame.config.WIN_WIDTH - Shape.get_size_n(shape_type).width:
                    position.x = position.tmp_x_horizontal
                    cls.reset_tmp_horizontal_values(position)
            else:
                cls.reset_tmp_horizontal_values(position)

    @classmethod
    def update_y(cls, shape_type, position, value: int, is_horizontal: bool):
        from game.shape.shape import Shape

        if is_horizontal:  # indicates that the block is moving vertically
            if position.is_jumping_vertically:
                position.tmp_x_vertical = position.tmp_x_vertical + value
                if position.tmp_x_vertical > SnakeGame.config.WIN_WIDTH:
                    position.tmp_x_vertical = value
                elif position.tmp_x_vertical < 0:
                    position.tmp_x_vertical = SnakeGame.config.WIN_WIDTH + value
        else:
            position.y = position.y + value
            if value > 0:
                cls.update_direction(position, Direction.BOTTOM)
            else:
                cls.update_direction(position, Direction.TOP)
            if position.y + Shape.get_size_n(shape_type).height > SnakeGame.config.WIN_HEIGHT:  # bottom corner
                if not position.is_jumping_vertically:
                    position.is_jumping_vertically = True
                    position.tmp_x_vertical = position.x
                    position.tmp_y_vertical = position.y - SnakeGame.config.WIN_HEIGHT
                else:
                    position.tmp_y_vertical = position.tmp_y_vertical + value
            elif position.y < 0:  # top corner
                if not position.is_jumping_vertically:
                    position.is_jumping_vertically = True
                    position.tmp_x_vertical = position.x
                    position.tmp_y_vertical = SnakeGame.config.WIN_HEIGHT + position.y
                else:
                    position.tmp_y_vertical = position.tmp_y_vertical + value
            else:
                cls.reset_tmp_vertical_values(position)
            if position.is_jumping_vertically:
                if 0 <= position.tmp_y_vertical <= SnakeGame.config.WIN_HEIGHT - Shape.get_size_n(shape_type).height:
                    position.y = position.tmp_y_vertical
                    cls.reset_tmp_vertical_values(position)
            else:
                cls.reset_tmp_vertical_values(position)

    @classmethod
    def update_position(cls, shape_type, position, changing_value, is_horizontal):
        cls.update_x(shape_type, position, changing_value, not is_horizontal)
        cls.update_y(shape_type, position, changing_value, is_horizontal)
        position.velocity = abs(changing_value)

    @staticmethod
    def update_direction(position, new_direction: str):
        position.direction = new_direction
