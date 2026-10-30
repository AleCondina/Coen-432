# Alessandro Condina
# Support Vector Machine class implements the scikit API

from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score


class SVM:
    def __init__(self, kernel, C=1.0, gamma='scale'):
        """
        Initializes the SVM model with configurable hyperparameters.
        Parameters:
            kernel (str): Specifies the kernel type to be used ('linear', 'rbf', etc.).
            C (float): Regularization parameter.
            gamma (str or float): Kernel coefficient for 'rbf', 'poly', and 'sigmoid'.
        """
        self.model = SVC(kernel=kernel, C=C, gamma=gamma, probability=True)

    def train(self, feature_train, target_train):

        self.model.fit(feature_train, target_train)
        print("SVM training complete.")

    def predict(self, feature_test):
        return self.model.predict(feature_test)

    def evaluate(self, feature_test, target_test):

        y_pred = self.predict(feature_test)
        accuracy = round(accuracy_score(target_test, y_pred) * 100, 2)
        report = classification_report(target_test, y_pred, output_dict=True)

        try:
            roc_auc = roc_auc_score(target_test, self.model.predict_proba(feature_test)[:, 1])
        except ValueError:
            roc_auc = None

        print("Classification Report:")
        print(classification_report(target_test, y_pred))
        if roc_auc is not None:
            print(f"ROC-AUC Score: {roc_auc:.2f}")

        return {
            'accuracy': accuracy,
            'precision': report['weighted avg']['precision'],
            'recall': report['weighted avg']['recall'],
            'f1-score': report['weighted avg']['f1-score'],
            'roc_auc': roc_auc
        }
