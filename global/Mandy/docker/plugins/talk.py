from time import sleep

import requests
from sopel import formatting, plugin


@plugin.rule(r".*")  # Matches any message
def reply_all(bot, trigger):
    # Don't respond to messages from the bot itself to avoid loops
    if trigger.nick == bot.nick:
        return
    # Don't respond to commands (messages starting with .)
    if trigger.match.string.startswith("."):
        return
    reply = trigger.match.string
    sleep(3)
    response = requests.post(
        "http://state-server:5003/reply",
        headers={"Content-Type": "application/json"},
        json={"next_node_title": reply},
    ).json()
    for msg in response.get("message"):
        bot.say(msg)
        sleep(3)

    if len(response.get("choices")) > 0:
        bot.say(
            formatting.color(
                "Choices:",
                formatting.colors.RED,
            )
        )
        for choice in response.get("choices"):
            bot.say(
                f"{formatting.color(choice.get('reply'), formatting.colors.BLUE)} --- ({formatting.color(choice.get('nextNode'), formatting.colors.LIGHT_BLUE)})"
            )
    else:
        bot.say(f"{formatting.color('Insert Answer:', formatting.colors.LIGHT_PURPLE)}")


@plugin.event("JOIN")
def on_join(bot, trigger):
    if trigger.nick == bot.nick:
        return
    response = requests.post("http://state-server:5003/onjoin").json()
    sleep(3)
    for msg in response.get("message"):
        bot.say(msg)
        sleep(3)
    if len(response.get("choices")) > 0:
        bot.say(
            formatting.color(
                "Choices:",
                formatting.colors.RED,
            )
        )
        for choice in response.get("choices"):
            bot.say(
                f"{formatting.color(choice.get('reply'), formatting.colors.BLUE)}\
                    ({formatting.color(choice.get('nextNode'), formatting.colors.LIGHT_BLUE)})"
            )
    else:
        bot.say(f"{formatting.color('Insert Answer:', formatting.colors.LIGHT_PURPLE)}")
