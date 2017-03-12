import abc

import pydle
from matrix_client.client import MatrixClient


class Protocol(metaclass=abc.ABCMeta):
    """
    An abstraction of a chat protocol
    """
    @abc.abstractmethod
    def __init__(self, username, password, room, server):
        """
        Connect to the server with the username and password and join the chat
        room.

        username and room should be made into class attributes.
        """
        self.event_callbacks = []

    @abc.abstractmethod
    def listen_forever(self):
        """
        Run a loop listening for events.
        """

    def add_event_callback(self, callback):
        """
        Add a callback to be called on a message event.

        callbacks should have the signature ``call(message, sender)``.
        """
        self.event_callbacks.append(callback)

    @abc.abstractmethod
    def send_message(self, message):
        """
        Send a message.
        """
    @abc.abstractmethod
    def process_event(self, event, callback):
        """
        Take a raw protocol event and then call the callback if it's something
        the bot should read.
        """


class IRCClient(pydle.Client):

    def on_connect(self):
         self.join(self.room)

    def on_message(self, source, target, message):
         self.message_callback(source, target, message)


class IRCProtocol(Protocol):

    def __init__(self, username, password, room, server, port=6667, tls=False):
        super().__init__(username, password, room, server)
        self.username = username
        self.room = room
        self.client = IRCClient('ApeBot')
        self.client.room = self.room
        self.client.message_callback = self.process_event
        self.client.connect(server, port, tls=tls)

    def listen_forever(self):
        self.client.handle_forever()

    def send_message(self, message):
        self.client.message(self.room, message)

    def process_event(self, source, target, message):
        for call in self.event_callbacks:
            call(message, target)


class MatrixProtocol(Protocol):
    """
    A Matrix Protocol wrapper.
    """

    def __init__(self, username, password, room, server):
        super().__init__(username, password, room, server)
        self.username = username
        # Connect to Matrix
        self.client = MatrixClient(server)
        self.token = self.client.login_with_password(username=username,
                                                     password=password)

        self.room = self.client.join_room(room)
        self.room.add_listener(self.process_event)

    def listen_forever(self):
        try:
            self.client.listen_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.room.send_text("ApeBot going to sleep")

    def send_message(self, message):
        self.room.send_text(message)

    def _is_message(self, event):
        if event['type'] == "m.room.message":
            if event['content']['msgtype'] == "m.text":
                # Ignore everything the bot says.
                if event['sender'] != self.username:
                    return event

    def process_event(self, room, event):
        if self._is_message(event):
            for call in self.event_callbacks:
                call(event['content']['body'], event['sender'])


