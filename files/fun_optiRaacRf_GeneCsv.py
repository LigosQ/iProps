#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:25:06 2020
@author: tafch
"""
"""
Created on Wed Dec  2 08:58:38 2020
@author: tafch
"""
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score 
from sklearn.model_selection import StratifiedShuffleSplit
from files.operResamplingOnData import *
from files.fun_dfData2Csv import *
from files.cmdmainCalcDepipFeats import *
from files.geneSmartPth import *
from files.class_resampData import *
from files.fun_comb_PNdf_1Schm import *
# from files.f_geneClfier import f_geneClfier_byStr
from files.class_mlClassifier import c_mlClassifier
def normalizeDataFrame(dfdata):
    pd_pureFeatReducDepip = dfdata.drop(columns=['class'])
    stdsc=StandardScaler()
    arrayNormedPdFeat = stdsc.fit_transform(pd_pureFeatReducDepip.T).T
    seriesClass_pd = dfdata['class']
    colnamesListInFeatDf = pd_pureFeatReducDepip.columns.values.tolist()
    dfNormdFeat = pd.DataFrame(arrayNormedPdFeat,columns=colnamesListInFeatDf)
    pd_adFeatClass = pd.concat([seriesClass_pd,dfNormdFeat])
    return arrayNormedPdFeat,seriesClass_pd.values.tolist()
def findIdxByThres(listdata,threshold):
    betterSchmIndlist = []
    for i in range(len(listdata)):
        if listdata[i]>threshold:
            betterSchmIndlist.append(i)
    return betterSchmIndlist
def getLogicInd(listdata,value):
    logicIndList = []
    for i in range(len(listdata)):
        if listdata[i]==value:
            logicIndList.append(True)
        else:
            logicIndList.append(False)
    return logicIndList
def getPosNegDfdata(dfdata):
    classValList = dfdata['class'].values
    logicIndPos1 = getLogicInd(classValList,1)
    dfPos = dfdata[(logicIndPos1)]
    logicIndPos2 = getLogicInd(classValList,0)
    dfNeg = dfdata[(logicIndPos2)]
    dfAll = pd.concat([dfPos,dfNeg],axis=0)
    return dfAll
def f_alphabet_str2dict(s_alphabet):
    ls_primaryAlpha = s_alphabet.split('#')
    d_alphabet = dict()
    for item in ls_primaryAlpha:
        ls_secdAlpha = item.split('-')
        d_alphabet[ls_secdAlpha[0]] = list(ls_secdAlpha[1])
    return d_alphabet
def innerFun_optiRaacByRf(textFilPth,posfilePth,negfilePth,rsampMethdStr,othersTres,
                          filepth_betterSchm,finalCsvPth,taskId,s_clfer):
    fid = open(textFilPth,'r')
    alphabetDict = {}
    lineNum = 0
    for line in fid.readlines():
        lineNum += 1
        curlineStr = line
        alphalist = curlineStr.split('#')
        lenList = len(alphalist)
        newAlphaList = alphalist
        newReducedAlphaStr = ''
        for i in range(lenList):
            curAaCluster = alphalist[i]
            newAaCluster = curAaCluster[0] + '-' + curAaCluster
            newAlphaList[i] = newAaCluster
            finalStrOfCurAlpha = '#'.join(newAlphaList)
        alphabetDict[str(lineNum)] = finalStrOfCurAlpha
    # rfClf0 = f_geneClfier_byStr(s_clsfier)
    rfClf0 = c_mlClassifier(s_clsfier).f_geneMlClassifier(None)
    predValList = []
    ls_predSchmList = []
    maxAccuracy = 0
    df_forMaxAccuracy = None
    numOfSplit = 3
    numOfCross = 4
    d_score_AllSchms = dict()
    for i in range(len(alphabetDict)):
        if i%20==1:
            print(i+1)
        curReducSet = alphabetDict[str(i+1)]
        d_curSchmInfo = dict()
        d_curSchmInfo['schmStr'] = curReducSet
        df_redDipep = f_combDipep_PosNeg_1schm(posfilePth,negfilePth,f_alphabet_str2dict(curReducSet))
        X,y = normalizeDataFrame(df_redDipep)
        split = StratifiedShuffleSplit(n_splits=numOfSplit, test_size=0.2, random_state=1)         
        resmp_obj = c_resampData(X,y,rsampMethdStr,df_redDipep.columns.tolist())
        d_maxAcc, x_rsmt, y_rsmt, df_resampledData = resmp_obj.f_operResampling()
        scoreList = []
        sumOfCross = 0
        y_rsmt_arr = np.array(y_rsmt)
        for train_index, test_index in split.split(x_rsmt,y_rsmt):
            X_train, X_test = x_rsmt[train_index], x_rsmt[test_index]
            y_train, y_test = y_rsmt_arr[train_index], y_rsmt_arr[test_index]
            rfClf = rfClf0
            scores_cross = cross_val_score(rfClf, X_train,y_train,cv=numOfCross)
            meanScores_curSplit = scores_cross.mean()
            scoreList.append(meanScores_curSplit)
        scores = np.array(scoreList)
        scores_mean = scores.mean()
        d_curSchmInfo['precision'] = scores_mean
        d_score_AllSchms[str(i)] = d_curSchmInfo
        if scores_mean>maxAccuracy:
            bestSchmStr = curReducSet
            bestSchmNo = i
        predValList.append(scores_mean)
        ls_predSchmList.append(curReducSet)
    df_redDipep = f_combDipep_PosNeg_1schm(posfilePth,negfilePth,f_alphabet_str2dict(bestSchmStr))
    writeDf2csv(df_redDipep,finalCsvPth)
    betterIndx = findIdxByThres(predValList,othersTres)
    rsltTxt_fid = open(filepth_betterSchm,'w+')
    goodPerformDict = {}
    for i in range(len(betterIndx)):
        curSchmIdex = betterIndx[i]
        curSchmStr = ls_predSchmList[i]
        rsltTxt_fid.write(str(curSchmIdex)+'\t\t precision: '+str(predValList[curSchmIdex])+'\n')
        rsltTxt_fid.write(curSchmStr+'\n')
        curPerformInfo = {}
        curPerformInfo['index'] = curSchmIdex
        curPerformInfo['precision'] = predValList[curSchmIdex]
        curPerformInfo['Scheme'] = curSchmStr
        goodPerformDict[str(i)] = curPerformInfo
    goodPerformDict['rawInfo'] = d_score_AllSchms
    rsltTxt_fid.close()
    jsonPth_allInfo = geneSmartPth('results',str(taskId)+'_json_RAAC.json')
    with open(jsonPth_allInfo, "w+") as fid_precDict:
        fid_precDict.write(json.dumps(goodPerformDict, ensure_ascii=False, indent=4, separators=(',', ':')))
    fid_precDict.close()
    return df_redDipep,predValList,bestSchmStr