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

    def listen_forever(self):
        try:
            self.client.listen_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.room.send_text("ApeBot going to sleep")

    def add_event_callback(self, callback):
        self.room.add_listener(callback)
