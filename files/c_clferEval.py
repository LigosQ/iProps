#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 19:40:21 2023
@author: sealight
"""
import math
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
from sklearn.metrics import confusion_matrix,roc_curve, auc
class Error_coding(Exception):
    pass
def f_getIndOfList(s_findStr, ls_allStr):
    for ind,s_item in enumerate(ls_allStr):
        if s_findStr == s_item:
            return ind
    return -1
def f_evalData_ByClfier(X_train, y_train, X_test, y_test,s_clfier):
    # print(s_clfier)
    # ls_clfNames = [
    #     "Nearest Neighbors",
    #     "SVM(linear)",
    #     "RBF SVM",
    #     "Gaussian Process",
    #     "Decision Tree",
    #     "Random Forest",
    #     "Neural Net",
    #     "AdaBoost",
    #     "Naive Bayes",
    #     "QDA",
    #     "xgboost",
    # ]
    # i_indClfier = f_getIndOfList(s_clfier, ls_clfNames)
    # if i_indClfier==0:
    #     obj_clf = KNeighborsClassifier(3)
    # elif i_indClfier==1:
    #     obj_clf = SVC(kernel="linear", C=0.025,probability=True)
    # elif i_indClfier==2:
    #     obj_clf = SVC(gamma=2, C=1,probability=True)
    # elif i_indClfier==3:
    #     obj_clf = GaussianProcessClassifier(1.0 * RBF(1.0))
    # elif i_indClfier==4:
    #     obj_clf = DecisionTreeClassifier(max_depth=5)
    # elif i_indClfier==5:
    #     obj_clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
    # elif i_indClfier==6:
    #     obj_clf = MLPClassifier(alpha=1, max_iter=1000)
    # elif i_indClfier==7:
    #     obj_clf = AdaBoostClassifier()
    # elif i_indClfier==8:
    #     obj_clf = GaussianNB()
    # elif i_indClfier==9:
    #     obj_clf = QuadraticDiscriminantAnalysis()
    # elif i_indClfier==10:
    #     from xgboost.sklearn import XGBClassifier
    #     obj_clf = XGBClassifier(max_depth=5)
    # elif i_indClfier==-1:
    #     raise Error_coding('Your given classifier string cannot be found in the list')
    # else:
    #     raise Error_coding('The f_getIndOfList function produces a wrong return-value')
    try:
        from files.class_mlClassifier import c_mlClassifier
    except:
        from class_mlClassifier import c_mlClassifier
    clf = c_mlClassifier(s_clfier).f_geneMlClassifier(None)
    # clf = obj_clf
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    y_predict = clf.predict(X_test)
    m_confMatrix = confusion_matrix(y_test, y_predict)
    ls_probab = clf.predict_proba(X_test)
    return y_predict, score,ls_probab, m_confMatrix
def f_clacSn_4matrics(ls_confusMat_4elms):
    tp, fp, fn, tn = ls_confusMat_4elms[0], ls_confusMat_4elms[1], ls_confusMat_4elms[2], ls_confusMat_4elms[3]
    if (tp+fn)==0:
        sn = 0
    else:
        sn = tp/(tp+fn)
    if (tn+fp)==0:
        sp = 0
    else:
        sp = tn/(tn+fp)    
    if ((tp+fn)*(tn+fn)*(tp+fp)*(tn+fp))==0:
        mcc = 0
    else:
        mcc = (tp*tn-fp*fn)/math.sqrt((tp+fn)*(tn+fn)*(tp+fp)*(tn+fp))
    acc = (tp+tn)/(tp+fp+fn+tn)
    return sn, sp, acc, mcc
def f_calcPermCalc(m_confMatrix):
    ls_confusMat_allElems = []
    ls_confusMat_expanded = m_confMatrix.tolist()
    for i in range(len(ls_confusMat_expanded)):
        ls_curElem = ls_confusMat_expanded[i]
        for j in range(len(ls_curElem)):
            i_curElem = ls_curElem[j]
            ls_confusMat_allElems.append(i_curElem)
    sn, sp, acc, mcc = f_clacSn_4matrics(ls_confusMat_allElems)
    return sn, sp, acc, mcc
def f_evalDf_ByClfier(df_feat,s_clfier, ls_kFold):
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
    ]
    i_indClfier = f_getIndOfList(s_clfier, ls_clfNames)
    if i_indClfier==0:
        obj_clf = KNeighborsClassifier(3)
    elif i_indClfier==1:
        obj_clf = SVC(kernel="linear", C=0.025,probability=True)
    elif i_indClfier==2:
        obj_clf = SVC(gamma=2, C=1,probability=True)
    elif i_indClfier==3:
        obj_clf = GaussianProcessClassifier(1.0 * RBF(1.0))
    elif i_indClfier==4:
        obj_clf = DecisionTreeClassifier(max_depth=5)
    elif i_indClfier==5:
        obj_clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
    elif i_indClfier==6:
        obj_clf = MLPClassifier(alpha=1, max_iter=1000)
    elif i_indClfier==7:
        obj_clf = AdaBoostClassifier()
    elif i_indClfier==8:
        obj_clf = GaussianNB()
    elif i_indClfier==9:
        obj_clf = QuadraticDiscriminantAnalysis()
    elif i_indClfier==-1:
        raise Error_coding('Your given classifier string cannot be found in the list')
    else:
        raise Error_coding('The f_getIndOfList function produces a wrong return-value')
    ser_y = df_feat['class']
    ser_X = df_feat.drop(columns=['class'])
    ls_pred_y = []
    ls_real_y = []
    ls_probVal_y = []
    for k,(ls_trainInd, ls_testInd) in enumerate(ls_kFold):
        X_train, X_test = ser_X[ls_trainInd], ser_X[ls_testInd]
        y_train, y_test = ser_y[ls_trainInd], ser_y[ls_testInd]
        ls_real_y.extend(y_test)
        obj_clf.fit(X_train, y_train)
        y_predict = obj_clf.predict(X_test)
        ls_pred_y.extend(y_predict)
        ls_probab = obj_clf.predict_proba(X_test)
        ls_probVal_y.extend(ls_probab[:,1])
    m_confMatrix = confusion_matrix(ls_real_y, ls_pred_y)
    fpr,tpr,threshold = roc_curve(ls_real_y, ls_probVal_y) 
    roc_auc = auc(fpr,tpr) 
    sn, sp, acc, mcc = f_calcPermCalc(m_confMatrix)
    return sn, sp, acc, mcc, roc_auc
    