# Coen-432 Assignment 2 
Alessandro Condina 

The bonus project meant for the grad students was completed. Two models are included
to make predications; SVM and KNN. The optimization of parameters was done using a 
grid search.

# Dependencies
A library was used for SVM and SVM grid search. 
run: pip install scikit-learn
to download the library so that the program can run

# Data.csv 
removed 13 patients with 6 attributes missing. 
All of these patients have a benign 
diagnosis, and given that the data set is 
primarily benign and large enough, 
these patients were ultimately excluded.

# Resources

These are the links to libraries used:\
SVM: https://scikit-learn.org/stable/api/sklearn.svm.htmlhttps://scikit-learn.org/stable/api/sklearn.svm.html

Metrics: https://scikit-learn.org/stable/api/sklearn.metrics.htmlhttps://scikit-learn.org/stable/api/sklearn.metrics.html

Grid Search: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
