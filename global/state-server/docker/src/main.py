from fastapi import FastAPI
from models.game_data import ConversationNode
from models.messages import NextNode
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
    current_game_state = get_current_game_state("/data/gameState.json")
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
    current_level_game_data = get_game_level_data(
        "/state-server/data/gameData.json",
        current_level,
    )
    next_node_data = current_level_game_data.convoNodes.get(next_node_title, None)
    if next_node_data:
        # add next_node to orderedConvoNodes
        add_game_state_ordered_convo_node(
            "/data/gameState.json",
            current_level,
            next_node_title,
        )
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
    if next_node_title != current_level_game_data.levelKey:
        on_wrong_key_message = current_level_game_data.onWrongKey.message
        return ConversationNode(message=on_wrong_key_message, choices=[])

    # if it is correct then run the action for the current onCorrectKey level
    action = current_level_game_data.onCorrectKey.action

    # then create a ConversationNode with the onCorrectKey message
    # and send it
    on_correct_key_message = current_level_game_data.onCorrectKey.message
    return ConversationNode(message=on_correct_key_message, choices=[])


@app.post("/onjoin")
async def on_join() -> ConversationNode:
    current_game_state = get_current_game_state("/data/gameState.json")
    current_level = current_game_state.currentLevel
    # get orderedConvoNodes array
    current_level_ordered_convo_nodes = current_game_state.currentState.level.get(
        current_level
    ).orderedConvoNodes
    current_level_game_data = get_game_level_data(
        "/state-server/data/gameData.json",
        current_level,
    )
    # if orderedConvoNodes is empty then initialize orderedConvoNodes with start_node
    # and send start node
    if len(current_level_ordered_convo_nodes) == 0:
        start_node_data = current_level_game_data.convoNodes["start"]
        # add start_node to orderedConvoNodes
        add_game_state_ordered_convo_node(
            "/data/gameState.json",
            current_level,
            "start",
        )
        return start_node_data
    # else send last node from orderedConvoNodes
    next_node_data = current_level_game_data.convoNodes.get(
        current_level_ordered_convo_nodes[-1]
    )
    return next_node_data
