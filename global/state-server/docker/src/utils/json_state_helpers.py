import json

from models.game_data import GameData, Level
from models.state import GameState


def get_current_game_state() -> GameState:
    game_state_file_path = "/data/gameState.json"
    with open(game_state_file_path, "r") as state_file:
        state_file_as_json = json.loads(state_file.read())
        return GameState(**state_file_as_json)


def save_new_game_state(updated_game_state: GameState):
    game_state_file_path = "/data/gameState.json"
    with open(game_state_file_path, "w") as state_file:
        state_file.write(updated_game_state.model_dump_json())


def get_game_level_data(level: str) -> Level:
    game_data_file_path = "/state-server/data/gameData.json"
    with open(game_data_file_path, "r") as game_data_file:
        game_data_as_json = json.loads(game_data_file.read())
        game_data_model = GameData(**game_data_as_json)
        level_data = game_data_model.level.get(level)
        return level_data


def add_game_state_ordered_convo_node(level: str, convo_node_name: str):
    game_state_file_path = "/data/gameState.json"
    with open(game_state_file_path, "r") as state_file:
        state_file_as_json = json.loads(state_file.read())
        game_state = GameState(**state_file_as_json)
    game_state.currentState.level.get(level).orderedConvoNodes.append(convo_node_name)
    with open(game_state_file_path, "w") as state_file:
        state_file.write(game_state.model_dump_json())
