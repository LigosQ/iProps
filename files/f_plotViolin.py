#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:52:20 2023
@author: sealight
funchtion: plot the violin figure
"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from files.geneSmartPth import *
class ErrorEditDefine(Exception):
    pass
def f_delClassInColList(ls_colList):
    ls_colList_0class = []
    for i in range(len(ls_colList)):
        if ls_colList[i]=='class':
            pass
        else:
            ls_colList_0class.append(ls_colList[i])
    return ls_colList_0class
def f_processDf_0(df_origDf, s_classColLab):
    ls_classCol_str = df_origDf[s_classColLab].replace([0, 1], ['Negative', 'Positive']).values.tolist() 
    ls_colList_0class = f_delClassInColList(ls_columnNames)
    ls_featVal_dim1 = df_origDf[ls_colList_0class[0]].values.tolist()
    ls_featNameStr_dim1 = ['Dim-1' for item in ls_featVal_dim1] 
    ls_featVal_dim2 = df_origDf[ls_colList_0class[1]].values.tolist()
    ls_featNameStr_dim2 = ['Dim-2' for item in ls_featVal_dim2]
    arr_finalClass = np.array([*ls_classCol_str, *ls_classCol_str])
    arr_featVal = np.array([*ls_featVal_dim1, *ls_featVal_dim2])
    arr_featType = np.array([*ls_featNameStr_dim1,*ls_featNameStr_dim2])
    arr_dfMat = np.vstack((arr_finalClass.T, arr_featVal.T, arr_featType.T)).T
    ls_finalColNames = ['Type','Value','Dimension']
    df_adaptedDf = pd.DataFrame(arr_dfMat, columns=ls_finalColNames)
    df_adaptedDf = df_adaptedDf.astype({'Value':'float'})
    return df_adaptedDf
def f_adaptOrigDf(df_origDf):
    ls_columnNames = df_origDf.columns.values.tolist()
    if len(ls_columnNames)==3:
        if 'class' in ls_columnNames:
            return f_processDf_0(df_origDf, 'class')
        elif 'label' in ls_columnNames:
            return f_processDf_0(df_origDf, 'label')
        else:
            raise ErrorEditDefine('"class/label" is not in the columns, the current version should have "class" in the columns')
    else:
        raise ErrorEditDefine('The number of columns !=3, please check your dataframe value...')
def f_chgClass2Label(ls_colNames):
    ls_chgedColNames = ['label' if ls_colNames[i]=='class' else ls_colNames[i] for i in range(len(ls_colNames)) ]
    return ls_chgedColNames
def f_getBalanceData(df_1,df_2):
    ls_shape1 = df_1.shape
    ls_shape2 = df_2.shape
    if ls_shape1[0] > ls_shape2[0]:
        import random
        print([ls_shape1[0],ls_shape2[0]])
        ls_randInd = random.sample(range(0, ls_shape1[0]), ls_shape2[0])
        df_1_adapt = df_1.iloc[ls_randInd]
        df_2_adapt = df_2
    elif ls_shape1[0] == ls_shape2[0]:
        df_1_adapt = df_1
        df_2_adapt = df_2
    else:
        import random
        print([ls_shape1[0],ls_shape2[0]])
        ls_randInd = random.sample(range(0, ls_shape2[0]), ls_shape1[0])
        df_2_adapt = df_2.iloc[ls_randInd]
        df_1_adapt = df_1
    return df_1_adapt,df_2_adapt
def f_processDf(df_origDf, s_classColLab):
    df_origDf[s_classColLab] = df_origDf[s_classColLab].replace([0, 1], ['negative', 'positive']) 
    df_origDf.columns = f_chgClass2Label(df_origDf.columns.values.tolist())
    df_pos = df_origDf[(df_origDf.label=="positive")]
    df_neg = df_origDf[(df_origDf.label=="negative")]
    df_pos, df_neg = f_getBalanceData(df_pos, df_neg)
    df_pos_noLab = df_pos.drop(columns=['label'])
    df_neg_noLab = df_neg.drop(columns=['label'])
    dim1_pos = np.array(df_pos_noLab.values[:, 0])
    dim2_pos = np.array(df_pos_noLab.values[:, 1])
    dim1_neg = np.array(df_neg_noLab.values[:, 0])
    dim2_neg = np.array(df_neg_noLab.values[:, 1])
    arr_feats = np.vstack((dim1_pos.T, dim1_neg.T, dim2_pos.T, dim2_neg.T)).T
    ls_finalColName = ['Dim1(pos)','Dim1(neg)','Dim2(pos)','Dim2(neg)']
    df_adapted = pd.DataFrame(arr_feats, columns=ls_finalColName)
    df_adapted = df_adapted.astype({'Dim1(pos)':'float', 'Dim1(neg)':'float', 'Dim2(pos)':'float','Dim2(neg)':'float'})
    return df_adapted
def f_adaptDf_forCompViolin(df_origDf):
    ls_columnNames = df_origDf.columns.values.tolist()
    if len(ls_columnNames)==3:
        if 'class' in ls_columnNames:
            ls_newColumn = []
            for i,s_name in enumerate(ls_columnNames):
                if s_name.lower() == 'class':
                    ls_newColumn.append('label')
                else:
                    ls_newColumn.append(s_name)
            df_origDf.columns = ls_newColumn
            return f_processDf(df_origDf, 'label')
        elif 'label' in ls_columnNames:
            return f_processDf(df_origDf, 'label')
        else:
            raise ErrorEditDefine('"class/label" is not in the columns, the current version should have "class" in the columns')
    else:
        raise ErrorEditDefine('The number of columns !=3, please check your dataframe value...')
def f_plotViolin_2comp(df_data, s_taskID, s_tsneOrUmap):
    df_adapted = f_adaptOrigDf(df_data)
    f, ax = plt.subplots()
    sns.violinplot(x="Dimension",
                    y="Value",
                    hue="Type",
                    data=df_adapted,
                    split=True,
                    inner='quartiles')
    s_outPDF_Name = ''.join([s_taskID,'_', s_tsneOrUmap, '_violin.pdf'])
    p_outPDF_Pth = geneSmartPth('results', s_outPDF_Name)
    plt.savefig(p_outPDF_Pth,dpi=600)
    s_outPNG_Name = ''.join([s_taskID,'_', s_tsneOrUmap, '_violin.png'])
    p_outPNG_Pth = geneSmartPth('results', s_outPNG_Name)
    plt.savefig(p_outPNG_Pth,dpi=72)
    return df_adapted
def f_plotViolin_2d_fullViolin(data, s_taskID, s_tsneOrUmap):
    if isinstance(data, pd.DataFrame):
        df_data = data 
    elif data.endswith('csv'):
        df_data = pd.read_csv(data)
    else:
        raise ErrorEditDefine('The 1st paramter isnot dataframe or csv file path, only these two types are supportted...')
    df_adapted = f_adaptDf_forCompViolin(df_data)
    f, ax = plt.subplots()
    sns.violinplot(data=df_adapted, palette="Set3", bw=.2, cut=1, linewidth=1,
                   split=True)
    s_outPDF_Name = ''.join([s_taskID,'_', s_tsneOrUmap, '_violin.pdf'])
    p_outPDF_Pth = geneSmartPth('results', s_outPDF_Name)
    plt.savefig(p_outPDF_Pth,dpi=600)
    s_outPNG_Name = ''.join([s_taskID,'_', s_tsneOrUmap, '_violin.png'])
    p_outPNG_Pth = geneSmartPth('results', s_outPNG_Name)
    plt.savefig(p_outPNG_Pth,dpi=72)
    return s_outPDF_Name, s_outPNG_Name
