# Alessandro Condina

from Patient import *


class DistanceToNode:

    def __init__(self, train_node, test, distance):
        self.train_node = train_node
        self.test = test
        self.distance = distance

    def get_distance(self):
        return self.distance

    def get_train_node(self):
        return self.train_node.Patient.patient_id

    def get_test_patient(self):
        return self.test.id

    def get_diagnosis(self):
        return self.train_node.Patient.diagnosis
