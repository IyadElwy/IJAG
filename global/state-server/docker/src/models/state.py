from pydantic import BaseModel


class LevelState(BaseModel):
    orderedConvoNodes: list[str]
    notes: list[str]


class CurrentState(BaseModel):
    level: dict[str, LevelState]


class GameState(BaseModel):
    currentLevel: str
    currentState: CurrentState
