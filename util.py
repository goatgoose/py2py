
class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @property
    def tuple(self):
        return self.ip, self.port

    def __str__(self):
        return f"{self.ip}:{self.port}"

    def __repr__(self):
        return str(self)
