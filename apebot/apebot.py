
from .intenter import IntentCaller

from matrix_client.client import MatrixClient


class ApeBot:
    """
    Main runner class for the bot.
    """

    def __init__(self, username, password, room):
        self.intent = IntentCaller()

        self.username = username
        # Connect to Matrix
        self.client = MatrixClient("https://matrix.org")
        self.token = self.client.login_with_password(username=username,
                                                password=password)

        self.room = self.client.join_room(room)
        self.room.add_listener(self.on_message)

    def on_message(self, room, event):
        """
        When a message is received this is called.
        """
        if event['type'] == "m.room.message":
            if event['content']['msgtype'] == "m.text":
                if event['sender'] != self.username:
                    self.intent.get_function(event['content']['body'])(room)
        else:
            pass

    def listen(self):
        try:
            self.client.listen_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.room.send_text("ApeBot going to sleep")

