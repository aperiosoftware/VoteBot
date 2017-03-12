from apebot.apebot import ApeBot, MatrixProtocol

protocol = MatrixProtocol("@apebot:localhost", "apebot",
                          "#apebot2:localhost", "http://localhost:8008")
apebot = ApeBot(protocol)


@apebot.intent.register_keyword("hide")
def hide(bot, message, sender):
    bot.send_message("ApeBot Hides")


@apebot.intent.register_keyword("hello")
def say_hello(bot, message, sender):
    bot.send_message("Hello {}".format(sender))


apebot.listen()
