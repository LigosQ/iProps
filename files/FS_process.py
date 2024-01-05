#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:25:10 2023
@author: sealight
"""
"""
Created on Fri Dec  2 09:37:07 2022
@author: sealight
"""
import os
import math
import argparse
import pandas as pd
import numpy as np
import seaborn as sns
import prettytable as pt
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,roc_curve, auc
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.utils.multiclass import unique_labels
from files.c_clferEval import *
from files.class_resampData import *
from files.geneSmartPth import *
from files.class_mlClassifier import *
from files import globSet
class ErrorCoding(Exception):
    pass
def f_MSE(ls_realTag, ls_predTag):
    fl_mse = metrics.mean_squared_error(ls_realTag, ls_predTag)
    return fl_mse
def f_checkClassifierStr(s_classifier):
    if isinstance(s_classifier, str):
        pass
    else:
        raise ErrorCoding('Only string type is supportted! please check your input.')
    # ls_clasifier = [
    #     "Nearest Neighbors",
    #     "SVM(linear)",
    #     "RBF SVM",
    #     "Gaussian Process",
    #     "Decision Tree",
    #     "Random Forest",
    #     "Neural Net",
    #     "AdaBoost",
    #     "Naive Bayes",
    #     "QDA",
    #     "xgboost"
    # ]
    # if s_classifier in ls_clasifier:
    #     pass
    # else:
    #     ls_outInfo = ["Your given classifier is not supportted in the current version. Supportted parameters: "]
    #     ls_outInfo.extend(ls_clasifier)
    #     s_outInfo = ''.join(ls_outInfo)
    #     raise ErrorCoding(s_outInfo)
def f_checkValidResample(s_resmpleMthd):
    if isinstance(s_resmpleMthd, str):
        ls_resample = ['RandomOverSampler','SMOTE','BorderlineSMOTE','ADASYN',
                       'KMeansSMOTE','SVMSMOTE','RandomUnderSampler','NearMiss',
                       'ClusterCentroids','EasyEnsemble',
                       'SMOTEENN','SMOTETomek','add','delete','both','orig']
        ls_resampMthdUnit = [item.casefold() for item in ls_resample]
        s_resampInputUnit = s_resmpleMthd.casefold()
        if s_resampInputUnit in ls_resampMthdUnit:
            pass
        else:
            s_outInfo = ','.join(ls_resampMthdUnit)
            raise ErrorCoding('The supportted resampling method is as follows: '+s_outInfo)
    else:
        raise ErrorCoding("The resample method should be string type. please check your input...")
#
def f_checkTestRatio(f_testRatio):
    if isinstance(f_testRatio, float):
        if f_testRatio in [0.1, 0.2, 0.3]:
            pass
        else:
            raise ErrorCoding('The often-used folder number is 5 or 10. This version only support these two values')
    elif isinstance(f_testRatio, str):
        f_testRatio = float(f_testRatio)
        if f_testRatio in [0.1, 0.2, 0.3]:
            pass
        else:
            raise ErrorCoding('The often-used folder number is 5 or 10. This version only support these two values')
    else:
        raise ErrorCoding('The number of folder only support int type, please check your input type...')
def f_checkColName(s_labelColName, df_csvData):
    if isinstance(s_labelColName, str):
        ls_allColNames = df_csvData.columns.values.tolist()
        if s_labelColName in ls_allColNames:
            pass
        else:
            raise ErrorCoding('Your given columns isnot in the csv file, please check your input...')
    else:
        raise ErrorCoding("The column name should be string type, please check your input data type.")
def f_checkParasAll(df_csvData, s_classifier, s_resampleMthd, f_testRatio,s_labelColName):
    f_checkClassifierStr(s_classifier)
    f_checkValidResample(s_resampleMthd)
    f_checkTestRatio(f_testRatio)
    f_checkColName(s_labelColName, df_csvData)
def f_readCsv_adBalanceData(df_csvData,s_resampMthd, s_labelColName):
    ls_y = df_csvData[s_labelColName].values.tolist()
    mat_X = df_csvData.drop(columns=[s_labelColName])
    ls_colNames = mat_X.columns.values.tolist()
    ls_colName_class = ['class']
    ls_colName_class.extend(ls_colNames)
    obj_resampMod = c_resampData(mat_X.values, ls_y, s_resampMthd, ls_colName_class)
    d_maxAcc, arr_X_resampled, ls_y_resampled, df_resampledData = obj_resampMod.f_operResampling()
    return [arr_X_resampled, ls_y_resampled, df_resampledData]
def f_stdForEachSample(mat_featX):
    mod_std = StandardScaler()
    matFeat_stdd = mod_std.fit_transform(mat_featX.T).T
    return matFeat_stdd
def f_getUnionResampName(s_userInputName):
    ls_resample = ['RandomOverSampler','SMOTE','BorderlineSMOTE','ADASYN',
                   'KMeansSMOTE','SVMSMOTE','RandomUnderSampler','NearMiss',
                   'ClusterCentroids','EasyEnsemble',
                   'SMOTEENN','SMOTETomek','add','delete','both','orig']
    ls_resampMthdUnit = [item.casefold() for item in ls_resample]
    s_resampInputUnit = s_userInputName.casefold()
    s_unionName = ls_resample[ls_resampMthdUnit.index(s_resampInputUnit)]
    return str(s_unionName)
def f_iPcaProcess(df_csvData, s_classifier, s_resampleMthd, f_testRatio,s_labelColName):
    s_rsmpName_union = f_getUnionResampName(s_resampleMthd)
    f_checkParasAll(df_csvData, s_classifier, s_rsmpName_union, f_testRatio,s_labelColName)
    [mat_featMatrix, ls_y_label, df_rsampedData] = f_readCsv_adBalanceData(df_csvData, s_rsmpName_union, s_labelColName)
    mat_feat_stded = f_stdForEachSample(mat_featMatrix)
    random_state = 10
    X_train, X_test, y_train, y_test = train_test_split(mat_feat_stded, ls_y_label, random_state=random_state,test_size=f_testRatio)
    try:
        mod_PCA = PCA(n_components='mle')
        X_pca_d = mod_PCA.fit(X_train)
    except:
        mod_PCA = PCA(n_components=0.9)
        X_pca_d = mod_PCA.fit(X_train)
    x_train_pcaDone = mod_PCA.transform(X_train)
    x_test_pcaDone = mod_PCA.transform(X_test)
    matFeat = np.vstack([x_train_pcaDone, x_test_pcaDone])
    ls_y = y_train + y_test
    f_build_FSed_Data(matFeat, ls_y, 'PCA')
    s_4metrics_Tab = f_evalFeatSet(x_train_pcaDone, y_train, x_test_pcaDone, y_test, s_classifier, 'PCA')
    ls_pcaRatio = mod_PCA.explained_variance_ratio_
    ls_cumsumRatio = np.cumsum(ls_pcaRatio)
    plt.figure()
    plt.plot(ls_cumsumRatio)
    plt.title('The explained variance ratio')
    ax=plt.gca();#
    ax.spines['bottom'].set_linewidth(2);###设置底部坐标轴的粗细
    ax.spines['left'].set_linewidth(2);####设置左边坐标轴的粗细
    plt.tick_params(labelsize=13)
    font2 = {'family': 'Times New Roman',
             'size': 13,
             }
    plt.xlabel('Feature number', font2)
    plt.ylabel('The explained variance ratio', font2)
    s_figName_pdf = 'PCA_explainRatio.pdf'
    p_figFullPth_pdf = geneSmartPth('results', s_figName_pdf)
    s_figName_png = 'PCA_explainRatio.png'
    p_figFullPth_png = geneSmartPth('results', s_figName_png)
    plt.savefig(p_figFullPth_pdf, dpi=600)
    plt.savefig(p_figFullPth_png, dpi=72)
    globSet.set_perform_paras('Fig_PCA_explainRatio',p_figFullPth_png)
    return s_4metrics_Tab
def f_build_FSed_Data(mat_fs_std_data, ls_y, s_FsMthd):
    try:
        mat_dim_x, mat_dim_y = mat_fs_std_data.shape
    except:
        raise ErrorCoding('The given matrix has no shape attribute.')
    if mat_dim_x==len(ls_y):
        pass
    else:
        raise ErrorCoding('The dimension of row is not equal to the number of y.')
    arr_y = np.array(ls_y)
    arr_FSed_data = np.vstack((arr_y.T, mat_fs_std_data.T)).T
    ls_col_featNames = ['class']
    for i in range(mat_dim_y):
        ls_col_featNames.append(''.join([s_FsMthd, '_feat_', str(i)]))
    df_FSed_stded = pd.DataFrame(arr_FSed_data, columns=ls_col_featNames)
    s_taskID = globSet.getGlobID()
    if s_taskID is None:
        s_taskID = ''
    s_csvFileName = ''.join([s_taskID,'_bestFeat_',s_FsMthd,'.csv'])
    p_FSed_csvFile = geneSmartPth('results', s_csvFileName)
    df_FSed_stded.to_csv(p_FSed_csvFile, index=False) 
def f_iLDA_process(df_csvData, s_classifier, s_resampleMthd, f_testRatio,s_labelColName):
    s_rsmpName_union = f_getUnionResampName(s_resampleMthd)
    f_checkParasAll(df_csvData, s_classifier, s_rsmpName_union, f_testRatio,s_labelColName)
    [mat_featMatrix, ls_y_label, df_rsampedData] = f_readCsv_adBalanceData(df_csvData, s_rsmpName_union, s_labelColName)
    mat_feat_stded = f_stdForEachSample(mat_featMatrix)
    random_state = 10
    X_train, X_test, y_train, y_test = train_test_split(mat_feat_stded, ls_y_label, random_state=random_state,test_size=f_testRatio)
    mod_LDA = LinearDiscriminantAnalysis()
    # mod_LDA = LinearDiscriminantAnalysis(n_components=f_getFeatDimNum(df_csvData))
    mod_LDA.fit(X_train, y_train)
    x_train_LdaDone = mod_LDA.transform(X_train)
    x_test_LdaDone = mod_LDA.transform(X_test)
    s_4metrics_Tab = f_evalFeatSet(x_train_LdaDone, y_train, x_test_LdaDone, y_test, s_classifier,'LDA')
    return s_4metrics_Tab
def f_clacSn_4matrics(ls_confusMat_4elms):
    tp, fp, fn, tn = ls_confusMat_4elms[0], ls_confusMat_4elms[1], ls_confusMat_4elms[2], ls_confusMat_4elms[3]
    if (tp+fn)==0:
        sn = 0
    else:
        sn = tp/(tp+fn)
    if (tn+fp)==0:
        sp = 0
    else:
        sp = tn/(tn+fp)    
    acc = (tp+tn)/(tp+fp+fn+tn)
    if ((tp+fn)*(tn+fn)*(tp+fp)*(tn+fp))==0:
        mcc = 0
    else:
        mcc = (tp*tn-fp*fn)/math.sqrt((tp+fn)*(tn+fn)*(tp+fp)*(tn+fp))
    d_4metrics = dict()
    d_4metrics['SN'] = round(sn,4)
    d_4metrics['SP'] = round(sp,4)
    d_4metrics['ACC'] = round(acc,4)
    d_4metrics['MCC'] = round(mcc,4)
    return d_4metrics
#
def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=sns.light_palette("seagreen", as_cmap=True)):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.#cmap=sns.light_palette("seagreen", as_cmap=True)
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'
    cm = confusion_matrix(y_true, y_pred)
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    else:
        pass
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')
    ax.set_ylim(len(classes)-0.5, -0.5)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax
#
def f_plotMatrix(y_test, y_predict,s_clfier,s_FS_lab, s_globID):
    class_names = np.array(["0","1"])
    plot_confusion_matrix(y_test, y_predict, classes=class_names, normalize=False)
    s_clf_noDelim = ''.join(s_clfier.split(' '))
    s_figName_pdf = ''.join([s_globID,'_FS_',s_FS_lab,'_confMatrix_',s_clf_noDelim,'.pdf'])
    p_figFullPth_pdf = geneSmartPth('results', s_figName_pdf)
    s_figName_png = ''.join([s_globID,'_FS_',s_FS_lab,'_confMatrix_',s_clf_noDelim,'.png'])
    p_figFullPth_png = geneSmartPth('results', s_figName_png)
    plt.savefig(p_figFullPth_pdf, dpi=600)
    plt.savefig(p_figFullPth_png, dpi=72)
    s_keyName = ''.join(['fig_conMat_',s_FS_lab])
    globSet.set_perform_paras(s_keyName,p_figFullPth_png)
def f_plotROC(y_test, y_score,s_clfier,s_FS_lab):
    fpr,tpr,threshold = roc_curve(y_test, y_score) ###计算真正率和假正率
    roc_auc = auc(fpr,tpr) ###计算auc的值
    ##画布
    lw = 2
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    ax=plt.gca();#
    ax.spines['bottom'].set_linewidth(2);#
    ax.spines['left'].set_linewidth(2);#
    plt.tick_params(labelsize=13)
    font2 = {'family': 'Times New Roman',
             'size': 13,
             }
    plt.xlabel('False Positive Rate', font2)
    plt.ylabel('True Positive Rate', font2)
    plt.title('Receiver operating characteristic', font2)
    plt.legend(loc="lower right")
    #####**********************************************
    s_clf_noDelim = ''.join(s_clfier.split(' '))
    s_figName_pdf = ''.join(['FS_',s_FS_lab,'_ROC_',s_clf_noDelim,'.pdf'])
    p_figFullPth_pdf = geneSmartPth('results', s_figName_pdf)
    s_figName_png = ''.join(['FS_',s_FS_lab,'_ROC_',s_clf_noDelim,'.png'])
    p_figFullPth_png = geneSmartPth('results', s_figName_png)
def f_plot4matrics(d_4metrics,s_classifier, s_FS_lab,s_globID):
    sn = d_4metrics['SN']
    sp = d_4metrics['SP']
    acc = d_4metrics['ACC']
    mcc = d_4metrics['MCC']
    ls_color = ['#AEC7E8','#FFB878','#98DF8A','#FF9896']
    fig,ax = plt.subplots()
    ax.bar(['SN','SP','ACC','MCC'], [sn,sp,acc,mcc],color=ls_color) 
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False) 
    ax.xaxis.set_ticks_position('none') 
    ax.yaxis.set_ticks_position('none') 
    ax.xaxis.set_tick_params(pad=5) 
    ax.yaxis.set_tick_params(pad=10) 
    ax.grid(visible= True, color='#4F9BFA', 
            linestyle='-.', linewidth=0.5, 
            alpha=0.4) 
    for i in ax.patches:
        plt.text(i.get_x()+(i.get_width()/2)-0.15,i.get_height()+0.05, 
                 str(round((i.get_height()), 3)), 
                 fontsize=13, fontweight='light', 
                 )
    font2 = {'family': 'Times New Roman',
             'size': 13,
             }
    plt.xlabel("Performance indicators",font2) 
    plt.ylabel("Value",font2)
    s_clf_noDelim = ''.join(s_classifier.split(' '))
    s_figName_pdf = ''.join([s_globID,'_FS_',s_FS_lab,'_4metrics_',s_clf_noDelim,'.pdf'])
    p_figFullPth_pdf = geneSmartPth('results', s_figName_pdf)
    s_figName_png = ''.join([s_globID,'_FS_',s_FS_lab,'_4metrics_',s_clf_noDelim,'.png'])
    p_figFullPth_png = geneSmartPth('results', s_figName_png)
    plt.savefig(p_figFullPth_pdf, dpi=600)
    plt.savefig(p_figFullPth_png, dpi=72)
    globSet.set_perform_paras(''.join(['fig_bar_',s_FS_lab]), p_figFullPth_png)
def f_ROC_multiClfier(x_train, y_train, x_test, y_test,s_FS_lab, s_globID):
    tb = pt.PrettyTable()
    tb.field_names = ["Classifier", "Sn", "Sp", "ACC",'MCC']
    ls_clfNames = [
        "lightGBM",
        "xgboost",
        "ExtraTreesClassifier",
        "Nearest Neighbors",
        "SVM(linear)",
        "SVM(RBF)",
        "Gaussian Process",
        "Decision Tree",
        "Random Forest",
        "Neural Net",
        "AdaBoost",
        "Naive Bayes",
        "QDA"
    ]
    ls_color = ['#E64B35','#4DBBD5','#00A087','#3C5488','#F39B7F',
                '#8491B4','#91D1C2','#7E6148','#AD002A','#EFC000','#0073C2',
                "#000000","#A44CAD"]
    linestyle_tuple = [
         ('solid', 'solid'),      # Same as (0, ()) or '-'
         ('dotted', 'dotted'),    # Same as (0, (1, 1)) or '.'
         ('dashed', 'dashed'),    # Same as '--'
         ('dashdot', 'dashdot'),  # Same as '-.'
         ('loosely dotted',        (0, (7, 3))),
         ('dotted',                (0, (5, 2))),
         ('densely dotted',        (0, (8, 4))),
         ('loosely dashed',        (0, (5, 1))),
         ('dashed',                (0, (5, 5))),
         ('densely dashed',        (0, (6, 1))),
         ('loosely dashdotted',    (0, (13, 2))),
         ('dashdotted',            (0, (13, 1))),
         ('loosely dashdotdotted', (0, (13, 2)))]
    ls_maker = ['.','o',8,'*','+','x']
    lw = 2
    fig = plt.figure()
    d_multClf_perf = []
    for i, s_clfierName in enumerate(ls_clfNames):
        y_predict, score, ls_probab, d_4metrics = f_calcPermCalc(x_train, y_train, x_test, y_test, s_clfierName)
        fpr,tpr,threshold = roc_curve(y_test, ls_probab[:,1]) ###计算真正率和假正率
        roc_auc = auc(fpr,tpr) ###计算auc的值
        plt.plot(fpr, tpr, color=ls_color[i],
                  lw=lw, label='%s (area = %0.2f)' % (s_clfierName, roc_auc),
                  marker=ls_maker[np.mod(i,6)],
                  linestyle=linestyle_tuple[i][1]) ###假正率为横坐标，真正率为纵坐标做曲线
        ####______----________
        tb.add_row([s_clfierName,d_4metrics['SN'], d_4metrics['SP'],d_4metrics['ACC'],d_4metrics['MCC']])
    s_4metrics_disp = tb.get_string()
    s_keyName = ''.join(['multiClifer_comp_',s_FS_lab])
    globSet.set_perform_paras(s_keyName, s_4metrics_disp)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    ax=plt.gca();
    ax.spines['bottom'].set_linewidth(2);
    ax.spines['left'].set_linewidth(2);#
    plt.tick_params(labelsize=13)
    font2 = {'family': 'Times New Roman',
             'size': 13,
             }
    plt.xlabel('False Positive Rate', font2)
    plt.ylabel('True Positive Rate', font2)
    plt.title('Receiver operating characteristic example', font2)
    plt.legend(loc="lower right")
    #####**********************************************
    s_figName_pdf = ''.join([s_globID,'_ROC_final_',s_FS_lab,'_multiClf.pdf'])
    p_figFullPth_pdf = geneSmartPth('results', s_figName_pdf)
    s_figName_png = ''.join([s_globID,'_ROC_final_',s_FS_lab,'_multiClf.png'])
    p_figFullPth_png = geneSmartPth('results', s_figName_png)
    plt.savefig(p_figFullPth_pdf, dpi=600)
    plt.savefig(p_figFullPth_png, dpi=72)
    globSet.set_perform_paras(''.join(['fig_ROC9_',s_FS_lab]), p_figFullPth_png)
    return s_4metrics_disp
def f_smoothData(ls_data,i_winSize):
    window = np.ones(int(i_winSize)) / float(i_winSize)
    if isinstance(ls_data,list):
        re = np.convolve(np.array(ls_data), window, mode='same')
    elif isinstance(ls_data, np.ndarray):
        re = np.convolve(ls_data, window, mode='same')
    else:
        raise ErrorCoding('The data type is wrong...')
    return re  
def f_calcPermCalc(x_train, y_train, x_test, y_test, s_classifier):
    y_predict, score, ls_probab, m_confMatrix = f_evalData_ByClfier(x_train, y_train, x_test, y_test, s_classifier)
    ls_confusMat_allElems = []
    ls_confusMat_expanded = m_confMatrix.tolist()
    for i in range(len(ls_confusMat_expanded)):
        ls_curElem = ls_confusMat_expanded[i]
        for j in range(len(ls_curElem)):
            i_curElem = ls_curElem[j]
            ls_confusMat_allElems.append(i_curElem)
    d_4metrics = f_clacSn_4matrics(ls_confusMat_allElems)
    return y_predict, score, ls_probab, d_4metrics
def f_evalFeatSet(x_train, y_train, x_test, y_test, s_classifier, s_FS_lab):
    y_predict, score, ls_probab, d_4metrics = f_calcPermCalc(x_train, y_train, x_test, y_test, s_classifier)
    s_globID = globSet.getGlobID()
    f_plotMatrix(list(map(int, y_test)), list(map(int,y_predict)),s_classifier,s_FS_lab,s_globID)
    f_plot4matrics(d_4metrics,s_classifier, s_FS_lab,s_globID)
    s_4metrics_Tab = f_ROC_multiClfier(x_train, y_train, x_test, y_test,s_FS_lab,s_globID)
    return s_4metrics_Tab
def main():
    parser = argparse.ArgumentParser(description="Dimension reduction basing on the PCA method")
    parser.add_argument('-i', '--infile', help=["The input file should be saved in the csv format,",
                        "other file types are not supported at present"], required=True)
    parser.add_argument('-c', '--clafier', help=["The classifier used in the method. Example: rf, svm, ..."], required=True)
    parser.add_argument('-f', '--foldNum', help='The number of Cross-validated folds', required=True)
    parser.add_argument('-r', '--resample', help='The name of the resampling mthod', required=True)
    parser.add_argument('-l', '--label', help='The column name of the sample category')
    args = parser.parse_args()