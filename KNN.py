# Alessandro Condina

import random
import heapq
import numpy as np
from Kdtree import *
from Node import Node


class KNN:
    def __init__(self, patients, num_neighbors):
        self.num_neighbors = num_neighbors
        self.neighbors = []
        self.right = 0
        self.wrong = 0
        self.accuracy = 0

        # Shuffle the patients
        shuffled_patients = self.shuffle_array(patients)

        # Split into training (75%) and testing (25%) sets
        split_index = len(shuffled_patients) - len(shuffled_patients) // 4
        train = shuffled_patients[:split_index]
        self.test = shuffled_patients[split_index:]

        # Build the K-d tree with the training data
        self.tree = KdTree(train)

        # Perform KNN classification for each test patient
        for test_patient in self.test:
            self.neighbors = []  # Reset neighbors for each test patient
            self.search(self.tree.root, test_patient, 0)
            self.vote(self.neighbors)

        # Calculate accuracy
        print(f"wrong: {self.wrong} right: {self.right} length of test: {len(self.test)}")
        self.accuracy = (self.right / len(self.test)) * 100
        rounded_accuracy = round(self.accuracy, 2)
        print(f"Test accuracy: {rounded_accuracy}%")

    def shuffle_array(self, patients):
        """Shuffles the list of patients in place and returns it."""
        random.shuffle(patients)
        return patients

    def distance(self, patient1, patient2):
        """Calculates Euclidean distance between two patients."""
        return np.sqrt(
            (patient1.radius_mean - patient2.radius_mean) ** 2 +
            (patient1.texture_mean - patient2.texture_mean) ** 2 +
            (patient1.perimeter_mean - patient2.perimeter_mean) ** 2 +
            (patient1.area_mean - patient2.area_mean) ** 2 +
            (patient1.smoothness_mean - patient2.smoothness_mean) ** 2 +
            (patient1.compactness_mean - patient2.compactness_mean) ** 2 +
            (patient1.concavity_mean - patient2.concavity_mean) ** 2 +
            (patient1.concave_points_mean - patient2.concave_points_mean) ** 2 +
            (patient1.symmetry_mean - patient2.symmetry_mean) ** 2 +
            (patient1.fractal_dimension_mean - patient2.fractal_dimension_mean) ** 2 +
            (patient1.radius_se - patient2.radius_se) ** 2 +
            (patient1.texture_se - patient2.texture_se) ** 2 +
            (patient1.perimeter_se - patient2.perimeter_se) ** 2 +
            (patient1.area_se - patient2.area_se) ** 2 +
            (patient1.smoothness_se - patient2.smoothness_se) ** 2 +
            (patient1.compactness_se - patient2.compactness_se) ** 2 +
            (patient1.concavity_se - patient2.concavity_se) ** 2 +
            (patient1.concave_points_se - patient2.concave_points_se) ** 2 +
            (patient1.symmetry_se - patient2.symmetry_se) ** 2 +
            (patient1.fractal_dimension_se - patient2.fractal_dimension_se) ** 2 +
            (patient1.radius_worst - patient2.radius_worst) ** 2 +
            (patient1.texture_worst - patient2.texture_worst) ** 2 +
            (patient1.perimeter_worst - patient2.perimeter_worst) ** 2 +
            (patient1.area_worst - patient2.area_worst) ** 2 +
            (patient1.smoothness_worst - patient2.smoothness_worst) ** 2 +
            (patient1.compactness_worst - patient2.compactness_worst) ** 2 +
            (patient1.concavity_worst - patient2.concavity_worst) ** 2 +
            (patient1.concave_points_worst - patient2.concave_points_worst) ** 2 +
            (patient1.symmetry_worst - patient2.symmetry_worst) ** 2 +
            (patient1.fractal_dimension_worst - patient2.fractal_dimension_worst) ** 2)

    def search(self, node, test_patient, level):
        """Recursively search for the k-nearest neighbors in the K-d tree."""
        if node is None:
            return

        # Calculate distance from the current node to the test patient
        distance = self.distance(node.patient, test_patient)

        # Add the current node to the priority queue if it is closer than the current k-nearest
        if len(self.neighbors) < self.num_neighbors or distance < -self.neighbors[0][0]:
            heapq.heappush(self.neighbors, (-distance, node))
            if len(self.neighbors) > self.num_neighbors:
                heapq.heappop(self.neighbors)

        # Determine the attribute to split by
        attribute = level % len(test_patient.attributes)

        # Choose the next subtree to search
        if test_patient.attributes[attribute] < node.patient.attributes[attribute]:
            next_node = node.left
            other_node = node.right
        else:
            next_node = node.right
            other_node = node.left

        # Recur on the chosen subtree
        self.search(next_node, test_patient, level + 1)

        # Check the other subtree if necessary
        if len(self.neighbors) < self.num_neighbors or abs(
                test_patient.attributes[attribute] - node.patient.attributes[attribute]) < -self.neighbors[0][0]:
            self.search(other_node, test_patient, level + 1)

    def vote(self, neighbors):
        """Vote based on the k-nearest neighbors to classify the test patient."""
        m_count = 0
        b_count = 0

        # Check if neighbors list is populated correctly
        if not neighbors:
            print("No neighbors found!")
            return

        real_diagnosis = neighbors[0][1].patient.diagnosis

        while neighbors:
            _, node = heapq.heappop(neighbors)
            print(f"Neighbor diagnosis: {node.patient.diagnosis}")
            if node.patient.diagnosis == 'M':
                m_count += 1
            else:
                b_count += 1

        if m_count > b_count:
            prediction = "M"
        else:
            prediction = "B"
        print(f"Predicted: {prediction}, Actual: {real_diagnosis}")

        if prediction == real_diagnosis:
            self.right += 1
        else:
            self.wrong += 1

