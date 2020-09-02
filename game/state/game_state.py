from game import SnakeGame


class GameState:
    # STATIC GLOBAL VALUES
    HIT_IT_SELF = 'hit_it_self'
    HIT_CORNERS = 'hit_corners'
    CLOSED_BY_USER = 'closed_by_user'
    NO_REASON = 'no_reason_bitch!^_^'

    def __init__(self):
        self.loosing_reason = ''
        self.is_paused = False
        self.food_blocks = []
        self.speed_blocks = []

    def set_loosing_state(self, loosing_reason):
        self.loosing_reason = loosing_reason

    def reset(self):
        self.loosing_reason = ''

    def is_lost(self) -> bool:
        if SnakeGame.config.EASY_MODE:
            return False
        else:
            if self.loosing_reason != '':
                return True
            return False

    @staticmethod
    def get_score() -> int:
        return len(SnakeGame.game_manager.snake)
