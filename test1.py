from client import Client
import time
import sys


class TestClient(Client):
    def on_test(self, obj, from_):
        print(f"on_test: {from_}, {obj}")
        return "hi!"

    @property
    def message_handlers(self):
        return {
            "test": self.on_test
        }


if __name__ == '__main__':
    client1 = TestClient("127.0.0.1", 1143, "http://127.0.0.1:1140", verbose=True)
    client1.allocate()

    client2 = TestClient("127.0.0.1", 1144, "http://127.0.0.1:1140", verbose=True)
    client2.allocate()

    time.sleep(5)

    ret = client1.send_message({
        "type": "test",
        "message": "hello other client!"
    }, ("127.0.0.1", 1144))
    print("return: ")
    print(ret)

    client1.shutdown()
    client2.shutdown()
