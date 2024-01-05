#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:51:14 2021
@author: tafch
"""
class ErrorUser(Exception):
    pass
class c_mlClassifier(object):
    def __init__(self,s_clfName):
        self._s_clfName = None
        if isinstance(s_clfName,str):
            self._s_clfName = s_clfName
        else:
            raise ErrorUser('The given parameter is the name of the classifier. It should be a string variable.')
    def f_geneMlClassifier(self, d_paraDict):
        s_methodName = self._s_clfName
        ls_supportMethods = ['SVM(linear)','SVM(RBF)','RF','KNN','AdaBoost','Gaussian',
                             'Neural Net', 'Naive Bayes', 'Random Forest', 'RBF SVM',
                             'Gaussian Process','QDA','Decision Tree','xgboost',
                             'Nearest Neighbors','Linear SVM','Logistic Regression',
                             'MLP Classifier','Ridge Classifier','Gradient Boosting Classifier',
                             'GaussianNB']
        ls_addmethds = ['Gradient Boosting Classifier','SVC','ExtraTreesClassifier',
                        'SGDClassifier','BernoulliNB','Perceptron',
                        'PassiveAggressiveClassifier','BaggingClassifier',
                        'CalibratedClassifierCV','ExtraTreeClassifier',
                        'NearestCentroid','LinearDiscriminantAnalysis',
                        'LabelSpreading','LabelPropagation','DummyClassifier',
                        'lightGBM']
        ls_supportMethods.extend(ls_addmethds)
        if s_methodName in ls_supportMethods:
            pass
        else:
            raise ErrorUser(f'Your given method {s_methodName} is not support in this version, please check...\n')
        match s_methodName:
            
            case ( 'RF' | 'Random Forest'):
                from sklearn.ensemble import RandomForestClassifier
                if d_paraDict is None:
                    classifier = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=1, bootstrap=True,)
                else:
                    classifier = RandomForestClassifier(n_estimators=d_paraDict['n_estimator'], 
                                                    max_depth=d_paraDict['max_depth'],
                                                    min_samples_split=d_paraDict['i_minSamples'], 
                                                    random_state=1, 
                                                    bootstrap=True,)
            case ('SVM(linear)' | 'Linear SVM'):
                from sklearn.svm import SVC
                if d_paraDict is None:
                    classifier = SVC(kernel="linear", C=0.025,probability=True)
                else:
                    classifier = SVC(C=d_paraDict['C'], 
                                    kernel='linear', 
                                    gamma=d_paraDict['gamma'], 
                                    decision_function_shape=d_paraDict['shape'],
                                    probability=True)
            case ('SVM(RBF)' | 'RBF SVM'):
                # from sklearn.svm import SVC
                from sklearn import svm
                if d_paraDict is None:
                    classifier = svm.NuSVC(gamma="auto",probability=True)
                else:
                    classifier = SVC(C=d_paraDict['C'], 
                                    kernel='rbf', 
                                    gamma=d_paraDict['gamma'], 
                                    decision_function_shape=d_paraDict['shape'],
                                    probability=True)
            case ('KNN' | 'Nearest Neighbors'):
                from sklearn.neighbors import KNeighborsClassifier
                if d_paraDict is None:
                    classifier = KNeighborsClassifier()
                else:
                    classifier = KNeighborsClassifier(n_neighbors=d_paraDict['i_neighbors'], 
                              algorithm='auto', 
                              weights=d_paraDict['s_distance'], 
                              n_jobs=d_paraDict['i_jobs'])
            case 'AdaBoost':
                from sklearn.ensemble import AdaBoostClassifier
                if d_paraDict is None:
                    classifier = AdaBoostClassifier()
                else:
                    classifier = AdaBoostClassifier(algorithm=d_paraDict['s_algor'], 
                                                  base_estimator=None,
                                                  learning_rate=d_paraDict['i_rate'], 
                                                  n_estimators=d_paraDict['i_estimator'], 
                                                  random_state=d_paraDict['i_randstate'])
            case ('Gaussian' | 'Gaussian Process'):
                from sklearn.gaussian_process import GaussianProcessClassifier
                if d_paraDict is None:
                    from sklearn.gaussian_process.kernels import RBF
                    classifier = GaussianProcessClassifier(1.0 * RBF(1.0))
                else:
                    from sklearn.gaussian_process.kernels import RBF
                    l_scale = 1.0
                    classifier = GaussianProcessClassifier(kernel=d_paraDict['bias'] * RBF(length_scale=l_scale), 
                                                          optimizer=None)
            case 'Neural Net':
                from sklearn.neural_network import MLPClassifier
                if d_paraDict is None:
                    classifier = MLPClassifier()
                else:
                    classifier = MLPClassifier(solver=d_paraDict['solver'],
                                               activation = d_paraDict['fun_activ'],
                                               max_iter = 10,
                                               alpha = d_paraDict['alpha'],
                                               hidden_layer_sizes = (100,50),
                                               random_state = 1,
                                               verbose = True)
            case 'Naive Bayes':
                from sklearn.naive_bayes import GaussianNB
                if d_paraDict is None:
                    classifier = GaussianNB()
                else:
                    classifier = GaussianNB()
            case 'Decision Tree':
                from sklearn import tree
                if d_paraDict is None:
                    classifier = tree.DecisionTreeClassifier()
                else:
                    classifier = tree.DecisionTreeClassifier()
            case 'QDA':
                from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
                if d_paraDict is None:
                    classifier = QDA()
                else:
                    classifier = QDA()
            case 'Logistic Regression':
                from sklearn.linear_model import LogisticRegression
                if d_paraDict is None:
                    classifier = LogisticRegression()
                else:
                    classifier = LogisticRegression()
            case 'MLP Classifier':
                from sklearn.neural_network import MLPClassifier
                if d_paraDict is None:
                    classifier = MLPClassifier()
                else:
                    classifier = MLPClassifier()
            case 'Ridge Classifier':
                from sklearn.linear_model import RidgeClassifier
                if d_paraDict is None:
                    classifier = RidgeClassifier()
                else:
                    classifier = RidgeClassifier()
            case 'Gradient Boosting Classifier':
                from sklearn.ensemble import GradientBoostingClassifier
                if d_paraDict is None:
                    classifier = GradientBoostingClassifier(random_state=10)
                else:
                    classifier = GradientBoostingClassifier(random_state=10)
            case 'SVC':
                from sklearn.svm import SVC
                classifier = SVC(gamma='auto',probability=True)
            case 'ExtraTreesClassifier':
                from sklearn.ensemble import ExtraTreesClassifier
                classifier = ExtraTreesClassifier(random_state=0)
            case 'SGDClassifier':
                from sklearn.linear_model import SGDClassifier
                classifier = SGDClassifier(loss="hinge", penalty="l2")
            case 'BernoulliNB':
                from sklearn.naive_bayes import BernoulliNB
                classifier = BernoulliNB(force_alpha=True)
            case 'Perceptron':
                from sklearn.linear_model import Perceptron
                classifier = Perceptron(tol=1e-3, random_state=0)
            case 'PassiveAggressiveClassifier':
                from sklearn.linear_model import PassiveAggressiveClassifier
                classifier = PassiveAggressiveClassifier(random_state=0)
            case 'BaggingClassifier':
                from sklearn.ensemble import BaggingClassifier
                classifier = BaggingClassifier(random_state=0)
            case 'CalibratedClassifierCV':
                from sklearn.calibration import CalibratedClassifierCV
                classifier = CalibratedClassifierCV()
            case 'RidgeClassifierCV':
                from sklearn.linear_model import RidgeClassifierCV
                classifier = RidgeClassifierCV()
            case 'ExtraTreeClassifier':
                from sklearn.tree import ExtraTreeClassifier
                classifier = ExtraTreeClassifier(random_state=0)
            case 'NearestCentroid':
                from sklearn.neighbors import NearestCentroid
                classifier = NearestCentroid()
            case 'LinearDiscriminantAnalysis':
                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
                classifier = LinearDiscriminantAnalysis()
            case 'LabelSpreading':
                from sklearn.semi_supervised import LabelSpreading
                classifier = LabelSpreading()
            case 'LabelPropagation':
                from sklearn.semi_supervised import LabelPropagation
                classifier = LabelPropagation()
            case 'DummyClassifier':
                from sklearn.dummy import DummyClassifier
                classifier = DummyClassifier()
            case 'xgboost':
                from xgboost.sklearn import XGBClassifier
                classifier = XGBClassifier(max_depth=5)
            case 'lightGBM':
                from lightgbm.sklearn import LGBMClassifier
                classifier = LGBMClassifier()
        #return=============
        return classifier
