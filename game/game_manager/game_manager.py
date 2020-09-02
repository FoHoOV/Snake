from game.movement.coordiantes import Position, Direction
from game.shape.shape import SnakeShapes, Shape, Snake, SnakeBlock
from game.state.game_state import GameState
from game import pygame, SnakeGame
import os
from random import randint


class GameManager:

    def __init__(self):
        self.window = None
        # index 0 = head
        self.snake = None
        self.state = None
        self.handler = None
        self.restart = False

    def setup(self, initial_direction, initial_snake_shape, initial_snake_length, max_food_blocks_length,
              max_speed_blocks_length,
              fps):
        # use shape horizontally and starting direction left and right or shape vertically
        # and starting direction top or bottom

        if self.handler:
            if self.handler.is_alive():
                self.handler.cancel()
                handler = None

        SnakeGame.config.WIN_WIDTH = 900
        SnakeGame.config.WIN_HEIGHT = 900
        SnakeGame.config.CORNERS_BLOCK_WIDTH = Shape.get_size(Shape.CORNERS_BLOCK)[0]
        SnakeGame.config.CORNERS_BLOCK_HEIGHT = Shape.get_size(Shape.CORNERS_BLOCK)[1]
        SnakeGame.config.INITIAL_SNAKE_LENGTH = initial_snake_length
        SnakeGame.config.INITIAL_DIRECTION = initial_direction
        SnakeGame.config.MAX_FOOD_BLOCKS_LENGTH = max_food_blocks_length
        SnakeGame.config.MAX_SPEED_BLOCKS_LENGTH = max_speed_blocks_length
        SnakeGame.config.SNAKE_SHAPE = initial_snake_shape
        SnakeGame.config.FPS = fps

        self.window = pygame.display.set_mode((SnakeGame.config.WIN_WIDTH, SnakeGame.config.WIN_HEIGHT))
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 20, True)

        self.state = GameState()

        # index 0 is for x and 1 is for y
        self.state.food_blocks_coordinates = []
        self.state.speed_blocks_coordinates = []
        self.snake = Snake(initial_snake_length, initial_direction)

    def start(self):
        food_loop_counter = 0
        speed_loop_counter = 0
        pause_loop_counter = 0
        self.state.is_paused = False
        game_paused_text = self.font.render('pause! (press space again to continue)', 1, (255, 255, 255))
        corner_block = Shape(Shape.CORNERS_BLOCK)
        food_block = Shape(Shape.FOOD_BLOCK)
        speed_block = Shape(Shape.SPEED_BLOCK)
        # mainloop
        while not self.state.is_lost():
            self.clock.tick(SnakeGame.config.FPS)
            pressed_keys = pygame.key.get_pressed()
            self.window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.set_loosing_state(GameState.CLOSED_BY_USER)
                    break

            if pressed_keys[pygame.K_SPACE]:
                pause_loop_counter += 1
                if pause_loop_counter == 5:
                    pause_loop_counter = 0
                    self.state.is_paused = not self.state.is_paused
            else:
                pause_loop_counter = 0
            if self.state.is_paused:
                self.snake.draw(None)
            else:
                is_key_pressed = False
                pressed_keys_for_snake = None
                # change to elif if you want to disable X and Y move at the same time
                if food_loop_counter >= 150:
                    if len(self.state.food_blocks_coordinates) < SnakeGame.config.MAX_FOOD_BLOCKS_LENGTH:
                        self.state.food_blocks_coordinates.append(Position.random_position_generator())
                    food_loop_counter = 0
                    if speed_loop_counter > 5:
                        if len(self.state.speed_blocks_coordinates) < SnakeGame.config.MAX_SPEED_BLOCKS_LENGTH and (
                                randint(1, 20) < 10):
                            self.state.speed_blocks_coordinates.append(Position.random_position_generator())
                        speed_loop_counter = 0
                    speed_loop_counter += 1
                food_loop_counter = food_loop_counter + 1

                if pressed_keys[pygame.K_RIGHT]:
                    if not is_key_pressed:
                        pressed_keys_for_snake = []
                    is_key_pressed = True
                    pressed_keys_for_snake.append(pygame.K_RIGHT)
                if pressed_keys[pygame.K_LEFT]:
                    if not is_key_pressed:
                        pressed_keys_for_snake = []
                    is_key_pressed = True
                    pressed_keys_for_snake.append(pygame.K_LEFT)
                if pressed_keys[pygame.K_DOWN]:
                    if not is_key_pressed:
                        pressed_keys_for_snake = []
                    is_key_pressed = True
                    pressed_keys_for_snake.append(pygame.K_DOWN)
                if pressed_keys[pygame.K_UP]:
                    if not is_key_pressed:
                        pressed_keys_for_snake = []
                    is_key_pressed = True
                    pressed_keys_for_snake.append(pygame.K_UP)
                self.snake.draw(pressed_keys_for_snake)

            for food_coordinate in self.state.food_blocks_coordinates:
                food_block.draw(x=food_coordinate[0], y=food_coordinate[1])
            for speed_coordinate in self.state.speed_blocks_coordinates:
                speed_block.draw(x=speed_coordinate[0], y=speed_coordinate[1])
            # corners

            corner_block.draw(x=0, y=0)
            corner_block.draw(x=SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH, y=0)
            corner_block.draw(x=0, y=SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT)
            corner_block.draw(x=SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH,
                              y=SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT)

            score_text = self.font.render('Score: ' + str(GameState.get_score()), 1, (255, 255, 255))
            if self.state.is_paused:
                self.window.blit(game_paused_text,
                                 (SnakeGame.config.WIN_WIDTH / 3, SnakeGame.config.WIN_HEIGHT / 2 - 10))

            self.window.blit(score_text, (SnakeGame.config.WIN_WIDTH - 100, 10))
            pygame.display.update()
            if self.state.is_lost():
                print('you lost! , reason: ', self.state.loosing_reason)

    def end(self):
        def change_best_score():
            if best_score:
                if int(best_score) < self.state.get_score():
                    with open("best_score.txt", "w") as file:
                        file.write(str(self.state.get_score()))
            else:
                with open("best_score.txt", "w") as file:
                    file.write(str(self.state.get_score()))

        self.window.fill((0, 0, 0))
        best_score = None
        best_score_text = None
        if os.path.exists('best_score.txt'):
            with open('best_score.txt', 'r') as file:
                best_score = file.read()
        print('current_score:', self.state.get_score())
        print('best_score:', best_score)
        if best_score and int(best_score) > self.state.get_score():
            best_score_text = self.font.render('Best Score: ' + best_score, 1, (255, 255, 255))
        else:
            best_score_text = self.font.render('Best Score: ' + str(self.state.get_score()), 1,
                                               (255, 255, 255))
        score_text = self.font.render('Score: ' + str(self.state.get_score()), 1, (255, 255, 255))
        loosing_reason_text = self.font.render('You Lost!: ' + str(self.state.loosing_reason), 1,
                                               (255, 0, 0))
        want_to_play_again_text = self.font.render("If you want to play again press 'Y' otherwise press 'N'.", 1,
                                                   (255, 255, 255))

        self.window.blit(score_text, (SnakeGame.config.WIN_WIDTH - 100, 10))
        self.window.blit(best_score_text, (SnakeGame.config.WIN_WIDTH / 2 - 55, SnakeGame.config.WIN_HEIGHT / 2 - 50))
        self.window.blit(loosing_reason_text, (SnakeGame.config.WIN_WIDTH / 2 - 100, SnakeGame.config.WIN_HEIGHT / 2))
        self.window.blit(want_to_play_again_text,
                         (SnakeGame.config.WIN_WIDTH / 2 - 200, SnakeGame.config.WIN_HEIGHT / 2 + 50))

        pygame.display.update()
        running = True
        while running:
            self.clock.tick(SnakeGame.config.FPS)
            pressed_keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('BYE :)')
                    running = False
                    break
            if pressed_keys[pygame.K_y]:
                change_best_score()
                running = False
                self.run()

            elif pressed_keys[pygame.K_n]:
                print('BYE :)')
                running = False

        if self.handler and self.handler.is_alive():
            self.handler.cancel()

        change_best_score()
        pygame.quit()

    def run(self):
        self.setup(Direction.LEFT, SnakeShapes.HORIZONTALLY, 19, 5, 1, 60)
        self.start()
        # if we loose or quit initiates end
        self.end()
