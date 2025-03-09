from alter_state.alter import alter_state
from fastapi import FastAPI, HTTPException
from models.game_data import ConversationNode, Level
from models.messages import NextNode
from models.state import GameState
from utils.json_state_helpers import (
    add_game_state_ordered_convo_node,
    get_current_game_state,
    get_game_level_data,
)

app = FastAPI()


@app.post("/reply")
async def getNextNodeMessage(next_node: NextNode | None = None) -> ConversationNode:
    # get nextNode From req body
    next_node_title = next_node.next_node_title if next_node else "start"
    # get current level
    current_game_state = get_current_game_state()
    current_level = current_game_state.currentLevel
    # get orderedConvoNodes array
    current_level_ordered_convo_nodes = current_game_state.currentState.level.get(
        current_level
    ).orderedConvoNodes
    # check logic for next node
    assert (not next_node and len(current_level_ordered_convo_nodes) == 0) or (
        next_node and len(current_level_ordered_convo_nodes) > 0
    ) is True
    # get current level game data
    current_level_game_data = get_game_level_data(current_level)
    next_node_data = current_level_game_data.convoNodes.get(next_node_title, None)
    if next_node_data:
        # add next_node to orderedConvoNodes
        add_game_state_ordered_convo_node(current_level, next_node_title)
        return next_node_data
    # if next_node is invalid get latest node data from orderedConvoNodes
    next_node_data = current_level_game_data.convoNodes.get(
        current_level_ordered_convo_nodes[-1]
    )
    # first check if this is a key reply or not
    if len(next_node_data.choices) > 0:
        return next_node_data
    # if it is then first check for correctness
    # if it is not correct create a ConversationNode with the OnWrongKey message
    # and send it
    if (
        next_node_title
        != current_game_state.currentState.level.get(current_level).levelKey
    ):
        on_wrong_key_message = current_level_game_data.onWrongKey.message
        return ConversationNode(message=on_wrong_key_message, choices=[])
    # change state of k8s environment according to new state
    alter_state(str(int(current_level) + 1))
    # then create a ConversationNode with the onCorrectKey message
    # and send it
    on_correct_key_message = current_level_game_data.onCorrectKey.message
    return ConversationNode(
        message=on_correct_key_message,
        choices=[
            {
                "reply": "Type anything to move on to the next level.",
                "nextNode": "Anything",
            }
        ],
    )


@app.post("/onjoin")
async def on_join() -> ConversationNode:
    current_game_state = get_current_game_state()
    current_level = current_game_state.currentLevel
    # get orderedConvoNodes array
    current_level_ordered_convo_nodes = current_game_state.currentState.level.get(
        current_level
    ).orderedConvoNodes
    current_level_game_data = get_game_level_data(current_level)
    # if orderedConvoNodes is empty then initialize orderedConvoNodes with start_node
    # and send start node
    if len(current_level_ordered_convo_nodes) == 0:
        start_node_data = current_level_game_data.convoNodes["start"]
        # add start_node to orderedConvoNodes
        add_game_state_ordered_convo_node(current_level, "start")
        return start_node_data
    # else send last node from orderedConvoNodes
    next_node_data = current_level_game_data.convoNodes.get(
        current_level_ordered_convo_nodes[-1]
    )
    return next_node_data


@app.get("/gameData/{level}")
async def get_game_data(level: str) -> Level:
    try:
        int(level)
    except ValueError:
        return HTTPException(status_code=422, detail="Level string not valid")
    return get_game_level_data(level)


@app.get("/gameState")
async def get_game_state() -> GameState:
    current_game_state = get_current_game_state()
    return current_game_state
