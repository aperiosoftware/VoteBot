from intenter import IntentCaller
from protocol import MatrixProtocol, IRCProtocol
import sys

password = sys.argv[1]


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


class VoteBot:
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

    def send_emote(self, message):
        """
        Transmit a /me style message into the current room.
        """
        self.protocol.send_emote(message)



thisbot = VoteBot(MatrixProtocol("@pyastrobot:matrix.org", password, '#pyastro:matrix.org', "https://matrix.org"))


def hide(thisbot, message, sender):
    thisbot.send_emote('hides')


def pingall(thisbot, message, sender):
    room = thisbot.protocol.room
    users = room.get_joined_members()
    for (user, info) in users.items():
        if 'pyastrobot' not in user:
            thisbot.send_message('ping {}'.format(user))


def newpoll(thisbot, message, sender):
    room = thisbot.protocol.room
    question = message.replace('Poll: ', '')
    thisbot.poll = Poll(thisbot, question)
    #pingall(thisbot, message, sender)
    thisbot.send_message(question)


def votefor(thisbot, message, sender):
    room = thisbot.protocol.room
    response = message.replace('Vote:', '')
    if not thisbot.poll.fixed:
        if response not in thisbot.poll.votes.keys():
            thisbot.poll.votes[response] = 1
        else:
            thisbot.poll.votes[response] += 1
    else:
        if response not in thisbot.poll.votes.keys():
            thisbot.send_message("I'm sorry {}, I can't let you do that.".format(sender))
        else:
            thisbot.poll.votes[response] += 1
    thisbot.send_message('Thanks for voting for "{}", {}'.format(response, sender))


def showpoll(thisbot, message, sender):
    thisbot.send_message("Here's the question: {}".format(thisbot.poll.text))
    thisbot.send_message('Votes so far:\n')
    thisbot.poll.display()


def fixoptions(thisbot, message, sender):
    thisbot.poll.fixed = True
    options = message.replace('Options:', '').split(',')
    for o in options: o.strip()
    thisbot.poll.votes = {opt: 0 for opt in options}

thisbot.intent.register_keyword('Hide')(hide)
thisbot.intent.register_keyword('Ping')(pingall)
thisbot.intent.register_keyword('Poll')(newpoll)
thisbot.intent.register_keyword('Vote')(votefor)
thisbot.intent.register_keyword('Show')(showpoll)
thisbot.intent.register_keyword('Options')(fixoptions)

thisbot.listen()
