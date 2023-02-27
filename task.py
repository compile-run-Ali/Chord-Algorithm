import hashlib
import random

class Node:
    def __init__(self, id):
        self.id = id
        self.successor = None
        self.predecessor = None
        self.finger_table = []
        self.data = {}

    def join(self, ring):
        if ring.nodes:
            self.successor = ring.get_node(self.id).find_successor(self.id)
            self.predecessor = self.successor.predecessor
            self.successor.predecessor = self
            self.predecessor.successor = self
            self.update_finger_table()
        else:
            self.successor = self
            self.predecessor = self

    def find_successor(self, id):
        node = self
        while True:
            if node.id == id:
                return node
            else:
                n = node.closest_preceding_node(id)
                if n == node:
                    return n.successor
                node = n


    def closest_preceding_node(self, id):
        for i in range(7, -1, -1):
            if self.finger_table[i] and self.finger_table[i].id != self.id and self.finger_table[i].id in range(self.id+1, id):
                return self.finger_table[i]
        return self


    def update_finger_table(self):
        self.finger_table = [None] * 8
        self.finger_table[0] = self.successor
        for i in range(1, 8):
            id = (self.id + 2**i) % 2**8
            self.finger_table[i] = self.find_successor(id)

    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return self.successor.get(key)

    def put(self, key, value):
        if key in range(self.id, self.successor.id):
            self.data[key] = value
        else:
            self.successor.put(key, value)

class Ring:
    def __init__(self):
        self.nodes = []
        self.hash_function = hashlib.sha256

    def add_node(self):
        id = random.randint(0, 2**8 - 1)
        node = Node(id)
        self.nodes.append(node)
        node.join(self)
        return node

    def remove_node(self, node):
        self.nodes.remove(node)
        node.predecessor.successor = node.successor
        node.successor.predecessor = node.predecessor
        node.predecessor.update_finger_table()
        node.successor.update_finger_table()

    def get_node(self, id):
        return min(self.nodes, key=lambda node: abs(node.id - id))
    
    def get(self, key):
        return self.get_node(key).get(key)
    
    def put(self, key, value):
        return self.get_node(key).put(key, value)
    
    def print_ring(self):
        for node in self.nodes:
            print(node.id, node.successor.id, node.predecessor.id)
        print()

# Testing the Chord Ring
ring = Ring()
for i in range(5):
    ring.add_node()
ring.print_ring()




