from .apebot import ApeBot

apebot = ApeBot("@apebot:matrix.org", "password", "#apebot:matrix.org")


@apebot.intent.register_keyword("hide")
def hide(room):
    room.send_message("ApeBot Hides")


apebot.listen()
