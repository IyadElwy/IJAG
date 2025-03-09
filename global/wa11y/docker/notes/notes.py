import argparse
import sys

import requests

parser = argparse.ArgumentParser(
    prog="Notes CLI",
    description="Using this app you can get info about the game, your objectives and more.\n\n",
)

parser.add_argument("-l", "--levels", help="Get levels", action="store_true")
parser.add_argument(
    "-o",
    "--objectives",
    help="Get level objectives (default current level) Ex. -o 4",
    type=int,
    nargs="?",
)
parser.add_argument(
    "-c",
    "--convos",
    help="Get level conversations (default current level) Ex. -o 3",
    type=int,
    nargs="?",
)

args = parser.parse_args()


def main():
    if args.levels:
        response = requests.get(
            "http://state-server.global.svc.cluster.local:5003/gameState"
        )
        game_state = response.json()
        current_state = game_state.get("currentState")
        levels = sorted(list(current_state.get("level")))
        current_level = game_state.get("currentLevel")
        output = ""
        for level in levels:
            if int(level) < int(current_level):
                output += f"Level {level}: Completed\n"
            elif int(level) == int(current_level):
                output += f"Level {level}: In Progress"
        print(output)
        return
    elif "-o" in sys.argv or "--objectives" in sys.argv:
        level = args.objectives
        state_response = requests.get(
            "http://state-server.global.svc.cluster.local:5003/gameState"
        )
        game_state = state_response.json()
        current_level = game_state.get("currentLevel")
        if not level:
            level = current_level
        if int(level) > int(current_level):
            print(f"Level {level} not reached yet.")
            return
        game_level_data_reponse = requests.get(
            f"http://state-server.global.svc.cluster.local:5003/gameData/{level}",
        )
        level_data = game_level_data_reponse.json()
        title = level_data.get("title")
        plot = level_data.get("storyPlot")
        print(f"Level: {level} --- {title}\n")
        for line in plot:
            print(line)
        print("\n")
    elif "-c" in sys.argv or "--convos" in sys.argv:
        level = args.convos
        state_response = requests.get(
            "http://state-server.global.svc.cluster.local:5003/gameState"
        )
        game_state = state_response.json()
        current_level = game_state.get("currentLevel")
        if not level:
            level = current_level
        if int(level) > int(current_level):
            print(f"Level {level} not reached yet.")
            return
        game_level_data_reponse = requests.get(
            f"http://state-server.global.svc.cluster.local:5003/gameData/{level}",
        )
        level_data = game_level_data_reponse.json()
        title = level_data.get("title")
        # get level data for current state
        ordererd_convo_nodes = (
            game_state.get("currentState")
            .get("level")
            .get(level)
            .get("orderedConvoNodes")
        )
        # get convo nodes from game data
        game_data_convo_nodes = level_data.get("convoNodes")
        print(f"Level: {level} --- {title}\n")
        for i, node in enumerate(ordererd_convo_nodes):
            convo_data = game_data_convo_nodes.get(node)
            mandy_message = convo_data.get("message")
            for line in mandy_message:
                print(f"mandy: {line}")
            if i + 1 < len(ordererd_convo_nodes):
                # get next node to print user choice
                next_node = ordererd_convo_nodes[i + 1]
                choice = sorted(
                    [
                        choice.get("reply")
                        if choice.get("nextNode") == next_node
                        else ""
                        for choice in convo_data.get("choices")
                    ],
                    reverse=True,
                )[0]
                print(f"wa11y: {choice}")
        print("\n")


if __name__ == "__main__":
    main()
