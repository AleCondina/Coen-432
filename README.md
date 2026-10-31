# Breast Cancer Classification: Custom KNN and SVM

A COEN 432 academic project by Alessandro Condina, with a reproducible evaluation
added after the original assignment. Predicts whether a breast-mass sample is
**malignant (M)** or **benign (B)** from 30 numeric measurements.

## What this project demonstrates

- Custom K-nearest neighbours classification with k-d tree search and majority voting.
- Support vector machines using scikit-learn, with linear and RBF kernels.
- Hyperparameter search, classification metrics, and a majority-class baseline.
- A reproducible benchmark that separates model selection from final test evaluation.

## Dataset and preprocessing

The bundled `training data/data.csv` contains **569 records**, **30 features**,
an identifier, and a diagnosis: **357 benign / 212 malignant**. Measurements
include the mean, standard error, and worst values of ten cell-nucleus properties.
The feature values and diagnosis labels were checked against scikit-learn's
`load_breast_cancer()` and match in row order (with the target encoding converted).
The original download channel was not recorded.

The source dataset is [Breast Cancer Wisconsin (Diagnostic), UCI](https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-data-set).
UCI lists it under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Dataset citation: Wolberg, W., Mangasarian, O., Street, N., & Street, W. (1993).
*Breast Cancer Wisconsin (Diagnostic)*. UCI Machine Learning Repository.
[DOI: 10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B).
The local CSV uses column names and letter diagnosis labels; the cleaned variant
also removes records as described below. Dataset licensing does not license the
project's code.

**Correction to the assignment notes:** the raw CSV contains no missing values.
The legacy `cleaned_breast_cancer_data.csv` removes 13 benign records with zero
values in six concavity-related features, leaving 556 records. Filtering raw
records with any zero feature reproduces the cleaned record set and measurements.
Zero values are not evidence of missing data. The new benchmark keeps all 569
records; the original interactive program continues to use the cleaned variant.

For the benchmark, the identifier is excluded, diagnosis is encoded as
`B=0, M=1`, and features are standardized using `StandardScaler`. The scaler is
fitted within each training fold through a pipeline, then refitted on the full
training partition. No test-set information is used to fit it. No imputation or
feature selection is applied.

## Reproduce the results

Use Python 3.12 or later. From the repository root:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-benchmark.txt
python evaluate.py
```

The script prints results and writes `results/benchmark.json`, including exact
metrics, confusion matrices, dataset SHA-256, split record IDs, selected parameters,
and runtime versions. It resolves paths relative to its own location.

## Benchmark methodology

1. Make one stratified 80/20 split with `random_state=89`: **455 training records**
   and **114 test records** (72 benign, 42 malignant).
2. Tune using five-fold shuffled stratified cross-validation on the training
   partition only, also seeded with 89. Select by **malignant-class F1**.
3. Refit each selected pipeline on all 455 training records, then evaluate on the
   same 114 test records. The test set is not used to select hyperparameters.
4. Evaluate the custom k-d tree KNN using the same scaled training/test arrays
   and the k chosen by the scikit-learn KNN reference search. Reuse the original
   tree search and voting methods while bypassing the constructor's random split.

| Model | Search space | Selected setting | Mean CV F1 |
|---|---|---|---|
| SVM | C: 0.1, 1, 10, 100; linear kernel; RBF kernel with gamma: scale, auto | RBF, C=1, gamma=scale | 0.9587 |
| KNN reference | Odd k from 1 through 25; uniform voting, Euclidean distance | k=3 | 0.9511 |
| Custom KNN | Uses reference-selected k; no separate search | k=3 | Not separately measured |

## Measured test results

Precision, recall, and F1 below use **malignant as the positive class**, rather
than weighted averages. All models share the split described above.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Majority baseline | 63.16% | 0.00% | 0.00% | 0.0000 | 0.5000 |
| SVM | 97.37% | 100.00% | 92.86% | 0.9630 | 1.0000 |
| KNN reference | 98.25% | 100.00% | 95.24% | 0.9756 | 0.9983 |
| Custom k-d tree KNN | 98.25% | 100.00% | 95.24% | 0.9756 | Not reported |

The SVM produced 72 true negatives, 39 true positives, 0 false positives, and
3 false negatives. Both KNN implementations produced 72 true negatives,
40 true positives, 0 false positives, and 2 false negatives. The custom KNN
matched all 114 reference predictions in this run.

SVM ROC-AUC uses decision scores; reference KNN uses malignant vote proportions.
Custom KNN ROC-AUC is omitted because its existing interface exposes hard labels
rather than continuous scores. AUC of 1.0 for SVM describes ranking on this small
split, not perfect thresholded classification or clinical reliability.

KNN was one correct prediction ahead of SVM on this split. That is insufficient
to establish a general performance advantage. These results are from the new
benchmark, not recovered measurements from the original submission.

## Run the original assignment

```bash
python -m pip install -r requirements.txt
python "Program files/Main.py"
```

Choose `KNN model`, `SVM model`, `KNN gridsearch`, or `SVM gridsearch`.
Enter `exit` after an experiment to quit.

The legacy program uses the 556-record cleaned variant, unscaled features, and
variable training sizes. SVM samples with seed 89 and uses five-fold GridSearchCV;
custom KNN shuffles without a fixed seed. Its legacy grid search repeatedly
compares test subsets and carries the best score across training sizes. Those
scores are not an unbiased final benchmark. Use `evaluate.py` for the table above.
Earlier KNN results also need recomputation because evaluation previously compared
predictions with a neighbour's label instead of the test record's label; that bug
has been fixed.

## Limitations and next steps

This is a small, widely used educational dataset and one fixed holdout split.
There is no external clinical validation, confidence interval, or repeated-seed
comparison. The test set should not become a target for further tuning.
Future comparisons should use nested cross-validation or a new untouched dataset.
The custom/reference agreement check covers this benchmark, not all possible
inputs, distance ties, or k values. No runtime or scalability advantage is claimed
for the custom k-d tree. This project is educational software, not a diagnostic tool.

## Implementation references

- [SVM](https://scikit-learn.org/stable/modules/svm.html)
- [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)
- [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- [Classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
