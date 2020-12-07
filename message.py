import json


class Message:
    def __init__(self, content, forwarding_tree):
        self.content = content
        self.forwarding_tree = forwarding_tree

    @staticmethod
    def from_json(obj):
        pass

    def to_json(self):
        pass
