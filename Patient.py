# This is a patient class that creates patient objects
# and initializes the 30 attributes
import pandas


class Patient:
    def __init__(self, patient_id, diagnosis, radius_mean, texture_mean, perimeter_mean,
                 area_mean, smoothness_mean, compactness_mean, concavity_mean,
                 concave_points_mean, symmetry_mean, fractal_dimension_mean, radius_se,
                 texture_se, perimeter_se, area_se, smoothness_se, compactness_se, concavity_se,
                 concave_points_se, symmetry_se, fractal_dimension_se, radius_worst, texture_worst,
                 perimeter_worst, area_worst, smoothness_worst, compactness_worst, concavity_worst,
                 concave_points_worst, symmetry_worst, fractal_dimension_worst):

        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.radius_mean = radius_mean
        self.texture_mean = texture_mean
        self.perimeter_mean = perimeter_mean
        self.area_mean = area_mean
        self.smoothness_mean = smoothness_mean
        self.compactness_mean = compactness_mean
        self.concavity_mean = concavity_mean
        self.concave_points_mean = concave_points_mean
        self.symmetry_mean = symmetry_mean
        self.fractal_dimension_mean = fractal_dimension_mean
        self.radius_se = radius_se
        self.texture_se = texture_se
        self.perimeter_se = perimeter_se
        self.area_se = area_se
        self.smoothness_se = smoothness_se
        self.compactness_se = compactness_se
        self.concavity_se = concavity_se
        self.concave_points_se = concave_points_se
        self.symmetry_se = symmetry_se
        self.fractal_dimension_se = fractal_dimension_se
        self.radius_worst = radius_worst
        self.texture_worst = texture_worst
        self.perimeter_worst = perimeter_worst
        self.area_worst = area_worst
        self.smoothness_worst = smoothness_worst
        self.compactness_worst = compactness_worst
        self.concavity_worst = concavity_worst
        self.concave_points_worst = concave_points_worst
        self.symmetry_worst = symmetry_worst
        self.fractal_dimension_worst = fractal_dimension_worst

    # This function prints all the patient attributes
    def print_patient(self):
        print(f"{self.patient_id}, {self.diagnosis}, {self.radius_mean}, {self.texture_mean}, "
              f"{self.perimeter_mean}, {self.area_mean}, {self.smoothness_mean}, {self.compactness_mean}, "
              f"{self.concavity_mean}, {self.concave_points_mean}, {self.symmetry_mean}, "
              f"{self.fractal_dimension_mean}, {self.radius_se}, {self.texture_se}, {self.perimeter_se}, "
              f"{self.area_se}, {self.smoothness_se}, {self.compactness_se}, {self.concavity_se}, "
              f"{self.concave_points_se}, {self.symmetry_se}, {self.fractal_dimension_se}, "
              f"{self.radius_worst}, {self.texture_worst}, {self.perimeter_worst}, {self.area_worst}, "
              f"{self.smoothness_worst}, {self.compactness_worst}, {self.concavity_worst}, "
              f"{self.concave_points_worst}, {self.symmetry_worst}, {self.fractal_dimension_worst}")


# This function creates patient object and initializes their attributes from a CSV file
def create_patient_from_csv(file_path):
    data = pandas.read_csv(file_path)
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
            row['concavity_worst'], row['concave points_worst'], row['symmetry_worst'], row['fractal_dimension_worst']
        )
        patients.append(patient)

    return patients
