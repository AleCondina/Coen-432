# Alessandro Condina
# Grid search class for KNN and SVM. SVM grid search implemented with scikit API

from DataLoader import DataLoader
import time
from KNN import KNN
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

class GridSearch:
    def __init__(self, model):
        if model not in ['KNN', 'SVM']:
            raise ValueError("You must enter either: 'KNN' or 'SVM'")
        else:
            self.model = model

    def evaluate(self):

        if self.model == 'KNN':
            # Define hyperparameters and values to be tested
            hyperparameters = {'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]}

            # Track the best performance
            best_accuracy = 0
            best_hyperparameters = None
            results = []

            data = DataLoader("../training data/cleaned_breast_cancer_data.csv")

            N = 40
            patient = data.create_patient_from_csv()

            while N != 540:

                for neighbors in hyperparameters['n_neighbors']:

                    start_time = time.time()
                    # runs the KNN algorithm
                    knn = KNN(patient, neighbors, N)
                    end_time = time.time()
                    print(f"Hyperparameters for {N} training instances: {neighbors}")
                    print(f"Execution time: {end_time - start_time} seconds")
                    print("________________________________________________________")
                    accuracy = knn.get_accuracy()

                    # Check if this run is the best
                    if accuracy >= best_accuracy:
                        best_accuracy = accuracy
                        best_hyperparameters = {'n_neighbors': neighbors}

                results.append({
                    'training_instances': N,
                    'best_accuracy': best_accuracy,
                    'best_hyperparameters': best_hyperparameters
                })
                N += 100
            print("Grid search results for KNN")
            print("________________________________________________________")
            print(f"{"training_instances":<20}{"best_accuracy":<15}{"best_hyperparameters":<25}")

            for result in results:
                training_instances = result['training_instances']
                best_accuracy = result['best_accuracy']
                best_hyperparameters = result['best_hyperparameters']
                print(f"{training_instances:<20}{best_accuracy:<15}{str(best_hyperparameters):<25}")


        elif self.model == 'SVM':

            data = DataLoader("../training data/cleaned_breast_cancer_data.csv")

            N = 40

            while N != 540:
                print(f"Grid search for {N} training instances")
                # Split data into train and test sets
                feature_train, feature_test, target_train, target_test = data.process_data(
                    target_column='diagnosis', training_instances=N)

                # Define the parameter grid
                param_grid = {
                    'C': [0.1, 1, 10, 100],
                    'kernel': ['linear', 'rbf'],
                    'gamma': ['scale', 'auto']
                }

                # Initialize the SVM model
                svm = SVC()

                # Set up the grid search
                grid_search = GridSearchCV(
                    estimator=svm,
                    param_grid=param_grid,
                    scoring='accuracy',
                    cv=5,  # 5-fold cross-validation
                    verbose=1,
                    n_jobs =-1 # Enable multithreading (use all CPU cores)
                )

                # Fit grid search
                grid_search.fit(feature_train, target_train)

                # Get the best parameters and score
                print("Best Parameters:", grid_search.best_params_)
                print("Best Cross-Validation Accuracy:", grid_search.best_score_)

                # Evaluate on test set
                best_model = grid_search.best_estimator_
                test_accuracy = best_model.score(feature_test, target_test)
                print("Test Accuracy:", test_accuracy, "\n")
                N += 100

        else:
            print("Invalid model. Please choose either 'KNN' or 'SVM'.")
