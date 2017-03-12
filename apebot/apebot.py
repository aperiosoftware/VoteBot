
from .intenter import IntentCaller

from .protocol import MatrixProtocol


class ApeBot:
    """
    Main runner class for the bot.
    """

    def __init__(self, username, password, room, server):
        self.intent = IntentCaller()
        self.protocol = MatrixProtocol(username, password, room, server)
        self.protocol.add_event_callback(self.on_event)

    def on_event(self, room, event):
        """
        When a message is received this is called.
        """
        if event['type'] == "m.room.message":
            if event['content']['msgtype'] == "m.text":
                # Ignore everything the bot says.
                if event['sender'] != self.protocol.username:
                    func = self.intent.get_function(event['content']['body'])
                    # func is None if no intent found.
                    if func:
                        func(self, room)

    def listen(self):
        self.protocol.listen_forever()
