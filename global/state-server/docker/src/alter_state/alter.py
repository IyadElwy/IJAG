from uuid import uuid4

from models.state import LevelState
from utils.json_state_helpers import get_current_game_state, save_new_game_state


def initialize_next_level(next_level: str, level_key: str):
    game_state = get_current_game_state()
    game_state.currentLevel = next_level
    game_state.currentState.level[next_level] = LevelState(
        orderedConvoNodes=["start"], levelKey=level_key, notes=[]
    )
    save_new_game_state(game_state)


def alter_state(next_level: str):
    level_key = str(uuid4())
    initialize_next_level(next_level, level_key)
    match next_level:
        case "2":
            from .levels.level_2 import Level2

            Level2(level_key)
