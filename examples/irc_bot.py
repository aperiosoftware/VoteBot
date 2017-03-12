from apebot.apebot import ApeBot, IRCProtocol

protocol = IRCProtocol("apebot", None, "#apebot", "irc.freenode.net")
apebot = ApeBot(protocol)


@apebot.intent.register_keyword("hide")
def hide(bot, message, sender):
    bot.send_message("ApeBot Hides")


@apebot.intent.register_keyword("hello")
def say_hello(bot, message, sender):
    bot.send_message("Hello {}".format(sender))


apebot.listen()
