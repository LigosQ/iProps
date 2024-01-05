#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 05:56:45 2023
@author: sealight
"""
"""
Created on Tue Feb  7 19:40:21 2023
@author: sealight
"""
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
class Error_coding(Exception):
    pass
def f_getIndOfList(s_findStr, ls_allStr):
    for ind,s_item in enumerate(ls_allStr):
        if s_findStr == s_item:
            return ind
    return -1
def f_geneClfier_byStr(s_clfier):
    ls_clfNames = [
        "Nearest Neighbors",
        "SVM(linear)",
        "RBF SVM",
        "Gaussian Process",
        "Decision Tree",
        "Random Forest",
        "Neural Net",
        "AdaBoost",
        "Naive Bayes",
        "QDA",
        "xgboost"
    ]
    i_indClfier = f_getIndOfList(s_clfier, ls_clfNames)
    if i_indClfier==0:
        obj_clf = KNeighborsClassifier(weights='distance')
    elif i_indClfier==1:
        obj_clf = SVC(kernel="linear", C=0.025,probability=True)
    elif i_indClfier==2:
        obj_clf = SVC(gamma=2, C=1,probability=True)
    elif i_indClfier==3:
        obj_clf = GaussianProcessClassifier(1.0 * RBF(1.0))
    elif i_indClfier==4:
        obj_clf = DecisionTreeClassifier()
    elif i_indClfier==5:
        obj_clf = RandomForestClassifier()
    elif i_indClfier==6:
        obj_clf = MLPClassifier(alpha=1, max_iter=1000)
    elif i_indClfier==7:
        obj_clf = AdaBoostClassifier()
    elif i_indClfier==8:
        obj_clf = GaussianNB()
    elif i_indClfier==9:
        obj_clf = QuadraticDiscriminantAnalysis()
    elif i_indClfier==10:
        from xgboost.sklearn import XGBClassifier
        obj_clf = XGBClassifier(max_depth=5)
    elif i_indClfier==-1:
        raise Error_coding('Your given classifier string cannot be found in the list')
    else:
        raise Error_coding('The f_getIndOfList function produces a wrong return-value')
    return obj_clf