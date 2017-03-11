from apebot.apebot import ApeBot

apebot = ApeBot("@apebot:matrix.org", "8HDye,skSncLhasy", "#apebot:matrix.org")


@apebot.intent.register_keyword("hide")
def hide(room):
    room.send_text("ApeBot Hides")


apebot.listen()
