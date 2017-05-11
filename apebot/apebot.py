from intenter import IntentCaller
from protocol import MatrixProtocol, IRCProtocol


class Poll():
    """
    Poll object for storing info about a vote.
    """
    def __init__(self, bot, text):
        self.text = text
        self.votes = {}
        self.bot = bot
        self.fixed = False

    def display(self):
        outstr = ''
        for (option, n_votes) in self.votes.items():
            outstr += '{} | {} {} \n'.format(n_votes, '='*n_votes, option)
        self.bot.send_message(outstr)


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
