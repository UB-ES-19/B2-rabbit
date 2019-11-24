class Node:
    def __init__(self, obj, parent=None):
        self.value = obj
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)
