from client import Client
import time


class TestClient(Client):
    def on_receive(self, content, from_):
        print(from_, content)


if __name__ == '__main__':
    client1 = TestClient("127.0.0.1", 1142, "http://127.0.0.1")
    client1.allocate()

    client2 = TestClient("127.0.0.1", 1143, "http://127.0.0.1")
    client2.allocate()

    time.sleep(5)

    client1.broadcast_message("hello other clients!")
