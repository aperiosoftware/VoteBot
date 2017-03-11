from apebot.apebot import ApeBot

password = input('Password? ')
apebot = ApeBot("@apebot:matrix.org", password, "#apebot:matrix.org")


@apebot.intent.register_keyword("hide")
def hide(room):
    room.send_text("ApeBot Hides")


@apebot.intent.register_keyword("George")
def george(room):
    room.send_text("Hello George")


apebot.listen()
