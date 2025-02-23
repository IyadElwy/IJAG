from sopel import plugin


@plugin.rule(r".*")  # Matches any message
def reply_all(bot, trigger):
    """Responds to every message in the channel"""
    # Don't respond to messages from the bot itself to avoid loops
    if trigger.nick == bot.nick:
        return

    # Don't respond to commands (messages starting with .)
    if trigger.match.string.startswith("."):
        return

    # Send response
    bot.say("Hello, friend.")
    bot.say("You said: {}".format(trigger.match.string))
