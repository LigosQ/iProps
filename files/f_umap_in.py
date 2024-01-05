#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 08:34:42 2023
@author: sealight
"""
import random
import numpy as np
import pandas as pd
from umap import UMAP
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from files.class_resampData import *
from files import globSet,config
from files.f_plotViolin import *
def f_runResample(df_data, s_sampMthd):
    ls_colName_class = df_data.columns.values.tolist()
    ls_y = df_data['class'].values.tolist()
    mat_X = df_data.drop(columns=['class']).values
    obj_resampMod = c_resampData(mat_X, ls_y, s_sampMthd, ls_colName_class)
    d_maxAcc, arr_X_resampled, ls_y_resampled, df_resampledData = obj_resampMod.f_operResampling()
    return df_resampledData
def f_stdNormlize_in(df_featData):
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
def f_resamplData(df_Protfeat,s_sampMthd):
    df_stdedDf = f_stdNormlize_in(df_Protfeat)
    df_resampledFeat = f_runResample(df_stdedDf,s_sampMthd)
    return df_resampledFeat
def chart(X, y):
    arr_concat=np.concatenate((X, y.reshape(y.shape[0],1)), axis=1)
    df=pd.DataFrame(arr_concat, columns=['x', 'y', 'z', 'class'])
    df['class'] = df['class'].astype(int)
    ls_y = df['class']
    df.sort_values(by='class', axis=0, ascending=True, inplace=True)
    plt.figure()
    ax = plt.axes(projection='3d')
    ls_color = ['#3F9475' if ls_y[i]==1 else '#9873A2' for i in range(len(ls_y))]
    ax.scatter(df['x'],df['y'],df['z'],c=ls_color, alpha=0.2)     
    plt.show()
def f_getIndex(ls_y, val):
    ls_index = [True if ls_y[i]==val else False for i in range(len(ls_y))]
    return ls_index
def umap_visual(X,y,p_outPDFpth,p_outPNG_fullPth):
    df_matX = pd.DataFrame(X, columns=['x', 'y'])
    ls_index_p = f_getIndex(y, 1)
    ls_index_n = f_getIndex(y, 0)
    X_p = X[ls_index_p,:].copy()
    X_n = X[ls_index_n,:].copy()
    fig_Pid = plt.figure() 
    facecolorsList = ['#3F9475','#FC9A98','#7ED5FE','#85CDBB','#8fc8c5','#95dafc','#d1ebcb','#f2eddb','#1df99e','#998ffe']
    edgeColorList = ['#2E6D56','#DB6562','#52A5D1','#43A38D','#7bbebb','#81cee9','#90b97d','#ccd5a5','#5bd0a0','#8882d8']
    numColorPairs = len(facecolorsList)               
    colorInd = random.randint(0,numColorPairs-1);
    curFaceColor = facecolorsList[colorInd]
    curEdgeColor = edgeColorList[colorInd]
    labels1  = ['negative','positive']
    plt.scatter(X_p[:,0], X_p[:,1], marker='o',facecolor=curFaceColor,edgecolors=curEdgeColor,s=135,alpha=0.5)
    colorInd2 = random.randint(0,numColorPairs-1);
    while colorInd2==colorInd:
        colorInd2 = random.randint(0,numColorPairs-1);
    curFaceColor = facecolorsList[colorInd2]
    curEdgeColor = edgeColorList[colorInd2]
    plt.scatter(X_n[:,0], X_n[:,1], marker='o',facecolor=curFaceColor,edgecolors=curEdgeColor,s=135,alpha=0.5)  
    ax = fig_Pid.gca()
    plt.xlabel('Dimension1')
    plt.ylabel('Dimension2')
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(labels = labels1, loc='best',fontsize='xx-large')
    ax=plt.gca();
    ax.spines['bottom'].set_linewidth(2);
    ax.spines['left'].set_linewidth(2);
    plt.tick_params(labelsize=20)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font2 = {'family': 'Times New Roman',
             'weight': 'bold',
             'size': 20,
             }
    plt.xlabel('UMAP result (dim-1)', font2)
    plt.ylabel('UMAP result (dim-2)', font2)
    plt.savefig(p_outPDFpth, dpi=600)
    plt.savefig(p_outPNG_fullPth,dpi=72)
    return ax
def f_umapProc_plotFig(p_csvFile,s_sampMthd,s_taskID):
    df_csvFile = pd.read_csv(p_csvFile)
    df_resampDf = f_resamplData(df_csvFile, s_sampMthd)
    ls_y = df_resampDf['class'].values
    X_mat = df_resampDf.drop(columns=['class']).values
    X_train, X_test, y_train, y_test = train_test_split(X_mat, ls_y, test_size=0.2, shuffle=False)
    reducer2 = UMAP(n_neighbors=100, n_components=2, n_epochs=1000,
                min_dist=0.5, local_connectivity=2, random_state=42,
                )
    X_train_res = reducer2.fit_transform(X_train, y_train)
    X_test_res = reducer2.transform(X_test)
    ls_p_outPDFpthPth = p_csvFile.split('.')
    s_suffixName = ls_p_outPDFpthPth[-2]
    ls_p_outPDFpthPth[-2] = ''.join([s_suffixName,'_umap'])
    ls_p_outPDFpthPth[-1] = 'pdf'
    s_outPDF_pth = '.'.join(ls_p_outPDFpthPth)
    globSet.set_finalTaskResults('umap-pdfFile', s_outPDF_pth)
    ls_p_outPDFpthPth[-1] = 'png'
    s_outPNG_pth = '.'.join(ls_p_outPDFpthPth)
    globSet.set_finalTaskResults('umap-pngFile', s_outPNG_pth)  
    umap_visual(X_train_res,y_train,s_outPDF_pth,s_outPNG_pth)
    globSet.set_umapTask_done()
    arr_dfData = np.vstack((y_train.T,X_train_res.T)).T
    df_UmapPlotData = pd.DataFrame(arr_dfData, columns=['class','Umap-1','Umap-2'])
    df_UmapPlotData = df_UmapPlotData.astype({'class':'int'})
    df_balancDf_frViolin = f_runResample(df_UmapPlotData,'delete')
    p_vio_pdf,p_vio_png = f_plotViolin_2d_fullViolin(df_balancDf_frViolin,s_taskID,'UMAP')
    p_vio_pdf_full = geneSmartPth('results', p_vio_pdf)
    p_vio_png_full = geneSmartPth('results', p_vio_png)
    globSet.set_finalTaskResults('umap_png_violon',p_vio_png_full)
    globSet.set_finalTaskResults('umap_pdf_violon',p_vio_pdf_full)
    globSet.set_bothTsneUmapDisp_done('umap_violin_progPloted')
