import abc

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
        self.message_callbacks = []

    @abc.abstractmethod
    def listen_forever(self):
        """
        Run a loop listening for events.
        """

    @abc.abstractmethod
    def add_event_callback(self, callback):
        """
        Add a callback for a new event.
        """

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


class MatrixProtocol(Protocol):
    """
    A Matrix Protocol wrapper.
    """

    def __init__(self, username, password, room, server):
        self.username = username
        # Connect to Matrix
        self.client = MatrixClient(server)
        self.token = self.client.login_with_password(username=username,
                                                     password=password)

        self.room = self.client.join_room(room)
        self.room.add_listener(self.process_event)
        self.event_callbacks = []

    def listen_forever(self):
        try:
            self.client.listen_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.room.send_text("ApeBot going to sleep")

    def add_event_callback(self, callback):
        """
        Add a callback to be called on a message event.

        callbacks should have the signature ``call(message, sender)``.
        """
        self.event_callbacks.append(callback)

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


