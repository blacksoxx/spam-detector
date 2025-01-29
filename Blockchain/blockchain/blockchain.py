import hashlib
import json
from time import time

class Block:
    def __init__(self, prev_hash, sender, receiver, data, spam):
        self.timestamp = time()
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.spam = spam
        self.prev_hash = prev_hash
        self.body_hash = self.compute_body_hash()
        self.hash = self.compute_header_hash()

    def compute_body_hash(self):
        body = json.dumps({
            "timestamp": self.timestamp,
            "sender": self.sender,
            "receiver": self.receiver,
            "data": self.data,
            "spam": self.spam
        }, sort_keys=True).encode()
        return hashlib.sha256(body).hexdigest()

    def compute_header_hash(self):
        header = json.dumps({
            "prev_hash": self.prev_hash,
            "body_hash": self.body_hash,
            "timestamp": self.timestamp
        }, sort_keys=True).encode()
        return hashlib.sha256(header).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("0", "system", "system", "Genesis Block", False)
        self.chain.append(genesis_block)

    def add_block(self, sender, receiver, data, spam):
        prev_hash = self.chain[-1].hash
        new_block = Block(prev_hash, sender, receiver, data, spam)
        self.chain.append(new_block)
        return new_block

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.prev_hash != previous.hash:
                return False

            if current.hash != current.compute_header_hash():
                return False

        return True
