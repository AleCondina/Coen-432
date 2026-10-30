# Alessandro Condina
# This file handles the project data.

import pandas
from Patient import Patient


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_patient_from_csv(self):
        data = pandas.read_csv(self.file_path)
        patients = []

        for _, row in data.iterrows():
            patient = Patient(
                row['id'], row['diagnosis'], row['radius_mean'], row['texture_mean'],
                row['perimeter_mean'], row['area_mean'], row['smoothness_mean'], row['compactness_mean'],
                row['concavity_mean'], row['concave points_mean'], row['symmetry_mean'], row['fractal_dimension_mean'],
                row['radius_se'], row['texture_se'], row['perimeter_se'], row['area_se'],
                row['smoothness_se'], row['compactness_se'], row['concavity_se'], row['concave points_se'],
                row['symmetry_se'], row['fractal_dimension_se'], row['radius_worst'], row['texture_worst'],
                row['perimeter_worst'], row['area_worst'], row['smoothness_worst'], row['compactness_worst'],
                row['concavity_worst'], row['concave points_worst'], row['symmetry_worst'],
                row['fractal_dimension_worst']
            )
            patients.append(patient)

        return patients

    def process_data(self, target_column, training_instances):

        data = pandas.read_csv(self.file_path)

        # drops the id column because there's no use for it
        if 'id' in data.columns:
            data = data.drop(columns=['id'])

        # encodes target variable M: malignant & B: benign so the functions interpret them properly
        if target_column not in data.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset.")
        data[target_column] = data[target_column].map({'M': 1, 'B': 0})

        # separate the target from features to ensure unbiased results
        features = data.drop(columns=[target_column])
        target = data[target_column]

        # calculates the test size based of training size
        testing_instances = training_instances // 4

        if training_instances + testing_instances > len(data):
            raise ValueError("Not enough instances in the dataset for the specified training size.")

        # randomly select training and testing instances
        selected_instances = data.sample(n=testing_instances + training_instances, random_state=89).index
        features_selected = features.loc[selected_instances]
        target_selected = target.loc[selected_instances]

        # split the data into training and testing sets
        feature_train = features_selected.iloc[:training_instances]
        feature_test = features_selected.iloc[training_instances:]
        target_train = target_selected.iloc[:training_instances]
        target_test = target_selected.iloc[training_instances:]

        return feature_train, feature_test, target_train, target_test







