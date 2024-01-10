#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 16:32:36 2022
@author: sealight
function: 1. gene the tsne figure for the given data
"""
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import pandas as pd
import numpy as np
import argparse
import random
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from files.class_resampData import *
from files import globSet,config
from files.class_resampData import *
from files.geneSmartPth import *
from files.f_plotViolin import *
class ErrorUser(Exception):
    pass
def tsne_visual(pltdata,p_outPDFpth,p_outPNG_fullPth):
    """对t-SNE降维的数据进行可视化"""
    p1 = pltdata[(pltdata.label=="positive")]
    p2 = pltdata[(pltdata.label=="negative")]
    x1 = p1.values[:, 0]
    y1 = p1.values[:, 1]
    x2 = p2.values[:, 0]
    y2 = p2.values[:, 1]
    fig_Pid = plt.figure() 
    facecolorsList = ['#3F9475','#FC9A98','#7ED5FE','#85CDBB']
    edgeColorList = ['#2E6D56','#DB6562','#52A5D1','#43A38D']
    numColorPairs = len(facecolorsList)               
    colorInd = random.randint(0,numColorPairs-1);
    curFaceColor = facecolorsList[colorInd]
    curEdgeColor = edgeColorList[colorInd]
    labels1  = ['negative','positive']
    plt.scatter(x1, y1, marker='o',facecolor=curFaceColor,edgecolors=curEdgeColor,s=135,alpha=0.5)
    colorInd2 = random.randint(0,numColorPairs-1);
    while colorInd2==colorInd:
        colorInd2 = random.randint(0,numColorPairs-1);
    curFaceColor = facecolorsList[colorInd2]
    curEdgeColor = edgeColorList[colorInd2]
    plt.scatter(x2, y2, marker='o',facecolor=curFaceColor,edgecolors=curEdgeColor,s=135,alpha=0.5)  
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
    plt.xlabel('TSNE result (dim-1)', font2)
    plt.ylabel('TSNE result (dim-2)', font2)
    plt.savefig(p_outPDFpth, dpi=600)
    plt.savefig(p_outPNG_fullPth,dpi=72)
    return ax
def tsne_visualIntP(pltdata,p_outPNG_fullPth):
    """对t-SNE降维的数据进行可视化"""
    p1 = pltdata[(pltdata.label==True)]
    p2 = pltdata[(pltdata.label==False)]
    x1 = p1.values[:, 0]
    y1 = p1.values[:, 1]
    x2 = p2.values[:, 0]
    y2 = p2.values[:, 1]
    fig_Pid = plt.figure() 
    facecolorsList = ['#3F9475','#FC9A98','#7ED5FE','#85CDBB']
    edgeColorList = ['#2E6D56','#DB6562','#52A5D1','#43A38D']
    numColorPairs = len(facecolorsList)               
    colorInd = random.randint(0,numColorPairs-1);
    curFaceColor = facecolorsList[colorInd]
    curEdgeColor = edgeColorList[colorInd]
    labels1  = ['negative','positive']
    plt.scatter(x1, y1, marker='o',facecolor=curFaceColor,edgecolors=curEdgeColor,s=135,alpha=0.5)
    colorInd2 = random.randint(0,numColorPairs-1);
    while colorInd2==colorInd:
        colorInd2 = random.randint(0,numColorPairs-1);
    curFaceColor = facecolorsList[colorInd2]
    curEdgeColor = edgeColorList[colorInd2]
    plt.scatter(x2, y2, marker='o',facecolor=curFaceColor,edgecolors=curEdgeColor,s=135,alpha=0.5)  
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
    plt.xlabel('TSNE result (dim-1)', font2)
    plt.ylabel('TSNE result (dim-2)', font2)
    plt.savefig(p_outPNG_fullPth,dpi=300)
    plt.clf()
    plt.close()
    return ax
def f_tsneProcess(rawdata,p_outPDFpth,p_outPNG_fullPth,s_taskID):
    """对输入数据进行处理降维并返回降维结果"""
    fea_data = rawdata.drop(columns=['class']).values  
    if fea_data.shape[1]==2:
        redu_fea = fea_data
    else:
        zero_count = rawdata['class'].value_counts()[0]
        one_count = rawdata['class'].value_counts()[1]
        if zero_count < one_count:
            perpVal = zero_count
        else:
            perpVal = one_count
        if perpVal<30:
            modle = TSNE(n_components=2, random_state=0, learning_rate='auto',init='pca',perplexity=perpVal)
            redu_fea = modle.fit_transform(fea_data)
        else:
            modle = TSNE(n_components=2, random_state=0, learning_rate='auto',init='pca')
            redu_fea = modle.fit_transform(fea_data) 
    lables_set = set(rawdata['class'])
    if (0 not in lables_set) and (1 not in lables_set):
        raise ErrorUser('没有0和1存在,The labels:0/1 is the supported symbol in the csv file, please your file data')
    else:
        if (0 not in lables_set) or (1 not in lables_set):
            raise ErrorUser('只有0或者只有1...There is one type data in the file, the positive or negative file is lost!')
        else:
            labels = rawdata['class'].replace([0, 1], ['negative', 'positive']).values 
    redu_data = np.vstack((redu_fea.T, labels.T)).T 
    tsne_df = pd.DataFrame(data=redu_data, columns=['Dimension1', 'Dimension2', "label"])
    ls_p_outPDFpthPth = p_outPDFpth.split('.')
    ls_p_outPDFpthPth[-1] = 'csv'
    s_outCsvPth = '.'.join(ls_p_outPDFpthPth)
    p_outCSV_fullPth = geneSmartPth('results',s_outCsvPth)
    tsne_visual(tsne_df,p_outPDFpth,p_outPNG_fullPth)
    p_vio_pdf,p_vio_png = f_plotViolin_2d_fullViolin(tsne_df,s_taskID,'TSNE')
    p_vio_pdf_full = geneSmartPth('results', p_vio_pdf)
    p_vio_png_full = geneSmartPth('results', p_vio_png)
    globSet.set_finalTaskResults('tsne_png_violon',p_vio_png_full)
    globSet.set_finalTaskResults('tsne_pdf_violon',p_vio_pdf_full)
    return s_outCsvPth
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
def main_plot_tsne2d(infile,s_sampMthd,s_taskID):
    csvdata = pd.read_csv(infile)
    df_resampDf = f_resamplData(csvdata, s_sampMthd)
    ls_p_outPDFpthPth = infile.split('.')
    ls_p_outPDFpthPth[-1] = 'pdf'
    s_outPDF_pth = '.'.join(ls_p_outPDFpthPth)
    globSet.set_finalTaskResults('tsne-pdfFile', s_outPDF_pth)
    ls_p_outPDFpthPth[-1] = 'png'
    s_outPNG_pth = '.'.join(ls_p_outPDFpthPth)
    globSet.set_finalTaskResults('tsne-pngFile', s_outPNG_pth)
    s_outCsvPth = f_tsneProcess(df_resampDf,s_outPDF_pth,s_outPNG_pth,s_taskID)
    globSet.set_finalTaskResults('tsne-csvFile', s_outCsvPth) 
    if globSet.get_plotTaskStatus()==False:
        globSet.set_plotTaskStatus(True)
    if globSet.get_violPlot_status('tsne_violin_progPloted')==False:
        globSet.set_violPlot_status_done('tsne_violin_progPloted')