from pydantic import BaseModel


class LevelState(BaseModel):
    orderedConvoNodes: list[str]
    levelKey: str


class CurrentState(BaseModel):
    level: dict[str, LevelState]


class GameState(BaseModel):
    currentLevel: str
    currentState: CurrentState
