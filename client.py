from abc import ABCMeta, abstractmethod
import socket
import requests
from util import Address


class Client:
    __metaclass__ = ABCMeta

    def __init__(self, ip, port, neighbors=2):
        self.address = Address(ip, port)
        self.neighbors = neighbors

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address.tuple)

    def allocate(self):
        pass

    def broadcast_message(self, content):
        pass

    @abstractmethod
    def on_receive(self, from_, content):
        pass

    def _forwarding_tree(self):
        # creates a tree of addresses, where each address points to the next address the message should be sent to.
        pass

    def _keep_alive_target(self):
        pass

    def _receive_message_target(self):
        pass
