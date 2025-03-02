from fastapi import FastAPI
from models.game_data import ConversationNode
from models.messages import Reply
from utils.json_state_helpers import (
    add_game_state_ordered_convo_node,
    get_current_game_state,
    get_game_level_data,
)

app = FastAPI()


@app.post("/reply")
async def getNextNodeMessage(reply: Reply | None = None) -> ConversationNode:
    # get nextNode From req body
    reply_text = reply.text if reply else "start"
    # get current level
    current_game_state = get_current_game_state(
        "/home/iyadelwy/Work/Cluster/apps/IJAG/global/state-server/docker/data/gameState.json"
    )
    current_level = current_game_state.currentLevel
    # get orderedConvoNodes array
    current_level_ordered_convo_nodes = current_game_state.currentState.level.get(
        current_level
    ).orderedConvoNodes
    # check logic for next node
    assert (not reply and len(current_level_ordered_convo_nodes) == 0) or (
        reply and len(current_level_ordered_convo_nodes) > 0
    ) is True
    # get current level game data
    current_level_game_data = get_game_level_data(
        "/home/iyadelwy/Work/Cluster/apps/IJAG/global/state-server/docker/data/gameData.json",
        current_level,
    )
    next_node_data = current_level_game_data.convoNodes.get(reply_text, None)
    if next_node_data:
        # add next_node to orderedConvoNodes
        add_game_state_ordered_convo_node(
            "/home/iyadelwy/Work/Cluster/apps/IJAG/global/state-server/docker/data/gameState.json",
            current_level,
            reply_text,
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
    if reply_text != current_level_game_data.levelKey:
        on_wrong_key_message = current_level_game_data.onWrongKey.message
        return ConversationNode(on_wrong_key_message, [])

    # if it is correct then run the action for the current onCorrectKey level
    action = current_level_game_data.onCorrectKey.action

    # then create a ConversationNode with the onCorrectKey message
    # and send it
    on_correct_key_message = current_level_game_data.onCorrectKey.message
    return ConversationNode(on_correct_key_message, [])


@app.post("/onjoin")
async def on_join():
    current_game_state = get_current_game_state(
        "/home/iyadelwy/Work/Cluster/apps/IJAG/global/state-server/docker/data/gameState.json"
    )
    current_level = current_game_state.currentLevel
    # get orderedConvoNodes array
    current_level_ordered_convo_nodes = current_game_state.currentState.level.get(
        current_level
    ).orderedConvoNodes
    # if orderedConvoNodes is empty then initialize orderedConvoNodes with start_node
    # and send start node
    if len(current_level_ordered_convo_nodes) == 0:
        current_level_game_data = get_game_level_data(
            "/home/iyadelwy/Work/Cluster/apps/IJAG/global/state-server/docker/data/gameData.json",
            current_level,
        )
        start_node_data = current_level_game_data.convoNodes["start"]
        # add start_node to orderedConvoNodes
        add_game_state_ordered_convo_node(
            "/home/iyadelwy/Work/Cluster/apps/IJAG/global/state-server/docker/data/gameState.json",
            current_level,
            "start",
        )
        return start_node_data
    # else send last node from orderedConvoNodes
    next_node_data = current_level_game_data.convoNodes.get(
        current_level_ordered_convo_nodes[-1]
    )
    return next_node_data
