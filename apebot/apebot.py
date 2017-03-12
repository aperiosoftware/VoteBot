from .intenter import IntentCaller
from .protocol import MatrixProtocol


class ApeBot:
    """
    Main runner class for the bot.
    """

    def __init__(self, protocol):
        self.intent = IntentCaller()
        self.protocol = protocol
        # Add the intent parser callback
        self.protocol.add_event_callback(self.on_message)

    def on_message(self, message, sender):
        """
        When a message is received this is called.
        """
        func = self.intent.get_function(message)
        # func is None if no intent found.
        if func:
            func(self, message, sender)

    def listen(self):
        self.protocol.listen_forever()

    def send_message(self, message):
        """
        Transmit a message into the current room.
        """
        self.protocol.send_message(message)
