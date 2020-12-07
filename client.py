from abc import ABCMeta, abstractmethod
import socket
import requests
from util import Address
import threading
import json
import time


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

        self.addresses = []

    def allocate(self):
        req = requests.request("POST", self.server_url + "/allocate", data={
            "port": self.address.port
        }).json()
        self.addresses = [Address(ip, port) for ip, port in req.get("addresses")]
        self.__log(f"allocate: {self.id}, {self.addresses}")

        self.socket.listen(self.neighbors)
        self.listen_thread = threading.Thread(target=self._listen_target)
        self.listen_thread.start()

    def broadcast_message(self, content):
        pass

    @staticmethod
    def send_message(obj, dest):
        message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        message_socket.bind(("0.0.0.0", 1141))
        message_socket.connect(dest)

        Client._send_to_conn(obj, message_socket)

        return Client._receive(message_socket)

    @staticmethod
    def _send_to_conn(obj, conn):
        to_send = json.dumps(obj) + "\n"
        to_send = to_send.encode()
        conn.sendall(to_send)

    @property
    @abstractmethod
    def message_handlers(self):
        # map of message type to handler function
        pass

    def shutdown(self):
        self.is_finished = True
        self.socket.close()

    def _forwarding_tree(self):
        # creates a tree of addresses, where each address points to the next address the message should be sent to.
        pass

    def _keep_alive_target(self):
        while not self.is_finished:
            req = requests.request("GET", self.server_url + "/keep_alive").json()
            [Address(ip, port) for ip, port in req.get("addresses")]
            time.sleep(3)

    def _listen_target(self):
        while not self.is_finished:
            try:
                conn, addr = self.socket.accept()
                self.__log(f"connected: {addr[0]}:{addr[1]}")

                client_thread = threading.Thread(target=self._receive_message_target, args=(conn,))
                self.client_threads[conn] = client_thread
                client_thread.start()
            except socket.error as e:
                self.__log("socket exception")
                self.__log(e)
                return
            print("not finished!")

    def _receive_message_target(self, conn):
        obj = self._receive(conn)
        from_ = conn.getpeername()
        response = self.message_handlers[obj.pop("type")](obj, from_)
        self._send_to_conn(response, conn)

    @staticmethod
    def _receive(conn):
        buffer = ""
        while True:
            recv = conn.recv(4096)
            buffer += recv.decode("utf-8")
            if buffer[-1] == "\n":
                break

        return json.loads(buffer)

    def __log(self, message):
        if self.verbose:
            print(f"[{self.address}] {message}")
