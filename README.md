# Breast Cancer Classification: KNN and SVM

Academic project for COEN 432 at Concordia University by Alessandro Condina.
Implements a custom K-nearest neighbours classifier using a k-d tree, alongside
scikit-learn SVM classification and hyperparameter search.

## Setup and run

Python 3.12 or later is required (the grid-search code uses Python 3.12 f-string syntax).
From the repository root:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python "Program files/Main.py"
```

Select `KNN model`, `SVM model`, `KNN gridsearch`, or `SVM gridsearch`.
After an experiment, enter `exit` to quit. Grid searches can take substantial time.
Data paths resolve relative to the source file, independent of your working directory.

## Data

The bundled CSV files contain breast-cancer measurements, diagnosis labels, and
numeric record identifiers. They have the Wisconsin Diagnostic Breast Cancer
feature schema. The original download source and redistribution terms were not
recorded in this repository and still need verification. These are dataset record
IDs, not this project's author's student ID. The model excludes the ID feature.

The original assignment notes state that 13 benign records with six missing
attributes were removed to produce the cleaned CSV. That preprocessing has not
been independently reproduced here.

## Evaluation and limitations

SVM uses five-fold `GridSearchCV` on training data, followed by evaluation on a
separate sampled test subset. The custom KNN search compares multiple settings
against repeatedly sampled test subsets; its best score is a tuning result,
not an unbiased final test estimate. Features are not standardized, which affects
Euclidean distance and SVM behaviour. KNN sampling is not seeded.

The KNN evaluation was corrected to compare predictions with each test record's
actual diagnosis. Earlier reported KNN results should be recomputed. No verified
benchmark accuracy is claimed in this README. This is educational software and
has not been validated for clinical use.

## References

- [SVM API](https://scikit-learn.org/stable/api/sklearn.svm.html)
- [Metrics API](https://scikit-learn.org/stable/api/sklearn.metrics.html)
- [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)
