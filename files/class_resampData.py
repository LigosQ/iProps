#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 17:19:17 2021
@author: tafch
"""
import numpy as np
import pandas as pd
class ErrorUser(Exception):
    pass
class c_resampData(object):
    def __init__(self, arr_x, ls_y, s_resampMethd,ls_dfColName):
        self._arr_X = arr_x
        self._ls_y = ls_y
        self._s_resampMthd = None
        self._b_isEqualNum = None
        self._ls_colName = None
        if isinstance(ls_dfColName,list):
            self._ls_colName = ls_dfColName
        else:
            raise ErrorUser('Error: your given column name is not the list type')
        ls_allusefulMthods = ['RandomOverSampler','SMOTE','BorderlineSMOTE','ADASYN',
                              'KMeansSMOTE','SVMSMOTE','RandomUnderSampler','NearMiss',
                              'ClusterCentroids','EasyEnsemble',
                              'SMOTEENN','SMOTETomek','add','delete','both','orig']
        if s_resampMethd in ls_allusefulMthods:
            self._s_resampMthd = s_resampMethd
        else:
            raise ErrorUser('The given resampling method is not supported now.\n'
                            'Please check the name or select one name from the method table.\n'
                            'Only the method lies in the table is supported in our package.\n')
    def f_clacNumberInEachType(self):
        set_y = set(self._ls_y)
        if len(set_y) == 2:
            pass
        elif len(set_y) == 1:
            raise ErrorUser('There are only one types of samples in the y list. \n'
                            'The current version supports two types or binary types.')
        elif len(set_y) >2:
            raise ErrorUser('The type number of y is more than 2. \n'
                            'The current version does not support the multi-classification task.')
        if (0 in set_y) and (1 in set_y):
            pass
        else:
            raise ErrorUser('The lable of positive samples should be 1, the negative samples are 0. \n'
                            'Your currnt lable in the y list does not meet the requirement.')
        i_numof_0 = 0
        i_numof_1 = 0
        i_finalNum_0 = None
        i_finalNum_1 = None
        for item in self._ls_y:
            if item == 1:
                i_numof_1 += 1
            else:
                i_numof_0 += 1
        if i_numof_0 == i_numof_1:
            self._b_isEqualNum = True
        else:
            self._b_isEqualNum = False
        if self._s_resampMthd in ['RandomOverSampler','SMOTE','BorderlineSMOTE','ADASYN', 'KMeansSMOTE','SVMSMOTE','add']:
            if i_numof_0 > i_numof_1:
                i_finalNum_0 = i_numof_0
                i_finalNum_1 = i_numof_0
            elif i_numof_0 < i_numof_1:
                i_finalNum_0 = i_numof_1
                i_finalNum_1 = i_numof_1
            else:
                i_finalNum_0 = i_numof_0
                i_finalNum_1 = i_numof_1
        elif self._s_resampMthd in ['RandomUnderSampler','NearMiss', 'ClusterCentroids','EasyEnsemble','BalanceCascade','delete']:
            if i_numof_0 > i_numof_1:
                i_finalNum_0 = i_numof_1
                i_finalNum_1 = i_numof_1
            elif i_numof_0 < i_numof_1:
                i_finalNum_0 = i_numof_0
                i_finalNum_1 = i_numof_0
            else:
                i_finalNum_0 = i_numof_0
                i_finalNum_1 = i_numof_1
        elif self._s_resampMthd in ['SMOTEENN','SMOTETomek','both']:
            i_diffNum = abs(i_numof_0 - i_numof_1)
            i_goldStyleNum = int(0.618*i_diffNum)
            if i_numof_0 > i_numof_1:
                i_finalNum_0 = i_numof_1 + i_goldStyleNum
                i_finalNum_1 = i_numof_1 + i_goldStyleNum
            elif i_numof_0 < i_numof_1:
                i_finalNum_0 = i_numof_0 + i_goldStyleNum
                i_finalNum_1 = i_numof_0 + i_goldStyleNum
            else:
                i_finalNum_0 = i_numof_0
                i_finalNum_1 = i_numof_1
        else:
            i_finalNum_0 = i_numof_0
            i_finalNum_1 = i_numof_1
        return i_finalNum_0, i_finalNum_1
    def f_resampBy1method(self, X_orig, y_orig, s_sampleMthdName):
        if (s_sampleMthdName == 'orig'):
            return X_orig,y_orig
        else:
            arr_X_resampled = None
            ls_y_resampled = None
            if s_sampleMthdName == 'RandomOverSampler':
                from imblearn.over_sampling import RandomOverSampler
                ros = RandomOverSampler(random_state=0)
                arr_X_resampled, ls_y_resampled = ros.fit_resample(X_orig, y_orig)
            if (s_sampleMthdName == 'SMOTE'):
                from imblearn.over_sampling import SMOTE
                smo = SMOTE(random_state=42)
                arr_X_resampled, ls_y_resampled = smo.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'BorderlineSMOTE':
                from imblearn.over_sampling import BorderlineSMOTE 
                smo = BorderlineSMOTE(random_state=42) 
                arr_X_resampled, ls_y_resampled = smo.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'ADASYN':
                from imblearn.over_sampling import ADASYN
                ana = ADASYN(random_state=0,sampling_strategy = 'minority')
                arr_X_resampled, ls_y_resampled = ana.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'KMeansSMOTE':
                from imblearn.over_sampling import KMeansSMOTE
                kms = KMeansSMOTE(random_state=42)
                arr_X_resampled, ls_y_resampled = kms.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'SVMSMOTE':
                from imblearn.over_sampling import SVMSMOTE
                svmm = SVMSMOTE(random_state=42)
                arr_X_resampled, ls_y_resampled = svmm.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'RandomUnderSampler':
                from imblearn.under_sampling import RandomUnderSampler 
                cc = RandomUnderSampler(random_state=0)
                arr_X_resampled, ls_y_resampled = cc.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'NearMiss':
                from imblearn.under_sampling import NearMiss
                nm1 = NearMiss()
                arr_X_resampled, ls_y_resampled = nm1.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'ClusterCentroids':
                from imblearn.under_sampling import ClusterCentroids
                cc = ClusterCentroids(random_state=0)
                arr_X_resampled, ls_y_resampled = cc.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'EasyEnsemble':
                from imblearn.ensemble import EasyEnsemble
                ee = EasyEnsemble(random_state=0)
                arr_X_resampled, ls_y_resampled = ee.fit_sample(X_orig, y_orig)
            if s_sampleMthdName == 'BalanceCascade':
                from imblearn.ensemble import BalanceCascade 
                bc = BalanceCascade(random_state=0)
                arr_X_resampled, ls_y_resampled = bc.fit(X_orig, y_orig)
            if s_sampleMthdName == 'SMOTEENN':
                from imblearn.combine import SMOTEENN
                smote_enn = SMOTEENN(random_state=0)
                arr_X_resampled, ls_y_resampled = smote_enn.fit_resample(X_orig, y_orig)
            if s_sampleMthdName == 'SMOTETomek':
                from imblearn.combine import SMOTETomek
                smote_tomek = SMOTETomek(random_state=0)
                arr_X_resampled, ls_y_resampled = smote_tomek.fit_resample(X_orig, y_orig)
            return arr_X_resampled, ls_y_resampled
    def f_estimPerfRsampedData(self, X_rsampled,y_rsampld):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        clf = RandomForestClassifier(random_state=0)
        scores = cross_val_score(clf, X_rsampled, y_rsampld)
        return scores.mean()
    def f_resampAdEvaluation_outPrecision(self, s_resampMthd, X_orig, y_orig):
        arr_x_rsamped, ls_y_resampled = self.f_resampBy1method(X_orig, y_orig, s_resampMthd)
        f_curRsampMethdScore = self.f_estimPerfRsampedData(arr_x_rsamped, ls_y_resampled)
        return f_curRsampMethdScore,arr_x_rsamped, ls_y_resampled
    def f_resamplByOverallStrategy(self, s_overallStrategy,X_orig,y_orig):
        if s_overallStrategy=='add':
            ls_allRsampMthods = ['RandomOverSampler','SMOTE','BorderlineSMOTE','ADASYN','SVMSMOTE']    
        elif s_overallStrategy=='delete':
            ls_allRsampMthods = ['RandomUnderSampler','NearMiss', 'ClusterCentroids']
            ls_allRsampMthods = ['NearMiss']
        elif s_overallStrategy=='both':
            ls_allRsampMthods = ['SMOTEENN','SMOTETomek']
        else:
            raise ErrorUser('Error: This function only support add/delete/both strategies. '
                            'Your codes or input parameters may be wrong...')
        f_maxPrecision = 0
        s_method_withBestAcc = ''
        for i_ind in range(len(ls_allRsampMthods)):
            s_curRsampMthd = ls_allRsampMthods[i_ind]
            f_accracy_curRsampMth,x,y = self.f_resampAdEvaluation_outPrecision(s_curRsampMthd, X_orig,y_orig)
            if f_accracy_curRsampMth > f_maxPrecision:
                f_maxPrecision = f_accracy_curRsampMth
                s_method_withBestAcc = s_curRsampMthd
            else:
                pass
        return f_maxPrecision,s_method_withBestAcc
    def f_geneDfBy3Elements(self, arr_x, ls_y):
        ls_colName = self._ls_colName
        if 'class' in ls_colName:
            ls_colName_withCls = [ls_colName[i] for i in range(len(ls_colName)) if ls_colName[i]!='class']
            ls_colName_withCls.append('class')
        else:
            ls_colName_withCls = ls_colName
            ls_colName_withCls.append('class')
        if isinstance(ls_y, list):
            arr_y = np.array(ls_y)
        elif type(ls_y) is np.ndarray:
            arr_y = ls_y
        else:
            raise ErrorUser('The given y should be set in a list type.')
        if isinstance(arr_x, list):
            arr_x = np.array(arr_x)
        elif type(arr_x) is np.ndarray:
            pass
        else:
            raise ErrorUser('The given x should be a ndarray or a list')
        if ls_colName_withCls[0] == 'class':
            arr_propWithCls = np.vstack((arr_y.T, arr_x.T)).T
        elif ls_colName_withCls[-1] == 'class':
            arr_propWithCls = np.vstack((arr_x.T, arr_y.T)).T
        else:
            raise ErrorUser('The class column is not in the 1st or the last column, please check your dataframe')
        df_withCls = pd.DataFrame(arr_propWithCls, columns=ls_colName_withCls)
        return df_withCls
    def f_operResampling(self):
        if self._s_resampMthd is None:
            raise ErrorUser('The resampling method in the object is None now.\n'
                            'There may be some mistakes happened in the initialization step.\n'
                            'please check codes...')
        else:
            pass
        arr_X_resampled = None
        ls_y_resampled = None
        i_resampNum_0, i_resampNum_1 = self.f_clacNumberInEachType()
        if (self._b_isEqualNum is None):
            raise ErrorUser('The member variable: b_isEqualNum is not assigned values. please check codes...')
        else:
            if self._b_isEqualNum == True:
                arr_X_resampled = self._arr_X
                ls_y_resampled = self._ls_y
                f_maxAcc = self.f_estimPerfRsampedData(arr_X_resampled, ls_y_resampled)
            else:
                X_orig = self._arr_X
                y_orig = self._ls_y
                if self._s_resampMthd in ['add','delete','both']:
                    f_maxPrecision,s_method_withBestAcc = self.f_resamplByOverallStrategy(self._s_resampMthd, X_orig,y_orig)
                    f_maxAcc, arr_X_resampled, ls_y_resampled = self.f_resampAdEvaluation_outPrecision(s_method_withBestAcc, X_orig,y_orig)
                else:
                    f_maxAcc, arr_X_resampled, ls_y_resampled = self.f_resampAdEvaluation_outPrecision(self._s_resampMthd, X_orig,y_orig)
            df_resampledData = self.f_geneDfBy3Elements(arr_X_resampled, ls_y_resampled)
            return f_maxAcc, arr_X_resampled, ls_y_resampled, df_resampledData
