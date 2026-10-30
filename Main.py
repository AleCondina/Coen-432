# Alessandro Condina
# Main entry point for the program to run
import pandas as pd
from Patient import create_patient_from_csv
from KNN import KNN

# Creates a list of Patients that have all 30 attributes
# patient = create_patient_from_csv("/training data/data.csv")
#
# M = 0
# B = 0
#
# # Load your dataset
# data = pd.read_csv('training data/data.csv')
#
# # Display the initial shape of the dataset
# print(f"Original dataset size: {data.shape[0]} patients")
#
# # Remove patients where any attribute value is 0
# data = data[(data != 0).all(axis=1)]
#
# # Display the new shape of the dataset after filtering
# print(f"Filtered dataset size: {data.shape[0]} patients")
#
# # Optional: Save the cleaned dataset to a new CSV file
# data.to_csv('cleaned_breast_cancer_data.csv', index=False)

patient = create_patient_from_csv("training data/cleaned_breast_cancer_data.csv")

knn = KNN(patient, 4)

# for p in patient:
#     if p.diagnosis == "M":
#         M += 1
#     else:
#         B += 1
#
# print(f"there are {M} M patients and {B} B patients")

