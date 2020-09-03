from game.ai.snake_ai import SnakeAI
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
        self.restart = False

    def setup(self, **kwargs):
        # use shape horizontally and starting direction left and right or shape vertically
        # and starting direction top or bottom

        if self.snake:
            if self.snake.handler:
                if self.snake.handler.is_alive():
                    self.snake.handler.cancel()
                    self.snake.handler = None

        if kwargs.get('initial_snake_length'):
            SnakeGame.config.INITIAL_SNAKE_LENGTH = kwargs.get('initial_snake_length')
        if kwargs.get('initial_direction'):
            SnakeGame.config.INITIAL_DIRECTION = kwargs.get('initial_direction')
        if kwargs.get('max_food_blocks_length'):
            SnakeGame.config.MAX_FOOD_BLOCKS_LENGTH = kwargs.get('max_food_blocks_length')
        if kwargs.get('max_speed_blocks_length'):
            SnakeGame.config.MAX_SPEED_BLOCKS_LENGTH = kwargs.get('max_speed_blocks_length')
        if kwargs.get('initial_snake_shape'):
            SnakeGame.config.SNAKE_SHAPE = kwargs.get('initial_snake_shape')
        if kwargs.get('fps'):
            SnakeGame.config.FPS = kwargs.get('fps')

        self.window = pygame.display.set_mode((SnakeGame.config.WIN_WIDTH, SnakeGame.config.WIN_HEIGHT))
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 20, True)

        self.state = GameState()

        self.snake = Snake(SnakeGame.config.INITIAL_SNAKE_LENGTH, SnakeGame.config.INITIAL_DIRECTION)

    def start(self):
        food_loop_counter = 0
        speed_loop_counter = 0
        pause_loop_counter = 0
        self.state.is_paused = False
        game_paused_text = self.font.render('pause! (press space again to continue)', 1, (255, 255, 255))

        corner_blocks = [
            Shape(Shape.CORNERS_BLOCK, x=0, y=0),
            Shape(Shape.CORNERS_BLOCK, x=SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH, y=0),
            Shape(Shape.CORNERS_BLOCK, x=0, y=SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT),
            Shape(Shape.CORNERS_BLOCK, x=SnakeGame.config.WIN_WIDTH - SnakeGame.config.CORNERS_BLOCK_WIDTH,
                  y=SnakeGame.config.WIN_HEIGHT - SnakeGame.config.CORNERS_BLOCK_HEIGHT)
        ]
        snake_ai = SnakeAI()
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
                    if len(self.state.food_blocks) < SnakeGame.config.MAX_FOOD_BLOCKS_LENGTH:
                        pos = Position.random_position_generator()
                        if SnakeGame.config.MOVE_FOOD_BLOCKS:
                            if randint(1, 1000) < 300:
                                self.state.food_blocks.append(
                                    Shape(Shape.FOOD_BLOCK, x=pos[0], y=pos[1], randomize_position=True,
                                          randomize_position_interval=10))
                            else:
                                self.state.food_blocks.append(
                                    Shape(Shape.FOOD_BLOCK, x=pos[0], y=pos[1]))
                        else:
                            self.state.food_blocks.append(
                                Shape(Shape.FOOD_BLOCK, x=pos[0], y=pos[1]))

                    food_loop_counter = 0
                    if speed_loop_counter > 5:
                        if len(self.state.speed_blocks) < SnakeGame.config.MAX_SPEED_BLOCKS_LENGTH and (
                                randint(1, 20) < 10):
                            pos = Position.random_position_generator()
                            self.state.speed_blocks.append(Shape(Shape.SPEED_BLOCK, x=pos[0], y=pos[1]))
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
                if SnakeGame.config.AI:
                    if not snake_ai.has_target():
                        snake_ai.create_target_if_exists()
                    if is_key_pressed or not snake_ai.has_target():
                        self.snake.draw(pressed_keys_for_snake)
                    else:
                        snake_ai.move()
                else:
                    self.snake.draw(pressed_keys_for_snake)

            for food_block in self.state.food_blocks:
                food_block.draw()
            for speed_block in self.state.speed_blocks:
                speed_block.draw()
            for corner_block in corner_blocks:
                corner_block.draw()

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

        if self.snake.handler and self.snake.handler.is_alive():
            self.snake.handler.cancel()

        change_best_score()
        pygame.quit()

    def run(self):
        self.setup()
        self.start()
        # if we loose or quit initiates end
        self.end()
