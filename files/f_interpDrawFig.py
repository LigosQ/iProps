#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 08:55:55 2023
@author: sealight
"""
import pandas as pd
import numpy as np
import xgboost
import shap,sys
try:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
    from class_mlClassifier import c_mlClassifier
    from buildReport import f_compHtmlFile
except:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT
    from files.class_mlClassifier import c_mlClassifier
    from files.buildReport import f_compHtmlFile
import os,time,random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
from sklearn.preprocessing import StandardScaler
class ErrorCoding(Exception):
    pass
def f_normCsvData(df_data):
    s_classRowRealName = ''
    ls_origFullCols = df_data.columns.values.tolist()
    for s_1colName in ls_origFullCols:
        if s_1colName.lower() == 'class':
            s_classRowRealName = s_1colName
            break
        elif s_1colName.lower() == 'type':
            s_classRowRealName = s_1colName
            break
    if s_classRowRealName == '':
        raise ErrorCoding('The default category column, whose name is class or type, cannot be found. Please check your files...')
    else:
        pass
    ser_classData_Y = df_data[s_classRowRealName]
    df_noTypeCol = df_data.drop(columns=[s_classRowRealName])
    scaler = StandardScaler()
    ser_classData_X = scaler.fit_transform(df_noTypeCol.T).T
    df_X = pd.DataFrame(ser_classData_X,columns=df_noTypeCol.columns)
    return df_X,ser_classData_Y
def f_getTopFeat_N(ls_meanShapVal, ls_featNames, i_topFeatNum):
    arr_shapVal = np.array(ls_meanShapVal)
    df_shapVal = pd.DataFrame(arr_shapVal,columns=['ImportVals'])
    ls_pureFeatNames = [s_name for i,s_name in enumerate(ls_featNames) if not(s_name=='class')]
    df_featNames = pd.DataFrame(np.array(ls_pureFeatNames),columns=['featNames'])
    df_shapAdFeatNames = pd.concat([df_featNames,df_shapVal],axis=1)
    df_sorted = df_shapAdFeatNames.sort_values(by='ImportVals', ascending=False)
    if i_topFeatNum<=len(ls_featNames):
        ls_topFeatNames = df_sorted.iloc[0:i_topFeatNum]['featNames']
    else:
        ls_topFeatNames = df_sorted['featNames']
    return ls_topFeatNames
def f_y_bin2_01(arr_y):
    ls_transdY = []
    for i,val in enumerate(arr_y):
        if val:
            ls_transdY.append(1)
        else:
            ls_transdY.append(1)
    arr_01_y = np.array(ls_transdY)
    return arr_01_y
def interpByYbrick(X_train, y_train,X_test, y_test,X_topFeats,ls_2ProTypeNames,
                   f_testRatio,m_clfer,d_allVisFigInfo,p_folder,i_allSampNum_rsmped):
    X,y = X_train,y_train
    from yellowbrick.features import RadViz
    visualizer = RadViz(classes=ls_2ProTypeNames,alpha=0.3,show=False)
    visualizer.fit(X_topFeats, y)           
    visualizer.transform(X_topFeats)        
    p_figName = os.path.join(p_folder, 'fig1.jpg') 
    p_figName_p = os.path.join(p_folder, 'fig1.pdf') 
    d_allVisFigInfo['fig1']['src'] = p_figName
    plt.legend()
    plt.savefig(p_figName,dpi=300,bbox_inches="tight")
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    s_outInfo = ''.join(['='*40, '\n Start explaining machine learning models: \n\n',
                         'Figure 1 has been plotted.'])
    print(s_outInfo)
    from yellowbrick.features import Rank1D
    visualizer = Rank1D(algorithm='shapiro')
    visualizer.fit(X_topFeats, y)           
    visualizer.transform(X_topFeats)        
    p_figName = os.path.join(p_folder, 'fig2.jpg')
    p_figName_p = os.path.join(p_folder, 'fig2.pdf') 
    d_allVisFigInfo['fig2']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 2 has been plotted.')
    from yellowbrick.features import Rank2D
    visualizer = Rank2D(algorithm='pearson')
    visualizer.fit_transform(X_topFeats, y)
    p_figName = os.path.join(p_folder, 'fig3.jpg') 
    p_figName_p = os.path.join(p_folder, 'fig3.pdf') 
    d_allVisFigInfo['fig3']['src'] = p_figName
    plt.savefig(p_figName,dpi=300,bbox_inches="tight")
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 3 has been plotted.')
    from yellowbrick.features import ParallelCoordinates
    visualizer = ParallelCoordinates(
        classes=ls_2ProTypeNames, features=X_topFeats.columns.values, sample=f_testRatio, shuffle=True
    )
    visualizer.fit_transform(X_topFeats, y)
    p_figName = os.path.join(p_folder, 'fig4.jpg')
    p_figName_p = os.path.join(p_folder, 'fig4.pdf') 
    d_allVisFigInfo['fig4']['src'] = p_figName
    plt.savefig(p_figName,dpi=300,bbox_inches="tight")
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 4 has been plotted.')
    from yellowbrick.features import PCA
    visualizer = PCA(scale=True, classes=ls_2ProTypeNames)
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    le.fit(y)
    Y_encd = le.transform(y)
    visualizer.fit_transform(X, Y_encd)
    p_figName = os.path.join(p_folder, 'fig5.jpg') 
    p_figName_p = os.path.join(p_folder, 'fig5.pdf') 
    d_allVisFigInfo['fig5']['src'] = p_figName
    plt.legend()
    plt.savefig(p_figName,dpi=300,bbox_inches="tight")
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 5 has been plotted.')
    from yellowbrick.features.manifold import manifold_embedding
    ls_visAlgor = ["lle","ltsa","hessian","modified","isomap","mds","spectral","tsne"]
    i_mthdIndex = 4
    i_halfSampNum = int(i_allSampNum_rsmped/2)
    if i_halfSampNum<30:
        i_perplexity = i_halfSampNum
    else:
        i_perplexity = 30
    manifold_embedding(X, Y_encd, manifold=ls_visAlgor[i_mthdIndex], n_neighbors=10,
                       show=False, perplexity=i_perplexity)
    p_figName = os.path.join(p_folder, 'fig6.jpg')
    p_figName_p = os.path.join(p_folder, 'fig6.pdf') 
    d_allVisFigInfo['fig6']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 6 has been plotted.')
    from sklearn.manifold import TSNE
    X_embedded = TSNE(n_components=2, learning_rate='auto',
                      init='random', perplexity=(i_perplexity)).fit_transform(X)
    redu_data = np.vstack((X_embedded.T, y.T)).T 
    tsne_df = pd.DataFrame(data=redu_data, columns=['Dimension1', 'Dimension2', "label"])
    try:
        from files.f_tsne_in import tsne_visualIntP
    except:
        from f_tsne_in import tsne_visualIntP
    p_figName = os.path.join(p_folder, 'fig7.jpg') 
    p_figName_p = os.path.join(p_folder, 'fig7.pdf') 
    d_allVisFigInfo['fig7']['src'] = p_figName
    tsne_visualIntP(tsne_df,p_figName)
    tsne_visualIntP(tsne_df,p_figName_p)
    print('Figure 7 has been plotted.')
    from yellowbrick.classifier import ClassificationReport
    viz = ClassificationReport(m_clfer, classes=ls_2ProTypeNames, support=True)
    viz.fit(X_train, y_train)
    viz.score(X_test, y_test)
    p_figName = os.path.join(p_folder, 'fig8.jpg')
    p_figName_p = os.path.join(p_folder, 'fig8.pdf') 
    d_allVisFigInfo['fig8']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 8 has been plotted.')
    from yellowbrick.classifier import ConfusionMatrix
    model = m_clfer
    iris_cm = ConfusionMatrix(
        model, classes=ls_2ProTypeNames,
        label_encoder={0: ls_2ProTypeNames[0], 1: ls_2ProTypeNames[1]}
    )
    iris_cm.fit(X_train, y_train)
    iris_cm.score(X_test, y_test)
    p_figName = os.path.join(p_folder, 'fig9.jpg')
    p_figName_p = os.path.join(p_folder, 'fig9.pdf') 
    d_allVisFigInfo['fig9']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 9 has been plotted.')
    from yellowbrick.classifier import ROCAUC
    visualizer = ROCAUC(model, classes=ls_2ProTypeNames,binary=True)
    visualizer.fit(X_train, y_train)        
    visualizer.score(X_test, y_test)        
    p_figName = os.path.join(p_folder, 'fig10.jpg')
    p_figName_p = os.path.join(p_folder, 'fig10.pdf') 
    d_allVisFigInfo['fig10']['src'] = p_figName
    plt.legend()
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 10 has been plotted.')
    from yellowbrick.classifier import PrecisionRecallCurve
    viz = PrecisionRecallCurve(m_clfer)
    viz.fit(X_train, y_train)
    viz.score(X_test, y_test)
    p_figName = os.path.join(p_folder, 'fig11.jpg')
    p_figName_p = os.path.join(p_folder, 'fig11.pdf') 
    d_allVisFigInfo['fig11']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 11 has been plotted.')
    from yellowbrick.classifier import ClassPredictionError
    visualizer = ClassPredictionError(
        m_clfer, classes=ls_2ProTypeNames
    )
    visualizer.fit(X_train, y_train)
    visualizer.score(X_test, y_test)
    p_figName = os.path.join(p_folder, 'fig12.jpg')
    p_figName_p = os.path.join(p_folder, 'fig12.pdf') 
    d_allVisFigInfo['fig12']['src'] = p_figName
    plt.legend()
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 12 has been plotted.')
    from yellowbrick.classifier import DiscriminationThreshold
    visualizer = DiscriminationThreshold(model)
    visualizer.fit(X, y)        
    p_figName = os.path.join(p_folder, 'fig13.jpg')
    p_figName_p = os.path.join(p_folder, 'fig13.pdf') 
    d_allVisFigInfo['fig13']['src'] = p_figName
    plt.legend()
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 13 has been plotted.')
    return d_allVisFigInfo
def mainPlotFun(df_train_X, df_test_X, arr_train_y, arr_test_y, df_X_resampd,arr_y_resampd,
                df_resampledData, f_testRatio,s_clf,ls_2ProTypeNames, 
                i_showSampIdx, i_topFeatNum, d_allVisFigInfo,s_timeStamp,
                i_allSampNum_rsmped):
    s_fulltime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    i_folderNo = 1
    s_figDirName = ''.join(['test',str(i_folderNo)])
    p_folder = f_geneAbsPath_frmROOT('interpReport',''.join(['test',str(i_folderNo)]))
    while os.path.isdir(p_folder):
        i_folderNo += 1
        s_figDirName = ''.join(['test',str(i_folderNo)])
        p_folder = f_geneAbsPath_frmROOT('interpReport',s_figDirName)
    os.makedirs(p_folder)
    if s_clf=='xgboost':
        from xgboost.sklearn import XGBClassifier
        m_clfer = XGBClassifier(max_depth=5)
    elif s_clf=='lightGBM':
        from lightgbm.sklearn import LGBMClassifier
        m_clfer = LGBMClassifier()
    else:
        c_clfer = c_mlClassifier(s_clf)
        m_clfer = c_clfer.f_geneMlClassifier(None)
    model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(df_X_resampd, label=arr_y_resampd), 100)
    explainer = shap.TreeExplainer(model)
    shap_values0 = explainer.shap_values(df_X_resampd)
    shap_values2 = explainer(df_X_resampd)
    ls_meanShapVal = []
    i_sampNum = len(shap_values0)
    for i_feat_col_i in range(len(shap_values0[0])):
        ls_col_i = [shap_values0[i_sampIdx][i_feat_col_i] for i_sampIdx in range(i_sampNum)]
        f_meanShap = np.mean(ls_col_i)
        ls_meanShapVal.append(f_meanShap)
    ls_featNames = df_X_resampd.columns.values.tolist()
    ls_topFeatNames = f_getTopFeat_N(ls_meanShapVal, ls_featNames, i_topFeatNum)
    X_topFeats = df_train_X[ls_topFeatNames]
    d_allVisFigInfo = interpByYbrick(df_train_X, arr_train_y,df_test_X, arr_test_y,X_topFeats,
                    ls_2ProTypeNames,f_testRatio,m_clfer,d_allVisFigInfo,p_folder,i_allSampNum_rsmped)
    p_figName = os.path.join(p_folder, 'fig14.jpg')
    p_figName_p = os.path.join(p_folder, 'fig14.pdf') 
    shap.plots.bar(shap_values2,show=False)
    d_allVisFigInfo['fig14']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 14 has been plotted.')
    i_topFeatNum = 15
    shap.plots.bar(shap_values2[i_showSampIdx],max_display=i_topFeatNum,show=False)
    p_figName = os.path.join(p_folder, 'fig15.jpg')
    p_figName_p = os.path.join(p_folder, 'fig15.pdf') 
    d_allVisFigInfo['fig15']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 15 has been plotted.')
    if df_X_resampd.shape[1]<=100:
        clustering = shap.utils.hclust(df_X_resampd,arr_y_resampd)
        shap.plots.bar(shap_values2, clustering=clustering, clustering_cutoff=0.5,show=False)
        plt.clf()
        plt.close()
    shap.summary_plot(shap_values0,df_X_resampd,show=False)
    p_figName = os.path.join(p_folder, 'fig16.jpg')
    p_figName_p = os.path.join(p_folder, 'fig16.pdf') 
    d_allVisFigInfo['fig16']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 16 has been plotted.')
    ind_mean = shap_values2.abs.mean(0).argsort[-1]
    shap.plots.scatter(shap_values2[:, ind_mean],show=False)
    p_figName = os.path.join(p_folder, 'fig17.jpg')
    p_figName_p = os.path.join(p_folder, 'fig17.pdf') 
    d_allVisFigInfo['fig17']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 17 has been plotted.')
    shap.force_plot(explainer.expected_value,shap_values0[i_showSampIdx],
                    df_X_resampd.iloc[i_showSampIdx],
                    show=False,matplotlib=True)
    p_figName = os.path.join(p_folder, 'fig18.jpg')
    p_figName_p = os.path.join(p_folder, 'fig18.pdf') 
    d_allVisFigInfo['fig18']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 18 has been plotted.')
    if df_X_resampd.shape[1]<=100:
        shap_interaction_values = explainer.shap_interaction_values(df_X_resampd)
        shap.summary_plot(shap_interaction_values, df_X_resampd,show=False)
        plt.clf()
        plt.close()
    shap.plots.heatmap(shap_values2,show=False)
    p_figName = os.path.join(p_folder, 'fig19.jpg')
    p_figName_p = os.path.join(p_folder, 'fig19.pdf') 
    d_allVisFigInfo['fig19']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 19 has been plotted.')
    i_numOf_0 =0
    i_numOf_1 = 0
    ls_usedRowNo = []
    while i_numOf_0<=15 or i_numOf_1<=15:
        i_index = random.randint(0, len(arr_y_resampd)-1)
        if arr_y_resampd[i_index]:
            i_numOf_1 += 1
            if i_numOf_1<=15:
                ls_usedRowNo.append(i_index)
        else:
            i_numOf_0 += 1 
            if i_numOf_0<=15:
                ls_usedRowNo.append(i_index)
    df_vis_all = df_X_resampd.iloc[ls_usedRowNo]
    features_display = df_X_resampd.loc[df_vis_all.index]
    expected_value = explainer.expected_value
    df_vis_1instan = df_X_resampd.iloc[[i_showSampIdx]]
    shap_value_1inst = explainer.shap_values(df_vis_1instan)[0]
    shap.decision_plot(expected_value, shap_value_1inst, 
                        df_X_resampd,show=False)
    p_figName = os.path.join(p_folder, 'fig20.jpg')
    p_figName_p = os.path.join(p_folder, 'fig20.pdf') 
    d_allVisFigInfo['fig20']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 20 has been plotted.')
    shap_values20 = explainer.shap_values(df_vis_all)
    shap.decision_plot(expected_value, shap_values20, 
                        features_display,
                        link='logit',show=False)
    p_figName = os.path.join(p_folder, 'fig21.jpg')
    p_figName_p = os.path.join(p_folder, 'fig21.pdf') 
    d_allVisFigInfo['fig21']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 21 has been plotted.')
    shap.plots.waterfall(shap_values2[i_showSampIdx],show=False)
    p_figName = os.path.join(p_folder, 'fig22.jpg')
    p_figName_p = os.path.join(p_folder, 'fig22.pdf') 
    d_allVisFigInfo['fig22']['src'] = p_figName
    plt.savefig(p_figName,dpi=300)
    plt.savefig(p_figName_p)
    plt.clf()
    plt.close()
    print('Figure 22 has been plotted.')
    import sweetviz as sv
    i_svUsedTopFeatNum = 20
    arr_topFeatNames = f_getTopFeat_N(ls_meanShapVal, ls_featNames, i_svUsedTopFeatNum)
    ls_topFeatNames = arr_topFeatNames.values.tolist()
    ls_topFeatNames.append('class')
    df_visUsed = df_resampledData[ls_topFeatNames]
    myreport = sv.analyze(df_visUsed)
    p_htmlPth = os.path.join(p_folder, 'report23.html') 
    d_allVisFigInfo['fig23']['src'] = p_htmlPth
    myreport.show_html(p_htmlPth,open_browser=False,layout='widescreen', scale=None)
    p_htmlnew = f_compHtmlFile(d_allVisFigInfo,s_figDirName, s_fulltime,s_timeStamp)
    print('Figure 23 has been plotted.\n\n You can view the model interpretation report for this task in your browser.')
    return p_htmlnew
