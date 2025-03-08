from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator, model_validator


class ConversationChoice(BaseModel):
    reply: str = Field(description="The player's response text")
    nextNode: str = Field(
        description="The ID of the next conversation node to navigate to"
    )


class ConversationNode(BaseModel):
    message: List[str] = Field(
        description="The message displayed for this conversation node"
    )
    choices: List[ConversationChoice] = Field(
        description="Available response choices for this node"
    )


class OnWrongKey(BaseModel):
    message: List[str]


class OnCorrectKey(BaseModel):
    message: List[str]


class Level(BaseModel):
    title: str = Field(description="Level title")
    storyPlot: List[str] = Field(description="The plot for the current level")
    objectives: List[str] = Field(description="Current level objectives")
    onWrongKey: OnWrongKey = Field(
        description="Response when an incorrect key is provided"
    )
    onCorrectKey: OnCorrectKey = Field(
        description="Response when the correct key is provided"
    )
    convoNodes: Dict[str, ConversationNode] = Field(
        description="The conversation nodes for the interactive narrative"
    )

    @model_validator(mode="after")
    def validate_start_node_exists(self) -> "Level":
        if "start" not in self.convoNodes:
            raise ValueError("convoNodes must contain a 'start' node")
        return self


class GameData(BaseModel):
    level: Dict[str, Level] = Field(description="The game state for each level")

    @field_validator("level")
    @classmethod
    def validate_level_keys(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        for key in v.keys():
            if not key.isdigit():
                raise ValueError(f"Level key '{key}' must be a digit string")
        return v
