# Alessandro Condina
# K Dimensional tree class

from Node import Node


class KdTree:
    def __init__(self, patients):
        self.root = self.insert(patients, 0)

    def insert(self, patients, level):
        if len(patients) == 0:
            return None

        attribute = level % 30
        median = len(patients) // 2

        # Sort patients based on the current attribute
        patients.sort(key=lambda p: p.attributes[attribute])
        node = Node(patient=patients[median])

        # Recursively build the tree
        node.left = self.insert(patients[:median], level + 1)
        node.right = self.insert(patients[median + 1:], level + 1)
        return node

    def search(self, node, test, level):
        if node is None:
            return

        distance = self.distance(node.patient, test)
        attribute = level % 30

        # Determine which side to search
        next_node = node.left if test.attributes[attribute] < node.patient.attributes[attribute] else node.right
        other_node = node.right if next_node == node.left else node.left

        # Recur down the tree
        self.search(next_node, test, level + 1)

    def distance(self, patient1, patient2):
        return sum((patient1.attributes[i] - patient2.attributes[i]) ** 2 for i in range(30)) ** 0.5
