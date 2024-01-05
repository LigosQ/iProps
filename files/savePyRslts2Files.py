#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:05:34 2021
@author: tafch
"""
import pandas as pd
import numpy as np
import math
from fun_optiRaacRf_GeneCsv import *
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, confusion_matrix
from sklearn.pipeline import Pipeline
from scipy.stats import randint as sp_randint
from sklearn.model_selection import RandomizedSearchCV
from fun_dfData2Csv import *
import os
import json
import warnings
from geneSmartPth import *
class ErrorUser(Exception):
    pass
def gridSearchRf_geneBestClf(X,y):
    rfClfier = RandomForestClassifier(random_state=1)
    param_dist = {"n_estimators":[2,5,10,None],
                    "max_depth": [3,5,8,10, None],              
                  "max_features": sp_randint(1, 11),          
                  "min_samples_split": sp_randint(2, 11),     
                  "bootstrap": [True, False],                 
                  "criterion": ["gini", "entropy"]}           
    n_iter_search = 20
    random_searchModel = RandomizedSearchCV(rfClfier, param_distributions=param_dist,
                                       n_iter=n_iter_search, cv=5)
    random_searchModel.fit(X, y)
    n_estimators_best = random_searchModel.best_params_['n_estimators']
    min_samples_split_best = random_searchModel.best_params_['min_samples_split']
    max_features_best = random_searchModel.best_params_['max_features']
    max_depth_best = random_searchModel.best_params_['max_depth']
    bootstrap_best = random_searchModel.best_params_['bootstrap']
    rfClfier_best = RandomForestClassifier(n_estimators=n_estimators_best,min_samples_split=min_samples_split_best,
                                      random_state=1, max_features=max_features_best,
                                      max_depth=max_depth_best,bootstrap=bootstrap_best)
    return rfClfier_best
def query2TypeIndex(dfdata):
    indexList_pos = []
    indexList_neg = []
    seriClassCol = dfdata['class']
    for i in range(len(seriClassCol)):
        if (seriClassCol[i]==1) or (seriClassCol[i]=='1'):
            indexList_pos.append(i)
        else:
            indexList_neg.append(i)
    return indexList_pos,indexList_neg
def geneDfByRsampledData(oldDf,x_resamp,y_resamp):
    colNameList = oldDf.columns.values.tolist()
    if colNameList[0]=='class' or colNameList[0]=='Class':
        if isinstance(y_resamp,list):
            y_resamp = np.array(y_resamp)
        else:
            raise ErrorUser('The y_resamp should be list type')
        featClassMat = np.vstack((y_resamp.T,x_resamp.T)).T
    elif colNameList[-1]=='class' or colNameList[-1]=='Class':
        if isinstance(y_resamp,list):
            y_resamp = np.array(y_resamp)
        else:
            raise ErrorUser('The y_resamp should be list type')
        featClassMat = np.vstack((x_resamp.T,y_resamp.T)).T
    else:
        raise ErrorUser('The class column should be in the 1st column or the last column, please check...')
    df_resampled = pd.DataFrame(featClassMat,columns=colNameList)
    return df_resampled
def clacIndDictForCrossVer(indexList,n):
    numOfIndex = len(indexList)
    eachSize = math.ceil(numOfIndex/n)
    eachSectStartIndexList = [eachSize*i for i in range(n)]
    eachSectEndIndexList = [eachSize*(i+1) for i in range(n)]
    eachSectEndIndexList[-1] = numOfIndex
    np.random.shuffle(indexList)
    indDict = {}
    for i_cross in range(n):
        curTest_startInd = eachSectStartIndexList[i_cross]
        curTest_endInd = eachSectEndIndexList[i_cross]
        pureIndInDf_curTest = indexList[curTest_startInd:curTest_endInd]
        pureIndInDf_curTrain = []
        for item in indexList:
            if item not in pureIndInDf_curTest:
                pureIndInDf_curTrain.append(item)
            else:
                pass
        indDict[str(i_cross)] = [pureIndInDf_curTest,pureIndInDf_curTrain]
    return indDict
def calcPerformance(labelArr, predictArr):
    TP = 0.; TN = 0.; FP = 0.; FN = 0.   
    for i in range(len(labelArr)):
        if labelArr[i] == 1 and predictArr[i] == 1:
            TP += 1.
        if labelArr[i] == 1 and predictArr[i] == 0:
            FN += 1.
        if labelArr[i] == 0 and predictArr[i] == 1:
            FP += 1.
        if labelArr[i] == 0 and predictArr[i] == 0:
            TN += 1.
    SN = TP/(TP + FN) 
    SP = TN/(FP + TN) 
    MCC = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    ACC = (TP+TN)/(TP+TN+FP+FN)
    return SN,SP,ACC,MCC
def geneIndDictForCross(dfdata,crossN,rsampMethdStr):
    X,y = normalizeDataFrame(dfdata)
    resmp_obj = c_resampData(X,y,rsampMethdStr,dfdata.columns.tolist())
    d_maxAcc, x_rsmt, y_rsmt, df_resampledData = resmp_obj.f_operResampling()
    df_resampled = geneDfByRsampledData(dfdata,x_rsmt,y_rsmt)
    classColList = df_resampled['class']
    dfPureFeat = df_resampled.drop(columns=['class'])
    allPosDataInd, allNegDataInd = query2TypeIndex(df_resampled)
    posIndexDict = clacIndDictForCrossVer(allPosDataInd, crossN)
    negIndexDict = clacIndDictForCrossVer(allNegDataInd, crossN)
    realY_list = []
    predY_list = []
    for i in range(crossN):
        indexList_trainAndTest_pos_i = posIndexDict[str(i)]
        testIndList_pos = indexList_trainAndTest_pos_i[0]
        trainIndList_pos = indexList_trainAndTest_pos_i[1]
        indexList_trainAndTest_neg_i = negIndexDict[str(i)]
        testIndList_neg = indexList_trainAndTest_neg_i[0]
        trainIndList_neg = indexList_trainAndTest_neg_i[1]
        testIndList_pos.extend(testIndList_neg)
        testIndList_i = testIndList_pos
        trainIndList_pos.extend(trainIndList_neg)
        trainIndList_i = trainIndList_pos
        x_train = dfPureFeat.iloc[trainIndList_i]
        y_train = classColList[trainIndList_i]
        x_test = dfPureFeat.iloc[testIndList_i]
        y_test = classColList[testIndList_i]
        bestRfClfier = gridSearchRf_geneBestClf(x_train,y_train)
        bestRfClfier.fit(x_train,y_train)
        y_predicted = bestRfClfier.predict(x_test)
        realY_list.extend(y_test)
        predY_list.extend(y_predicted)
    SN,SP,ACC,MCC = calcPerformance(realY_list,predY_list)
    return SN,SP,ACC,MCC
def savePyReslt2Files(precDict_perCombs,bestFeat_maxPrec,crossSplitNum,resampMethd,taskID):
    warnings.filterwarnings("ignore")
    dict_AllInfo = {}
    dict_AllInfo['bestFeatName'] = bestFeat_maxPrec['FeatCombName']
    dict_AllInfo['maxPrecision'] = bestFeat_maxPrec['maxPrecision']
    dfbestFeat = bestFeat_maxPrec['bestFeat']
    SN,SP,ACC,MCC = geneIndDictForCross(dfbestFeat,crossSplitNum,resampMethd)
    dict_AllInfo['SN'] = SN
    dict_AllInfo['SP'] = SP
    dict_AllInfo['ACC'] = ACC
    dict_perPropPrecison = precDict_perCombs
    dict_AllInfo['perPropPrec'] = dict_perPropPrecison
    optiRaacJsonPth = geneSmartPth('results',str(taskID)+'_json_RAAC.json')
    if os.path.isfile(optiRaacJsonPth):
        with open(optiRaacJsonPth,'r',encoding='utf8')as fp:
            json_optiRaacInfo = json.load(fp)
        dict_AllInfo['raacSchmsInfo'] = json_optiRaacInfo
    else:
        dict_AllInfo['raacSchmsInfo'] = None
    csvPth_bestFeat = geneSmartPth('results',str(taskID)+'_bestFeat'+'.csv')
    jsonPth_allInfo = geneSmartPth('results',str(taskID)+'_allInfoJson'+'.json')
    with open(jsonPth_allInfo, "w") as fid_precDict:
        fid_precDict.write(json.dumps(dict_AllInfo, ensure_ascii=False, indent=4, separators=(',', ':')))
    fid_precDict.close()
    writeDf2csv(dfbestFeat,csvPth_bestFeat)
