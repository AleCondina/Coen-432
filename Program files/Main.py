# Alessandro Condina
# Main entry point for the program to run

from DataLoader import DataLoader
from SVM import SVM
from KNN import KNN
import time
from GridSearch import GridSearch

data = DataLoader("../training data/cleaned_breast_cancer_data.csv")

print("Assignment 2\nDeveloped by Alessandro Condina")

selection = input(
    "What would you like to demo (choose from the following)?:\n"
    "- KNN gridsearch\n- SVM gridsearch\n- KNN model\n- SVM model\n"
    "Enter your choice: "
)

while selection not in ["KNN gridsearch", "SVM gridsearch", "KNN model", "SVM model"]:
    selection = input(
        "Invalid choice. Please choose from the following:\n"
        "- KNN gridsearch\n- SVM gridsearch\n- KNN model\n- SVM model\n"
        "Enter your choice: "
    )

while selection != "exit":

    if selection == "KNN gridsearch":
        print("\nStarting KNN Grid Search...\n")
        KNN_grid_search = GridSearch(model="KNN")
        KNN_grid_search.evaluate()

    elif selection == "SVM gridsearch":
        print("\nStarting SVM Grid Search...\n")
        SVM_grid_search = GridSearch(model="SVM")
        SVM_grid_search.evaluate()

    elif selection == "KNN model":
        print("\nRunning KNN Model...\n")

        patients = data.create_patient_from_csv()

        while True:
            try:
                N = int(input("Enter the number of training instances (40-440): "))
                if 40 <= N <= 440:
                    break  # Valid input, exit the loop
                else:
                    print("Invalid input. Please enter a number between 40 and 440.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        while True:
            try:
                neighbors = int(input("Enter the number of neighbors: "))
                if 0 <= N-1:
                    break
                else:
                    print("Invalid input.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        start_time = time.time()
        knn = KNN(patients, neighbors, N)
        accuracy = knn.get_accuracy()
        end_time = time.time()

        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Execution time: {round((end_time - start_time) * 1000, 2)} milliseconds\n")

    elif selection == "SVM model":
        print("\nRunning SVM Model...\n")

        while True:
            try:
                N = int(input("Enter the number of training instances (40-440): "))
                if 40 <= N <= 440:
                    break
                else:
                    print("Invalid input. Please enter a number between 40 and 440.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        kernel = input("Enter an SVM kernel (rbf, linear): ")
        while kernel not in ["rbf", "linear"]:
            kernel = input("Invalid input. Enter an SVM kernel (rbf, linear): ")

        while True:
            try:
                C = float(input("Choose a value for the decision boundary (lower is more generalized, higher is more precise).\n"
                  "Suggested values: 0.1, 1, 10, 100: "))
                if 0 <= N <= 100000:
                    break
                else:
                    print("Invalid input. Suggested values: 0.1, 1, 10, 100: ")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        feature_train, feature_test, target_train, target_test = data.process_data(
            target_column="diagnosis", training_instances=N
        )

        svm = SVM(kernel=kernel, C=C, gamma="scale")

        start_time = time.time()
        svm.train(feature_train, target_train)
        results = svm.evaluate(feature_test, target_test)
        end_time = time.time()

        print("Evaluation Results:", results)
        print(f"Execution time: {round((end_time - start_time) * 1000, 2)} milliseconds\n")

    selection = input("If you want to exit, type 'exit'. To perform another task, choose from the following:\n"
                      "- KNN gridsearch\n- SVM gridsearch\n- KNN model\n- SVM model\n"
                      "Enter your choice: ")

print("Program ended...")
exit()
