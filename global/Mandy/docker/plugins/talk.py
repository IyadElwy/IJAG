import requests
from sopel import plugin


@plugin.rule(r".*")  # Matches any message
def reply_all(bot, trigger):
    # Don't respond to messages from the bot itself to avoid loops
    if trigger.nick == bot.nick:
        return

    # Don't respond to commands (messages starting with .)
    if trigger.match.string.startswith("."):
        return

    reply = trigger.match.string
    # Send response
    # bot.say("You said: {}".format(trigger.match.string))


@plugin.event("JOIN")
def on_join(bot, trigger):
    message = requests.post("state-server:5003/onjoin")
    print(message)
