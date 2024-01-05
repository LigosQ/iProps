#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 22:08:55 2022
@author: sealight
"""
import concurrent.futures
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from concurrent.futures import wait,FIRST_COMPLETED
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import argparse,datetime
import pandas as pd
from itertools import combinations
from files.mainFeatSystheOpt import *
from files.chkAdAdapFasta_1line import *
from files.delNoMeanAA import *
from files.class_calc1Dipep_1schm_noIO import *
from files.class_resampData import *
from files.class_mlClassifier import *
from files import globSet,config
from files.geneSmartPth import *
from files import getBestACCProps
from files.f_tsne_in import *
from files.f_umap_in import *
# from files.f_geneClfier import f_geneClfier_byStr
from files.class_mlClassifier import c_mlClassifier
class ErrorCoding(Exception):
    pass
def f_is2listEqual(ls_1,ls_2):
    if len(ls_1) == len(ls_2):
        for i in range(len(ls_1)):
            if ls_1[i]==ls_2[i]:
                pass
            else:
                return False
        return True
    else:
        raise ErrorCoding('Two list variables have different length.')
def f_concat2Df_h(df_data1, df_data2):
    ls_cols1 = df_data1.columns.values.tolist()
    ls_cols2 = df_data2.columns.values.tolist()
    b_isInDf1 = 'class' in ls_cols1
    b_isInDf2 = 'class' in ls_cols2
    if (b_isInDf1) and (b_isInDf2):
        if f_is2listEqual(df_data1['class'].values.tolist(),df_data2['class'].values.tolist()):
            df_noclass1 = df_data1.values
            df_noclass2 = df_data2.drop(columns=['class']).values
            ls_colNames1_c = df_data1.columns.values.tolist()
            ls_colNames2_c = df_data2.drop(columns=['class']).columns.values.tolist()
            ls_finalColName = ls_colNames1_c
            ls_finalColName.extend(ls_colNames2_c)
        else:
            raise ErrorCoding('The contacted data have different class/target.')
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
def f_concat2Df_v(df_data1, df_data2):
    ls_df1 = df_data1.columns.values.tolist()
    ls_df2 = df_data2.columns.values.tolist()
    if ls_df1 == ls_df2:
        arr_df1 = df_data1.values
        arr_df2 = df_data2.values
        arr_combed = np.vstack((arr_df1, arr_df2))
        df_combdDf = pd.DataFrame(arr_combed)
        df_combdDf.columns = ls_df1
    else:
        raise ErrorCoding('The contacted data are not equal in column names...')
    return df_combdDf
def f_tranTxt2Dict(s_alphaTxt):
    import pickle
    d_allSchm = dict()
    i_schmNo = 0
    try:
        with open(s_alphaTxt,'rb') as fid_schmPkl:
            s_allSchmLines = pickle.load(fid_schmPkl)
    except:
        raise ErrorCoding('Error: the code cannot open the group scheme pkl file.')
    ls_allGrpSchmStr = s_allSchmLines.split('\n')
    for i,s_schmStr_i in enumerate(ls_allGrpSchmStr):
        i_schmNo += 1
        d_schm_i = dict()
        s_line_strip = s_schmStr_i.strip()
        ls_subSchm = s_line_strip.split('#')
        if ls_subSchm[0]=='':
            ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
            d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
            d_schm_i = d_origAmAcid_2RedStr
        else:
            for s_item in ls_subSchm:
                d_schm_i[s_item[0]] = s_item
        d_allSchm[str(i_schmNo)] = d_schm_i
    return d_allSchm
def f_tranTxt2Dict_v0(s_alphaTxt):
    d_allSchm = dict()
    i_schmNo = 0
    try:
        with open(s_alphaTxt, 'r') as fid_alphaTxt:
            for s_line_i in fid_alphaTxt.readlines():
                i_schmNo += 1
                d_schm_i = dict()
                s_line_strip = s_line_i.strip()
                ls_subSchm = s_line_strip.split('#')
                if ls_subSchm[0]=='':
                    ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
                    d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
                    d_schm_i = d_origAmAcid_2RedStr
                else:
                    for s_item in ls_subSchm:
                        d_schm_i[s_item[0]] = s_item
                d_allSchm[str(i_schmNo)] = d_schm_i
    except IOError:
        raise ErrorCoding(''.join(['There is an error when open and load ',s_alphaTxt]))
    return d_allSchm
def f_genePosNegFeat_by1Schm(s_posPth,s_negPth,d_alphabet, i_schmNo):
    df_final3Feats = None
    for i_dipepType in range(3):
        obj  = c_calc1Dipep_1schm(i_dipepType)
        obj.inFilePth = s_posPth
        obj.alphaBet = d_alphabet
        obj.negOrPos = 'pos'
        obj.recodeSeq(i_dipepType,i_schmNo)
        df_dipepFeats_pos = obj.f_getDipepDf_AdCsv_ofCurShm()
        obj.inFilePth = s_negPth
        obj.negOrPos = 'neg'
        obj.recodeSeq(i_dipepType,i_schmNo)
        df_dipepFeats_neg = obj.f_getDipepDf_AdCsv_ofCurShm()
        if i_dipepType == 0:
            df_final3Feats = f_concat2Df_v(df_dipepFeats_pos,df_dipepFeats_neg)
        else:
            df_curDipepType = f_concat2Df_v(df_dipepFeats_pos,df_dipepFeats_neg)
            df_curDipepType_noCls = df_curDipepType.drop(columns=['class'])
            df_final3Feats = f_concat2Df_h(df_final3Feats,df_curDipepType_noCls)
    return df_final3Feats
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
def f_clacOptRaac_1Schm(s_posPth, s_negPth, s_clfer, d_curSchm,s_sampMthd, i_schmNo, b_isSaveDf):
    df_3dipep_feat = f_genePosNegFeat_by1Schm(s_posPth, s_negPth,d_curSchm,i_schmNo)
    obj_classifier = c_mlClassifier(s_clfer)
    classifier = obj_classifier.f_geneMlClassifier(None)
    df_3dipep_feat = f_stdNormlize(df_3dipep_feat)
    df_resampledFeat = f_runResample(df_3dipep_feat,s_sampMthd)
    y = df_resampledFeat['class'].values.tolist()
    matX = df_resampledFeat.drop(columns=['class']).values
    n_cross = 5
    ls_scores = cross_val_score(classifier, matX, y, cv=n_cross)
    f_precison = np.mean(ls_scores)
    d_resultInfo = dict()
    precDict_perCombs = dict()
    d_resultInfo['precision']=f_precison
    if b_isSaveDf:
        d_resultInfo['featMat']=df_3dipep_feat.applymap(lambda x: '%.5f'%x)
    else:
        d_resultInfo['featMat']=None
    d_resultInfo['redDict']=d_curSchm
    precDict_perCombs[''.join(['Raac-', str(i_schmNo)])] = f_precison
    print(precDict_perCombs)
    return precDict_perCombs,d_resultInfo
def f_calcSingleProps(s_1propName, d_otherParas):
    if 'Raac' in s_1propName:
        i_schmNo = int(s_1propName.split('-')[1])
        d_curSchm = d_otherParas['d_allSchm'][str(i_schmNo)]
        b_isSaveDf = False
        precDict_perCombs,bestFeat_maxPrec = \
            f_clacOptRaac_1Schm(d_otherParas['inFasta_p'],d_otherParas['inFasta_n'],d_otherParas['s_clfier'],\
                                d_curSchm, d_otherParas['rsampMethdStr'],i_schmNo,\
                                b_isSaveDf)
    elif 'userGivenFeat' in s_1propName:
        s_csvpth = globSet.getGlobParas()['userCsv']
        precDict_perCombs,bestFeat_maxPrec = \
            mainFun_clacProps_combCsv_MlPred(d_otherParas['inFasta_p'],d_otherParas['inFasta_n'],\
                                             d_otherParas['rsampMethdStr'],d_otherParas['othersTres'],\
                                             [s_1propName],d_otherParas['s_taskID'],s_csvpth, d_otherParas['s_clfier'])
        if s_1propName in globSet.getFailProps():
            pass
        else:
            globSet.add_finalProp(s_1propName,bestFeat_maxPrec['precision'])
    else:
        precDict_perCombs,bestFeat_maxPrec = \
            mainFun_clacProps_combCsv_MlPred(d_otherParas['inFasta_p'],d_otherParas['inFasta_n'],\
                                             d_otherParas['rsampMethdStr'],d_otherParas['othersTres'],\
                                             [s_1propName],d_otherParas['s_taskID'],0, d_otherParas['s_clfier'])
        if s_1propName in globSet.getFailProps():
            pass
        else:
            globSet.add_finalProp(s_1propName,bestFeat_maxPrec['precision'])
    return [precDict_perCombs,bestFeat_maxPrec]
def f_calc1Prop_geneCsv(s_1propName, d_otherParas):
    if 'Raac' in s_1propName:
        i_schmNo = int(s_1propName.split('-')[1])
        d_curSchm = d_otherParas['d_allSchm'][str(i_schmNo)]
        b_isSaveDf = True
        precDict_perCombs,bestFeat_maxPrec = \
            f_clacOptRaac_1Schm(d_otherParas['inFasta_p'],d_otherParas['inFasta_n'],d_otherParas['s_clfier'],\
                                d_curSchm, d_otherParas['rsampMethdStr'],i_schmNo,\
                                b_isSaveDf)
    else:
        precDict_perCombs,bestFeat_maxPrec = \
            mainFun_clacProps_combCsv_MlPred(d_otherParas['inFasta_p'],d_otherParas['inFasta_n'],\
                                             d_otherParas['rsampMethdStr'],d_otherParas['othersTres'],\
                                             [s_1propName],d_otherParas['s_taskID'],0,d_otherParas['s_clfier'])
    s_outCsvFName = ''.join([s_1propName,'_',d_otherParas['s_taskID'],'.csv'])
    p_csvSavePth = geneSmartPth('results',s_outCsvFName)
    if bestFeat_maxPrec['featMat'] is None:
        pass
    else:
        df_featForSave = bestFeat_maxPrec['featMat']
        df_featForSave.to_csv(p_csvSavePth, index=False)
        globSet.set_featCsvPth(s_1propName, p_csvSavePth)
    return [precDict_perCombs,bestFeat_maxPrec]
def f_dispFinishedTask(futureList):
    ls_taskDone = []
    done, unfinished = concurrent.futures.wait(futureList, return_when=FIRST_COMPLETED)
    while len(done)!=len(futureList):
        done, unfinished = concurrent.futures.wait(futureList, return_when=FIRST_COMPLETED)
        for d in done:
            if d in ls_taskDone:
                pass
            else:
                print(d.result()[0])
                ls_taskDone.append(d)
                for s_key,s_val in list(d.result()[0].items()):
                    if s_key in globSet.get_doneFeat():
                        pass
                    else:
                        globSet.add_doneFeat(s_key)
def f_clacProps_multiThread(ls_props, d_paras):
    ls_finishProp = []
    d_allPropInfo = dict()
    d_allSchmInfo = globSet.getReduceSchm()
    inFasta_p_t = fun_checkAdAdaptSeqInOneLine(d_paras['inFasta_p'])
    inFasta_n_t = fun_checkAdAdaptSeqInOneLine(d_paras['inFasta_n'])
    inFasta_p = delNoMeanAA_mainFun(inFasta_p_t)
    inFasta_n = delNoMeanAA_mainFun(inFasta_n_t)
    d_paras['inFasta_p'] = inFasta_p
    d_paras['inFasta_n'] = inFasta_n
    d_paras['d_allSchm'] = d_allSchmInfo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureList = {executor.submit(f_calcSingleProps, s_prop, d_paras): s_prop for s_prop in ls_props}
        f_dispFinishedTask(futureList)
        done, unfinished = concurrent.futures.wait(futureList, return_when=FIRST_COMPLETED)
        for d in done:
            d_curTaskInfo = d.result()[0]
            for key, vals in d_curTaskInfo.items():
                if key in globSet.getFailProps():
                    pass
                else:
                    d_allPropInfo[key] = vals
                    ls_finishProp.append(key)
    concurrent.futures.wait(futureList)
    s_temp = ''.format(datetime.datetime.now())
    return d_allPropInfo,ls_finishProp
def f_clacTopN_raac_multiThread(ls_props, d_paras):
    ls_finishProp = []
    d_allPropInfo = dict()
    d_allSchmInfo = globSet.getReduceSchm()
    inFasta_p_t = fun_checkAdAdaptSeqInOneLine(d_paras['inFasta_p'])
    inFasta_n_t = fun_checkAdAdaptSeqInOneLine(d_paras['inFasta_n'])
    inFasta_p = delNoMeanAA_mainFun(inFasta_p_t)
    inFasta_n = delNoMeanAA_mainFun(inFasta_n_t)
    d_paras['inFasta_p'] = inFasta_p
    d_paras['inFasta_n'] = inFasta_n
    d_paras['d_allSchm'] = d_allSchmInfo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureList = {executor.submit(f_calc1Prop_geneCsv, s_prop, d_paras): s_prop for s_prop in ls_props}
        f_dispFinishedTask(futureList)
        done, unfinished = concurrent.futures.wait(futureList, return_when=FIRST_COMPLETED)
        for d in done:
            d_curTaskInfo = d.result()[0]
            for key, vals in d_curTaskInfo.items():
                d_allPropInfo[key] = vals
                ls_finishProp.append(key)
    executor.shutdown(wait=True)
    return d_allPropInfo, ls_finishProp
def f_check_ifOptiRaacIn(ls_finishProps):
    b_status = False
    for s_curProps in ls_finishProps:
        if 'raac' in s_curProps.lower():
            b_status = True
            break
    return b_status
def f_findTopN_raacProps(d_allPropInfo,i_topNum):
    ls_allRaacNames = []
    ls_allRaacACC = []
    for key,val in d_allPropInfo.items():
        if 'raac' in key.lower():
            ls_allRaacNames.append(key)
            ls_allRaacACC.append(val)
        else:
            pass
    ls_sortedId_ACClist = sorted(range(len(ls_allRaacACC)), key=lambda k: ls_allRaacACC[k], reverse=True)
    if len(ls_allRaacACC)>=i_topNum:
        ls_topN_index = ls_sortedId_ACClist[0:i_topNum]
        ls_topN_schmNames = [ls_allRaacNames[i_item] for i_item in ls_topN_index]
    else:
        ls_topN_schmNames = ls_allRaacNames
    print(ls_topN_schmNames)
    return ls_topN_schmNames
def f_removeRaacSchm(ls_finishProp_stage1):
    ls_finished_noRaac = []
    for s_curProp in ls_finishProp_stage1:
        if 'raac' in s_curProp.lower():
            pass
        else:
            ls_finished_noRaac.append(s_curProp)
    return ls_finished_noRaac
def f_geneCombPairList(ls_finalProps, i_combNum=2):
    ls_combPairs = []
    if len(ls_finalProps)==1:
        raise ErrorCoding('The finished property number is only 1. Cannot do the combination process...')
    else:
        if len(ls_finalProps)<i_combNum:
            i_combNum = len(ls_finalProps)
            print(f'The number of combinations you set exceeds the maximum {0}, and the code will use that maximum to combine'.format(len(ls_finalProps)))
        else:
            pass
    for item in combinations(ls_finalProps,i_combNum):
        ls_combPairs.append(item)
    return ls_combPairs
def f_comb2csvFile(s_prop1,s_prop2,taskID):
    s_csvFileName1 = ''.join([s_prop1,'_',str(taskID),'.csv'])
    p_pthCsv1 = geneSmartPth('results', s_csvFileName1)
    s_csvFileName2 = ''.join([s_prop2,'_',str(taskID),'.csv'])
    p_pthCsv2 = geneSmartPth('results', s_csvFileName2)
    try:
        df_prop1 = pd.read_csv(p_pthCsv1)
        df_prop2 = pd.read_csv(p_pthCsv2)
    except:
        raise ErrorCoding('There is an error when reading the csv files: '+s_prop1+'/'+s_prop2)
    df_combinedProp = f_concat2Df_h(df_prop1, df_prop2)
    return df_combinedProp
def f_evalDfPerformance(df_propData,s_sampMthd,obj_clsfer):
    df_propData_normed = f_stdNormlize(df_propData)
    df_resampledFeat = f_runResample(df_propData_normed,s_sampMthd)
    y = df_resampledFeat['class'].values.tolist()
    matX = df_resampledFeat.drop(columns=['class']).values
    n_cross = 5
    ls_scores = cross_val_score(obj_clsfer, matX, np.array(y,dtype=np.int32), cv=n_cross)
    f_precison = ls_scores.mean()
    return f_precison
def f_getDf(s_propName,s_taskID):
    s_csvFileName = ''.join([s_propName,'_',str(s_taskID),'.csv'])
    p_pthCsv = geneSmartPth('results', s_csvFileName)
    try:
        df_csvFeat = pd.read_csv(p_pthCsv)
    except:
        raise ErrorCoding('There is error when reading the csv file(f_getDf)...')
    return df_csvFeat
def f_rmClassInColumns(ls_colums, s_classLab):
    ls_outVarb = []
    for i in range(len(ls_colums)):
        if ls_colums[i] == s_classLab:
            pass
        else:
            ls_outVarb.append(ls_colums[i])
    return ls_outVarb
def f_geneColNames_multiDf(ls_dfVariable):
    if len(ls_dfVariable)>=2:
        ls_finalColNames = []
        for i,df_i in enumerate(ls_dfVariable):
            if i==0:
                ls_finalColNames_0 = df_i.columns.values.tolist()
                ls_finalColNames = f_rmClassInColumns(ls_finalColNames_0, 'class')
            elif i==(len(ls_dfVariable)-1):
                ls_colNames_i = df_i.columns.values.tolist()
                ls_colNames_i_noClass = f_rmClassInColumns(ls_colNames_i, 'class')
                ls_finalColNames.extend(ls_colNames_i_noClass)
                ls_finalColNames.append('class')
            else:
                ls_colNames_i = df_i.columns.values.tolist()
                ls_colNames_i_noClass = f_rmClassInColumns(ls_colNames_i, 'class')
                ls_finalColNames.extend(ls_colNames_i_noClass)
        return ls_finalColNames
    else:
        raise ErrorCoding('The given df list has only one element...')
def f_concat_pureFeatMat(ls_dfVariable, s_classLab):
    if len(ls_dfVariable)>=2:
        for i,df_i in enumerate(ls_dfVariable):
            if i==0:
                df_current = df_i.drop(columns=[s_classLab])
                arrFinal = df_current.values
            elif i==(len(ls_dfVariable)-1):
                ser_classCol = df_i[s_classLab].values
                df_current = df_i.drop(columns=[s_classLab])
                arr_feat_i = df_current.values
                arrFinal = np.vstack((arrFinal.T, arr_feat_i.T)).T
                arrFinal = np.vstack((arrFinal.T, ser_classCol.T)).T
            else:
                df_current = df_i.drop(columns=[s_classLab])
                arr_feat_i = df_current.values
                arrFinal = np.vstack((arrFinal.T, arr_feat_i.T)).T
        return arrFinal
    else:
        raise ErrorCoding('The given df list has only one element...')
def f_comb_N_csv(ls_combPropListPairs,s_taskID):
    ls_df_list = []
    for i, s_propName in enumerate(ls_combPropListPairs):
        df_csvFeat = f_getDf(s_propName, s_taskID)
        ls_df_list.append(df_csvFeat)
    ls_finalColNames = f_geneColNames_multiDf(ls_df_list)
    arr_finalFeatMat = f_concat_pureFeatMat(ls_df_list, 'class')
    df_finalCombed = pd.DataFrame(arr_finalFeatMat, columns=ls_finalColNames)
    return df_finalCombed
def f_combCsvEval_inMultiPrcess(ls_combPair,s_taskID,s_rsmpModel,obj_clsfer_specific):
    if len(ls_combPair)==2:
        s_prop1 = ls_combPair[0]
        s_prop2 = ls_combPair[1]
        df_combDf_multiProps = f_comb2csvFile(s_prop1, s_prop2,s_taskID)
    elif len(ls_combPair)<2:
        pass
    else:
        df_combDf_multiProps = f_comb_N_csv(ls_combPair,s_taskID)
    fv_ACC = f_evalDfPerformance(df_combDf_multiProps, s_rsmpModel,obj_clsfer_specific)
    s_combProp_name = '+'.join(ls_combPair)
    print([s_combProp_name, fv_ACC])
    globSet.add_finalProp(s_combProp_name, fv_ACC)
    return [s_combProp_name, fv_ACC]
def f_comb2csvfile_evalution(ls_finishSingleProps_stage2,d_paras,d_allPropInfo,ls_finishProps):
    i_combFeat_num = globSet.getFeatNumInPairs()
    ls_combPropPairs = f_geneCombPairList(ls_finishSingleProps_stage2,i_combFeat_num)
    s_taskID = d_paras['s_taskID']
    s_clferName = d_paras['s_clfier']
    s_rsmpModel = d_paras['rsampMethdStr']
    # obj_clsfer_specific = f_geneClfier_byStr(s_clferName)
    obj_clsfer_specific = c_mlClassifier(s_clferName).f_geneMlClassifier(None)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureList = {executor.submit(f_combCsvEval_inMultiPrcess,ls_1combPair, s_taskID,s_rsmpModel,obj_clsfer_specific): ls_1combPair for ls_1combPair in ls_combPropPairs}
        done, unfinished = concurrent.futures.wait(futureList, return_when=FIRST_COMPLETED)
    concurrent.futures.wait(futureList)
def f_updateDict_delUselessRaacAddTop(d_origPropInfo,d_raac_topN):
    for s_key,fv_acc in d_raac_topN.items():
        globSet.add_finalProp(s_key,fv_acc)
def f_updateDict_noRaac(d_origPropInfo):
    for s_key,fv_acc in d_origPropInfo.items():
        globSet.add_finalProp(s_key,fv_acc)
def f_getFinalPropList_beforeComb(s_property,d_allPropInfo,ls_finishProps,d_paras,i_featNum_inComb):
    ls_props_t = s_property.split(',')
    b_isHasOptiRaac = f_check_ifOptiRaacIn(ls_finishProps)
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    i_topPropNum = d_allParas['orDip']
    b_doComb = False
    if b_isHasOptiRaac:
        ls_topN_Raac = f_findTopN_raacProps(d_allPropInfo,i_topPropNum)
        print('topN props are :')
        print(ls_topN_Raac)
        print('The classification realization of the top N features with the best classification performance is as follows:\n')
        d_allPropInfo_stage2, ls_finishProp_stage2 = f_clacTopN_raac_multiThread(ls_topN_Raac,d_paras)
        ls_finishProps_stage1_noRaac = f_removeRaacSchm(ls_finishProps)
        ls_finishProps_stage1_noRaac.extend(ls_topN_Raac)
        ls_finishSingleProps_stage2 = ls_finishProps_stage1_noRaac
        if i_featNum_inComb>=2:
            b_doComb = True
        f_updateDict_delUselessRaacAddTop(d_allPropInfo,d_allPropInfo_stage2)
    else:
        if len(ls_props_t)>=2 and i_featNum_inComb>=2:
            ls_finishSingleProps_stage2 = ls_finishProps
            b_doComb = True
        elif len(ls_props_t)>=2 and i_featNum_inComb==1:
            ls_finishSingleProps_stage2 = ls_finishProps
            b_doComb = False
        elif len(ls_props_t)==1 and i_featNum_inComb>=2:
            ls_finishSingleProps_stage2 = ls_finishProps
            b_doComb = False
        else:
            ls_finishSingleProps_stage2 = ls_finishProps
            b_doComb = False
    return ls_finishSingleProps_stage2,b_doComb
def f_remUselessKeyvalPair(d_propNameAcc):
    d_usefulDict = dict()
    for s_key,f_val in d_propNameAcc.items():
        if 'best' in s_key:
            pass
        else:
            d_usefulDict[s_key] = f_val
    return d_usefulDict
def get_first_15_elements(list_in,N=15):
  if len(list_in) <= N:
    return list_in
  else:
    return list_in[:N]
def sort_dict_by_value(dict_in):
  dict_temp = dict()
  for key,val in dict_in.items():
      if key == 'bestFeat':
          pass
      elif key == 'bestFeat-predictAccuray':
          pass
      else:
          dict_temp[key] = val

  key_list, val_list = zip(*sorted(dict_temp.items(), key=lambda x: x[1], reverse=True))
  return get_first_15_elements(key_list), get_first_15_elements(val_list)
def f_sortAllProps(s_taskID, i_topN_best):
    d_allFinalProp_ACC = globSet.get_finalProps()
    d_allFinalProp_ACC = f_remUselessKeyvalPair(d_allFinalProp_ACC)
    ls_finalPropAcc = []
    for s_key,f_acc in d_allFinalProp_ACC.items():
        if s_key == 'optiRaac':
            pass
        else:
            ls_finalPropAcc.append([s_key,f_acc])
    i_allPropsNum = len(ls_finalPropAcc)
    if i_topN_best <= i_allPropsNum:
        if i_allPropsNum<=15:
            i_topN_best = i_allPropsNum
        else:
            i_topN_best = 15
    else:
        print('The top N best number: n >= length of all the propops, the number is set to be the number of all currnt props')
        if i_allPropsNum<=15:
            i_topN_best = i_allPropsNum
        else:
            i_topN_best = 15
    # sorted_id = sorted(range(len(ls_finalPropAcc)), key=lambda k: ls_finalPropAcc[k][1], reverse=True)
    # ls_finalPropNames_sorted = [ls_finalPropAcc[i][0] for i in range(len(sorted_id)) if (i+1)<=i_topN_best]
    # ls_finalPropAcc_sorted = [ls_finalPropAcc[i][1] for i in range(len(sorted_id)) if (i+1)<=i_topN_best]
    ls_finalPropNames_sorted, ls_finalPropAcc_sorted = sort_dict_by_value(d_allFinalProp_ACC)
    fig,ax = plt.subplots()
    ax.barh(ls_finalPropNames_sorted, ls_finalPropAcc_sorted) 
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False) 
    ax.xaxis.set_ticks_position('none') 
    ax.yaxis.set_ticks_position('none') 
    ax.xaxis.set_tick_params(pad=5) 
    ax.yaxis.set_tick_params(pad=10) 
    ax.grid(visible = True, color='#4F9BFA', 
            linestyle='-.', linewidth=0.5, 
            alpha=0.4) 
    ax.invert_yaxis() 
    for i in ax.patches:
        plt.text(i.get_width()+0.05, i.get_y()+0.5, 
                 str(round((i.get_width()), 3)), 
                 fontsize=10, fontweight='light', 
                 ) 
    plt.xlabel("Identification accuracy") 
    plt.ylabel("Protein properties")
    fig.text(0.97, 0.01, 'iProp', fontsize=12, 
              color='grey', ha='right', va='bottom', 
              alpha=0.7) 
    ls_sortListName = [s_taskID,'_propList','.pdf']
    s_sortListFigName = ''.join(ls_sortListName)
    p_fullPth_sortLsPdf = geneSmartPth('results', s_sortListFigName)
    plt.savefig(p_fullPth_sortLsPdf, dpi=600)
    ls_sortListName[-1] = '.png'
    s_sortListFigName = ''.join(ls_sortListName)
    p_fullPth_sortLsPng = geneSmartPth('results', s_sortListFigName)
    plt.savefig(p_fullPth_sortLsPng, dpi=72)
    globSet.set_finalTaskResults('sortListPng',p_fullPth_sortLsPng)
    globSet.set_task_done('accSortList_progPloted')
    globSet.set_finalTaskResults('accTopN-pdfFile', p_fullPth_sortLsPdf)
def f_procPara_then_calc(s_posFile, s_negFile, s_sampMthd, s_clsfier, s_property,s_taskID,para_featNum):
    d_givenParas = dict()
    d_givenParas['inFasta_p'] = s_posFile
    d_givenParas['inFasta_n'] = s_negFile
    d_givenParas['rsampMethdStr'] = s_sampMthd
    d_givenParas['othersTres'] = 0
    d_givenParas['s_taskID'] = s_taskID
    d_givenParas['s_clfier'] = s_clsfier
    ls_props_t = s_property.split(',')
    ls_props = []
    for item in ls_props_t:
        if item == 'optiRaac':
            if globSet.getReduceSchm() is None:
                d_allSchmInfo = f_tranTxt2Dict('data/groupSchms.pkl')
                globSet.setReduceSchm(d_allSchmInfo)
            else:
                pass
            for i in range(1,len(d_allSchmInfo)+1):
                ls_props.append(''.join(['Raac-', str(i)]))
        else:
            ls_props.append(item)
    globSet.add_allTask(ls_props)
    d_allPropInfo,ls_finishProps = f_clacProps_multiThread(ls_props, d_givenParas)
    ls_finishSingleProps_stage2,b_doComb = f_getFinalPropList_beforeComb(s_property,\
                                                                         d_allPropInfo,ls_finishProps,\
                                                                         d_givenParas,\
                                                                         para_featNum)
    globSet.setFeatCalcFinish()
    if b_doComb:
        print('The features involved in feature mixing are: ')
        print(ls_finishSingleProps_stage2)
        globSet.setInCombPhase()
        f_comb2csvfile_evalution(ls_finishSingleProps_stage2, d_givenParas,d_allPropInfo,ls_finishProps)
    else:
        print('The features involved in feature mixing are: None')
    # obj_clsfer = f_geneClfier_byStr(s_clsfier)
    obj_clsfer = c_mlClassifier(s_clsfier).f_geneMlClassifier(None)
    p_bestFeatCsv,s_bestPropName,f_bestScore = getBestACCProps.f_compListGetTheBestProp(s_sampMthd,obj_clsfer,s_taskID)
    print(''.join(['Best Feature: ',s_bestPropName]))
    print(''.join(['Best Score: ',format(f_bestScore,'.6f')]))
    globSet.set_bestFeat_csvPth(p_bestFeatCsv)
    globSet.set_taskFinishStatus(True)
    main_plot_tsne2d(p_bestFeatCsv,s_sampMthd,s_taskID)
    f_umapProc_plotFig(p_bestFeatCsv,s_sampMthd,s_taskID)
    f_sortAllProps(s_taskID,2)
    return d_allPropInfo,ls_finishProps
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate the properties of proteins")
    parser.add_argument('-p', '--posFile', help="The input file should be saved in the fasta format.", required=True)
    parser.add_argument('-n', '--negFile', help="The input file should be saved in the fasta format.", required=True)
    parser.add_argument('-s', '--sampMthd', help='The method used for the imbalanced data.', required=True)
    parser.add_argument('-c', '--clsfier', help='The embeded classifier used in the property evaluation.', required=True)
    parser.add_argument('-p', '--property', help='The protein properties evaluated. Properties need be separated by commas.', required=True)
    args = parser.parse_args()
    f_procPara_then_calc(args.posFile, args.negFile, args.sampMthd, args.clsfier, args.property)
    