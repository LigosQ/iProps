#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 11:10:25 2020
@author: tafch
"""
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from files.fun_dfData2Csv import *
from files.geneSmartPth import geneSmartPth
from files.class_resampData import *
from files.fun_geneMultiFeats import *
from files.fun_optiRaacRf_GeneCsv import *
from files.f_geneClfier import f_geneClfier_byStr
from files.class_mlClassifier import c_mlClassifier
from files import globSet 
class ErrorEditDefine(Exception):
    pass
def isEqalInAllElem(clsSeries_1,clsSries_2):
    numOfClsLab = len(clsSeries_1)
    if numOfClsLab==len(clsSries_2):
        for i in range(numOfClsLab):
            if clsSeries_1[i] != clsSries_2[i]:
                raise ErrorEditDefine('The class value in some position is not equal...')
                return False
        return True
    else:
        raise ErrorEditDefine('The length of class column is not equal....')
        return False
def comb2FeatDf(dfdata1,dfdata2):
    clsColVal_1 = dfdata1['class']
    dfdata1_dropCls = dfdata1.drop(columns=['class'])
    clsColVal_2 = dfdata2['class']
    dfdata2_dropCls = dfdata2.drop(columns=['class'])
    if isEqalInAllElem(clsColVal_1.values,clsColVal_2.values):
        matrix_feat1 = dfdata1_dropCls.values
        matrix_feat2 = dfdata2_dropCls.values
        arrayFeatMat2 = np.vstack((matrix_feat1.T,matrix_feat2.T)).T
        arrayFeatMat_adCls = np.vstack((clsColVal_1.T,arrayFeatMat2.T)).T
        colList_feat1 = dfdata1_dropCls.columns.values.tolist()
        colList_feat2 = dfdata2_dropCls.columns.values.tolist()
        finalColNamList = ['class']
        finalColNamList.extend(colList_feat1)
        finalColNamList.extend(colList_feat2)
        df_2combFeat = pd.DataFrame(arrayFeatMat_adCls, columns=finalColNamList)
        return df_2combFeat
    else:
        raise ErrorEditDefine('The combinded csv files have different class columns...')
def normalizeDataFrame(dfdata):
    pd_pureFeatReducDepip = dfdata.drop(columns=['class'])
    stdsc=StandardScaler()
    arrayNormedPdFeat = stdsc.fit_transform(pd_pureFeatReducDepip.T).T
    seriesClass_df = dfdata['class']
    return arrayNormedPdFeat,seriesClass_df.values.tolist()
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
def f_stdNormlize(df_featData):
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
def calcRoughlyClsfyPrecison(df_data,o_clafier,rsampMethdStr):
    df_propData_normed = f_stdNormlize(df_data)
    df_resampledFeat = f_runResample(df_propData_normed,rsampMethdStr)
    y = df_resampledFeat['class'].values.tolist()
    matX = df_resampledFeat.drop(columns=['class']).values
    n_cross = 5
    ls_scores = cross_val_score(o_clafier, matX, np.array(y,dtype=np.int32), cv=n_cross)
    fv_precison = ls_scores.mean()
    return fv_precison
def f_runResample(df_data, s_sampMthd):
    ls_colName_class = df_data.columns.values.tolist()
    ls_y = df_data['class'].values.tolist()
    mat_X = df_data.drop(columns=['class']).values
    obj_resampMod = c_resampData(mat_X, ls_y, s_sampMthd, ls_colName_class)
    d_maxAcc, arr_X_resampled, ls_y_resampled, df_resampledData = obj_resampMod.f_operResampling()
    return df_resampledData
def mainFun_clacProps_combCsv_MlPred(inFasta_p,inFasta_n,rsampMethdStr,othersTres,\
                                     ls_givenPropList,taskId,userFeatCsvPth,s_clsfier):
    alphabetFilPth = geneSmartPth('data','reducedAlphabet_full.txt')
    filepth_betterSchm = geneSmartPth('results',str(taskId)+'_goodSchmsList.txt')
    bestFeatPth_optRaac = geneSmartPth('results',str(taskId)+'_optRaacFeat'+'.csv')
    bestFeatCsvPth_multProp = geneSmartPth('results',str(taskId)+'_finalBestFeat.csv')
    precDict_perCombs = {}
    maxPrecision = 0
    bestFeat_maxPrec = {}
    # classifier = f_geneClfier_byStr(s_clsfier)
    classifier = c_mlClassifier(s_clsfier).f_geneMlClassifier(None)
    if len(ls_givenPropList)==1:
        s_curProp = ls_givenPropList[0]
        try:
            if s_curProp=='optiRaac':
                df_singleProp,accList,bestSchm = innerFun_optiRaacByRf(alphabetFilPth,\
                                                                       inFasta_p,inFasta_n,\
                                                                       rsampMethdStr,othersTres,\
                                                                       filepth_betterSchm,\
                                                                       bestFeatPth_optRaac,taskId,s_clsfier)
            elif s_curProp=='userGivenFeat':
                df_singleProp = calcMultiFeats(inFasta_p,inFasta_n,s_curProp,taskId,userFeatCsvPth)
            else:
                df_singleProp = calcMultiFeats(inFasta_p,inFasta_n,s_curProp,taskId,0)
            if s_curProp=='optiRaac':
                f_v_precRate = np.max(np.array(accList))
            else:
                f_v_precRate = calcRoughlyClsfyPrecison(df_singleProp,classifier,rsampMethdStr)
        except:
            # raise ErrorEditDefine(f'Something went wrong while the code was calculating {s_curProp}'\
            #                       '.The program is paused, please try another feature...')
            print(f'Something went wrong while the code was calculating {s_curProp}'\
                                  '.The program is paused, please try another feature...')
            precDict_perCombs[s_curProp] = 'omitted'
            bestFeat_maxPrec['precision'] = 'omitted'
            bestFeat_maxPrec['featMat'] = 'omitted'
            bestFeat_maxPrec['propName'] = 'omitted'
            print(f'{s_curProp} is omitted')
            globSet.addFail1Props(s_curProp)
        else:
            df_singleProp_5f = df_singleProp.applymap(lambda x: '%.5f'%x)
            precDict_perCombs[s_curProp] = f_v_precRate
            maxPrecision = f_v_precRate
            bestFeat_maxPrec['precision'] = f_v_precRate
            bestFeat_maxPrec['featMat'] = df_singleProp_5f
            bestFeat_maxPrec['propName'] = s_curProp
            print('Finished property: '+s_curProp)
            globSet.add_doneFeat(s_curProp)
        return precDict_perCombs,bestFeat_maxPrec
    else:
        raise ErrorEditDefine("The length of the passed feature list is not one.")
