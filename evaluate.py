"""Reproduce the README benchmark without modifying the original assignment."""
import contextlib
import hashlib
import io
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'Program files'))
from KNN import KNN
from Kdtree import KdTree
from Patient import Patient


def metrics(y, pred, scores=None):
    return dict(accuracy=accuracy_score(y, pred),
                precision=precision_score(y, pred, zero_division=0),
                recall=recall_score(y, pred, zero_division=0),
                f1=f1_score(y, pred, zero_division=0),
                roc_auc=roc_auc_score(y, scores) if scores is not None else None,
                confusion_matrix=confusion_matrix(y, pred, labels=[0, 1]).tolist())


def custom_predict(train, labels, test, k):
    # Reuse the assignment's tree search and voting with the benchmark's fixed split.
    # Its constructor otherwise shuffles and selects a different train/test subset.
    patients = [Patient(i, 'M' if y else 'B', *row) for i, (row, y) in enumerate(zip(train, labels))]
    model = KNN.__new__(KNN)
    model.num_neighbors = k
    model.tree = KdTree(patients)
    model.predictions, model.true_labels = [], []
    model.right = model.wrong = 0
    for i, row in enumerate(test):
        model.neighbors = []
        patient = Patient(i, 'B', *row)
        model.search(model.tree.root, patient, 0)
        # vote's actual-label argument affects bookkeeping only, not prediction.
        model.vote(model.neighbors, 'B')
    return np.array([int(p == 'M') for p in model.predictions])


def main():
    path = ROOT / 'training data' / 'data.csv'
    data = pd.read_csv(path)
    X = data.drop(columns=['id', 'diagnosis'])
    y = data.diagnosis.map({'B': 0, 'M': 1})
    if X.isna().any().any() or y.isna().any():
        raise ValueError('Unexpected missing features or diagnosis labels')
    reference = load_breast_cancer()
    assert np.allclose(X.to_numpy(), reference.data)
    assert np.array_equal(y.to_numpy(), 1 - reference.target)
    train, test = train_test_split(np.arange(len(data)), test_size=0.2, stratify=y, random_state=89)
    assert not set(train) & set(test)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=89)
    results = {}
    dummy = DummyClassifier(strategy='most_frequent').fit(X.iloc[train], y.iloc[train])
    results['Majority baseline'] = metrics(y.iloc[test], dummy.predict(X.iloc[test]), dummy.predict_proba(X.iloc[test])[:, 1])
    grids = {
        'SVM': (SVC(), [dict(model__kernel=['linear'], model__C=[0.1, 1, 10, 100]),
                       dict(model__kernel=['rbf'], model__C=[0.1, 1, 10, 100], model__gamma=['scale', 'auto'])]),
        'KNN reference': (KNeighborsClassifier(), dict(model__n_neighbors=list(range(1, 26, 2))))
    }
    for name, (estimator, grid) in grids.items():
        search = GridSearchCV(Pipeline([('scale', StandardScaler()), ('model', estimator)]), grid,
                              cv=cv, scoring='f1', n_jobs=1)
        search.fit(X.iloc[train], y.iloc[train])
        best = search.best_estimator_
        scores = best.decision_function(X.iloc[test]) if name == 'SVM' else best.predict_proba(X.iloc[test])[:, 1]
        pred = best.predict(X.iloc[test])
        results[name] = metrics(y.iloc[test], pred, scores)
        results[name].update(best_parameters=search.best_params_, cv_f1=search.best_score_)
        if name == 'KNN reference':
            scale = best.named_steps['scale']
            with contextlib.redirect_stdout(io.StringIO()):
                custom = custom_predict(scale.transform(X.iloc[train]), y.iloc[train].to_numpy(),
                                        scale.transform(X.iloc[test]), search.best_params_['model__n_neighbors'])
            assert np.array_equal(custom, pred), 'Custom/reference predictions differ'
            results['Custom k-d tree KNN'] = metrics(y.iloc[test], custom)
            results['Custom k-d tree KNN']['matches_reference_predictions'] = bool(np.array_equal(custom, pred))
            results['Custom k-d tree KNN']['k'] = search.best_params_['model__n_neighbors']
    output = dict(dataset_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  versions=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__, sklearn=sklearn.__version__),
                  seed=89, positive_label='M', rows=len(data), features=X.shape[1],
                  train_rows=len(train), test_rows=len(test),
                  train_record_ids=data.iloc[train].id.tolist(), test_record_ids=data.iloc[test].id.tolist(), results=results)
    dest = ROOT / 'results' / 'benchmark.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
