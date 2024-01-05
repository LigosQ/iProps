#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 16:51:13 2020
@author: tafch
"""
"""
Created on Thu Nov 26 08:46:17 2020
@author: tafch
"""
"""
Created on Fri Oct 23 15:59:46 2020
@author: tafch
"""
"""
Created on Wed Oct 14 15:05:38 2020
@author: tafch
"""
import pandas as pd
import numpy as np
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SVMSMOTE
from imblearn.combine import SMOTEENN
import argparse
from fun_dfData2Csv import *
class ErrorUser(Exception):
    pass
def countNumOfTypes(ylist):
    numof_0 = 0
    numof_1 = 0
    for i in range(len(ylist)):
        if ylist[i]==0:
            numof_0 += 1
        else:
            numof_1 += 1
    return numof_0,numof_1
def calMinnumOfTypes(y,resamStrategy):
    setOfY = list(set(y))
    if (resamStrategy=='add'):
        pass
    elif (resamStrategy=='delete'):
        pass
    elif (resamStrategy=='both'):
        pass
    elif resamStrategy=='orig':
        pass
    else:
        raise ErrorUser('The resample strategy string should be "add"/"delete" in current version....')
    if len(setOfY)==2:
        if (0 in setOfY) and (1 in setOfY):
            numof_0, numof_1 = countNumOfTypes(y)
            imblanRatio_01 = numof_0/numof_1
            if imblanRatio_01 > 5:
                pass
            if resamStrategy=='add':
                return True, numof_0, 'positive'
            if resamStrategy=='delete':
                return True, numof_1, 'negative'
            if resamStrategy=='both':
                if imblanRatio_01 > 1:
                    return True, numof_1, 'both'
                else:
                    return True, numof_0, 'both'
            if resamStrategy=='orig':
                return False,0,'orig'
def funRunResampling(isNeedResamp, finalResampNum, resampClass, resamTypeStr, featmat, y):
    if isNeedResamp==True:
        if resamTypeStr=='add':
            if resampClass=='positive':
                addResamper = SVMSMOTE(random_state=42)    
            if resampClass=='negative':
                addResamper = SVMSMOTE(random_state=42) 
            x_rsamp, y_rsamp = addResamper.fit_resample(featmat, y)
        if resamTypeStr=='delete':
            if resampClass=='positive':
                delResamper = NearMiss()
            if resampClass=='negative':
                delResamper = NearMiss()
            x_rsamp, y_rsamp = delResamper.fit_resample(featmat,y)
        if resamTypeStr=='both':
            combResamper = SMOTEENN(random_state=0)
            x_rsamp, y_rsamp = combResamper.fit_resample(featmat, y)
        if resamTypeStr=='orig':
            x_rsamp = featmat
            y_rsamp = y
    else:
        x_rsamp = featmat
        y_rsamp = y
        if resamTypeStr=='orig':
            x_rsamp = featmat
            y_rsamp = y
    return x_rsamp,y_rsamp
def main(csvfilepth,resamTypeStr):
    pthSplitList = csvfilepth.split('.')
    if not pthSplitList[-1]=='csv':
        raise ErrorUser('the input pth should be csv format, please check')
    lenSplitList = len(pthSplitList)
    if lenSplitList==2:
        pthSplitList[0] = pthSplitList[0] + '_resamp_'+resamTypeStr
        outcsvFile = '.'.join(pthSplitList)
    elif lenSplitList>2:
        pthSplitList[-2] = pthSplitList[-2] + '_resamp_'+resamTypeStr
        outcsvFile = '.'.join(pthSplitList)
    else:
        raise ErrorUser('The given csv file is incorrect, ...')
    dfData = pd.read_csv(csvfilepth)
    columnsDf = dfData.columns.values.tolist()
    colNameNew = ['class']
    colNameTemp = [columnsDf[i] for i in range(len(columnsDf)) if i!=0]
    colNameNew.append(colNameTemp)
    dfX = dfData.drop(columns=['class'])
    array_x = dfX.values
    y = dfData['class'].values.tolist()
    isNeedRsamle,finalRsmtNum, resampClass = calMinnumOfTypes(y,resamTypeStr)
    x_rsmt,y_rsmt = funRunResampling(isNeedRsamle, finalRsmtNum, resampClass, resamTypeStr, array_x, y)
    if isinstance(y_rsmt,list):
        y_rsmt = np.array(y_rsmt)
    if columnsDf[0]=='class':
        matFull = np.vstack((y_rsmt.T, x_rsmt.T)).T
    else:
        matFull = np.vstack((x_rsmt.T, y_rsmt.T)).T
    dfMatFull = pd.DataFrame(data=matFull, columns=columnsDf)
    writeDf2csv(dfMatFull,outcsvFile)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Balace the positive and negative samples by smote and nearestmiss strategy")
    parser.add_argument('-i', '--infile', help="The input file should be csv format, other file types are not supported at present", required=True)
    parser.add_argument('-t', '--resamMethd', help="The used resampling method, value:a/d...[a:add/smote, d:delete/knear]", required=True)  
    args = parser.parse_args()
    main(args.infile, args.resamMethd)