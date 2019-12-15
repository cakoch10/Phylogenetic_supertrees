class Node(object):
    def __init__(self, key):
        self.key = key
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def to_string(self):
        