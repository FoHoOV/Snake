import pygame as pygame


class SnakeGame:
    config = None
    game_manager = None

    @staticmethod
    def start():
        SnakeGame.config = Config()
        SnakeGame.game_manager = GameManager()
        SnakeGame.game_manager.run()


from game.game_manager.game_manager import GameManager
from game.config import Config
