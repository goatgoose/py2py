from abc import ABCMeta, abstractmethod
import socket
import requests
from util import Address
import threading
import json
from message import Message


class Client:
    __metaclass__ = ABCMeta

    def __init__(self, ip, port, server_url, neighbors=2, verbose=False):
        self.address = Address(ip, port)
        self.server_url = server_url
        self.neighbors = neighbors
        self.verbose = verbose

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address.tuple)

        self.is_finished = False

        self.listen_thread = None
        self.client_threads = {}  # connection : thread

        self.id = None
        self.addresses = []

    def allocate(self):
        req = requests.request("POST", self.server_url, data={
            "port": self.address.port
        }).json()
        self.id = req.get("id")
        self.addresses = [Address(ip, port) for ip, port in req.get("addresses")]
        self.__log(f"allocate: {self.id}, {self.addresses}")

        self.listen_thread = threading.Thread(target=self._listen_target)
        self.listen_thread.start()

    def broadcast_message(self, content):
        pass

    def send_message(self, content, to):
        pass

    @abstractmethod
    def on_receive(self, content, from_):
        pass

    def _forwarding_tree(self):
        # creates a tree of addresses, where each address points to the next address the message should be sent to.
        pass

    def _keep_alive_target(self):
        pass

    def _listen_target(self):
        while not self.is_finished:
            try:
                conn, addr = self.socket.accept()
                self.__log(f"connected: {addr[0]}:{addr[1]}")

                client_thread = threading.Thread(target=self._receive_message_target, args=(conn,))
                self.client_threads[conn] = client_thread
                client_thread.start()
            except socket.error as e:
                print("socket exception")
                print(e)
                return

    def _receive_message_target(self, conn):
        buffer = ""
        while True:
            recv = conn.recv(65535)
            if not recv:
                self.client_threads.pop(conn)
                self.__log(f"sock closed: {conn}")
                return

            buffer += recv.decode("utf-8")
            lines = buffer.split("\n")
            buffer = lines[-1]

            for line in lines[:-1]:
                self._receive(json.loads(line), conn.getpeername())

    def _receive(self, recv_obj, from_):
        message = Message.from_json(recv_obj)
        self.on_receive(message.content, from_)

    def __log(self, message):
        if self.verbose:
            print(message)
