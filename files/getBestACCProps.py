#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:07:54 2022
@author: sealight
"""
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from files.class_resampData import *
from files.geneSmartPth import *
from files import globSet,config
class ErrorEditDefine(Exception):
    pass
def f_runResample(df_data, s_sampMthd):
    ls_colName_class = df_data.columns.values.tolist()
    ls_y = df_data['class'].values.tolist()
    mat_X = df_data.drop(columns=['class']).values
    obj_resampMod = c_resampData(mat_X, ls_y, s_sampMthd, ls_colName_class)
    d_maxAcc, arr_X_resampled, ls_y_resampled, df_resampledData = obj_resampMod.f_operResampling()
    return df_resampledData
def f_concat2Df_h_1(df_data1, df_data2):
    ls_cols1 = df_data1.columns.values.tolist()
    ls_cols2 = df_data2.columns.values.tolist()
    b_isInDf1 = 'class' in ls_cols1
    b_isInDf2 = 'class' in ls_cols2
    if (b_isInDf1) and (b_isInDf2):
        if all(df_data1['class'].values == df_data2['class'].values):
            df_noclass1 = df_data1
            df_noclass2 = df_data2.drop(columns=['class'])
            ls_colNames1_c = df_data1.columns.values.tolist()
            ls_colNames2_c = df_noclass2.columns.values.tolist()
            ls_finalColName = ls_colNames1_c
            ls_finalColName.extend(ls_colNames2_c)
        else:
            raise ErrorEditDefine('The contacted data have different class/target.')
    elif (b_isInDf1) and (not b_isInDf2):
        df_noclass1 = df_data1.values
        df_noclass2 = df_data2.values
        ls_finalColName = ls_cols1
        ls_finalColName.extend(ls_cols2)
    elif (not b_isInDf1) and (b_isInDf2):
        df_noclass2 = df_data2.values
        df_noclass1 = df_data1.values
        ls_finalColName = ls_cols1
        ls_finalColName.extend(ls_cols2)
    else:
        df_noclass1 = df_data1.values
        df_noclass2 = df_data2.values
    arr_combMat = np.vstack((df_noclass1.T, df_noclass2.T)).T
    if b_isInDf1 or b_isInDf2:
        df_combFeat = pd.DataFrame(arr_combMat)
        df_combFeat.columns = ls_finalColName
    else:
        df_combFeat = pd.DataFrame(arr_combMat)
    return df_combFeat
def f_stdNormlize1(df_featData):
    df_featureAdClass = df_featData
    featureData = df_featureAdClass.drop(columns=['class'])
    ls_pureFeatNames = featureData.columns.values.tolist()
    stdsc=StandardScaler()
    normedData = stdsc.fit_transform(featureData.T).T
    classColData = df_featureAdClass['class']
    newFeatureData = np.vstack([classColData.T,normedData.T]).T
    ls_columnNames_normed = ['class']
    ls_columnNames_normed.extend(ls_pureFeatNames)
    newFeatDf_normed = pd.DataFrame(newFeatureData, columns = ls_columnNames_normed)
    return newFeatDf_normed
def f_comp2List_eachElem(ls_1,ls_2):
    if len(ls_1)==len(ls_2):
        ls_compReslt = []
        for i_ind,val in enumerate(ls_1):
            if ls_1[i_ind]==ls_2[i_ind]:
                ls_compReslt.append(1)
            else:
                ls_compReslt.append(1)
        return ls_compReslt
    else:
        raise ErrorEditDefine('The length of the two arrays does not match')
def f_evaluateCsvDataByTrainData(df_propCsvData,s_sampMthd,obj_clsfer,f_testSize):
    df_propData_normed = f_stdNormlize1(df_propCsvData)
    df_resampledFeat = f_runResample(df_propData_normed,s_sampMthd)
    y = df_resampledFeat['class'].values.tolist()
    matX = df_resampledFeat.drop(columns=['class']).values
    X_train,X_test,y_train,y_test = train_test_split(matX,y,test_size=f_testSize,random_state=0)
    obj_clsfer.fit(X_train,y_train)
    predict = obj_clsfer.predict(X_test)
    fv_acc = sum(f_comp2List_eachElem(y_test,predict))/len(predict)
    return fv_acc
def f_evaluateCsvDataByTrainData_mulTestSize(df_propCsvData,s_sampMthd,obj_clsfer):
    ls_testSize = [0.8, 0.85, 0.9]
    ls_predVal_underDiffSize = [0 for item in ls_testSize]
    for i_index in range(len(ls_testSize)):
        fv_curTestSetRate = ls_testSize[i_index]
        fv_curAcc = f_evaluateCsvDataByTrainData(df_propCsvData,s_sampMthd,obj_clsfer,fv_curTestSetRate)
        ls_predVal_underDiffSize[i_index] = fv_curAcc
    return np.mean(ls_predVal_underDiffSize)
def f_findSameAccPropNames(ls_sortedAccTuple):
    i_Index = -1
    fv_maxAccVal = ls_sortedAccTuple[-1][1]
    b_isNext = True
    ls_samMaxACC_propNames = [ls_sortedAccTuple[-1][0]]
    while b_isNext:
        if i_Index == -(len(ls_sortedAccTuple)):
            return ls_samMaxACC_propNames
        else:
            i_Index -= 1
        if fv_maxAccVal==ls_sortedAccTuple[i_Index][1]:
            ls_samMaxACC_propNames.append(ls_sortedAccTuple[i_Index][0])
    return ls_samMaxACC_propNames
def f_1singleProp_readCsv(s_1propName,s_taskID):
    s_propCsvName = ''.join([s_1propName,'_',s_taskID,'.csv'])
    p_fullpth = geneSmartPth('results',s_propCsvName)
    try:
        df_1prop = pd.read_csv(p_fullpth)
    except:
        raise ErrorEditDefine('There is an error when reading the csv files: '+p_fullpth)
    return df_1prop
def f_combProp_getDf(ls_splitList,s_taskID):
    for i_propInd in range(len(ls_splitList)-1):
        if i_propInd ==0:
            df_prop0 = f_1singleProp_readCsv(ls_splitList[0],s_taskID)
            df_prop1 = f_1singleProp_readCsv(ls_splitList[1],s_taskID)
            df_combDf = f_concat2Df_h_1(df_prop0,df_prop1)
        else:
            df_nextProp = f_1singleProp_readCsv(ls_splitList[i_propInd+1],s_taskID)
            df_combDf = f_concat2Df_h_1(df_combDf,df_nextProp)
    return df_combDf
def f_getCsv_evalMeanAcc(s_propName,s_sampMthd,obj_clsfer,s_taskID):
    ls_splitList = s_propName.split('+')
    i_lsLength = len(ls_splitList)
    if i_lsLength==1:
        df_curProp = f_1singleProp_readCsv(s_propName,s_taskID)
    else:
        df_curProp = f_combProp_getDf(ls_splitList,s_taskID)
    fv_accCurProp = f_evaluateCsvDataByTrainData_mulTestSize(df_curProp,s_sampMthd,obj_clsfer)
    return fv_accCurProp
def f_getDataFrame_1prop(s_propName,s_sampMthd,obj_clsfer,s_taskID):
    ls_splitList = s_propName.split('+')
    i_lsLength = len(ls_splitList)
    if i_lsLength==1:
        df_curProp = f_1singleProp_readCsv(s_propName,s_taskID)
    else:
        df_curProp = f_combProp_getDf(ls_splitList,s_taskID)
    return df_curProp
def f_compareMultiProps(ls_samMaxAcc_propNames,s_sampMthd,obj_clsfer,s_taskID):
    ls_meanAccEachProp = [[item, 0] for item in ls_samMaxAcc_propNames]
    for i_idx in range(len(ls_samMaxAcc_propNames)):
        s_curProp = ls_samMaxAcc_propNames[i_idx]
        fv_meanAcc_curProp = f_getCsv_evalMeanAcc(s_curProp,s_sampMthd,obj_clsfer,s_taskID)
        ls_meanAccEachProp[i_idx][1] = fv_meanAcc_curProp
    ls_meanAccEachProp.sort(key=lambda x:x[1])
    s_bestPropName = ls_meanAccEachProp[-1][0]
    return s_bestPropName
def f_compListGetTheBestProp(s_sampMthd,obj_clsfer,s_taskID):
    ls_forSortFun = []
    d_propAccInfo = globSet.get_finalProps()
    if d_propAccInfo==0:
        pass
    else:
        for s_key,fv_val in list(d_propAccInfo.items()):
            ls_forSortFun.append((s_key,fv_val))
        if len(d_propAccInfo)==1:
            s_bestPropName = ls_forSortFun[0][0]
        else: 
            ls_forSortFun.sort(key=lambda x:x[1])
            if ls_forSortFun[-1][1]==ls_forSortFun[-2][1]:
                ls_samMaxAcc_propNames = f_findSameAccPropNames(ls_forSortFun)
                s_bestPropName = f_compareMultiProps(ls_samMaxAcc_propNames,s_sampMthd,obj_clsfer,s_taskID)
            else:
                s_bestPropName = ls_forSortFun[-1][0]
        df_bestProp = f_getDataFrame_1prop(s_bestPropName,s_sampMthd,obj_clsfer,s_taskID)
        s_bestProp_csvName = ''.join([s_taskID,'_bestFeat','.csv'])
        p_fullPth_bestFeat = geneSmartPth('results', s_bestProp_csvName)
        df_bestProp = df_bestProp.applymap(lambda x: '%.5f'%x)
        df_bestProp.to_csv(p_fullPth_bestFeat, index=False)
        globSet.add_finalProp('bestFeat',s_bestPropName)
        f_bestScore = d_propAccInfo[s_bestPropName]
        globSet.add_finalProp('bestFeat-predictAccuray',f_bestScore)
        s_jsonFileName = ''.join([s_taskID,'_allPropInfo','.json'])
        p_jsonFilePth = geneSmartPth('results', s_jsonFileName)
        d_allTaskInfo = globSet.get_finalProps()
        json_str = json.dumps(d_allTaskInfo, ensure_ascii=False, indent=4, separators=(',', ':'))
        with open(p_jsonFilePth, 'w') as json_file:
            json_file.write(json_str)
        return p_fullPth_bestFeat,s_bestPropName,f_bestScore
        