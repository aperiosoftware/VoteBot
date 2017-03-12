from apebot.apebot import ApeBot

apebot = ApeBot("@apebot:localhost","apebot",
                "#apebot2:localhost", "http://localhost:8008")


@apebot.intent.register_keyword("hide")
def hide(bot, room):
    room.send_text("ApeBot Hides")


@apebot.intent.register_keyword("George")
def george(bot, room):
    room.send_text("Hello George")


apebot.listen()
