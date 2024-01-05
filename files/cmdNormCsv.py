#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 16:25:50 2019
@author: admin
"""
import numpy as np
import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler
from cmdcsv2arff import *
from fun_dfData2Csv import *
class ErrorUser(Exception):
    pass
def checkFormatIsCorrect(pth, fileformat):
    if isinstance(pth,str):
        infStrList = pth.split('.')
        if infStrList[-1]==fileformat:
            if fileformat=='csv':
                csvNamList = pth.split('/')
                lenthCsvList = len(csvNamList)
                csvName = csvNamList[-1]
                csvNameList = csvName.split('.')
                newArfName = csvNameList[0]+'_normd.arff'
                newCsvName = csvNameList[0]+'_normd.csv'
                newArfNameList = []
                newCsvNameList = []
                for i in range(lenthCsvList):
                    if i==(lenthCsvList-1):
                        newArfNameList.append(newArfName)
                        newCsvNameList.append(newCsvName)
                    else:
                        newArfNameList.append(csvNamList[i])
                        newCsvNameList.append(csvNamList[i])
                outArfPth = '/'.join(newArfNameList)
                outCsvPth = '/'.join(newCsvNameList)
            return outCsvPth,outArfPth,True
        else:
            raise ErrorUser('The parameter in fun_comFiles() is not the path of %s file.Please check...'%(fileformat))
    elif isinstance(pth,list):
        for i in range(len(pth)):
            curFormat = pth[i].split('.')
            if curFormat[-1]!=fileformat:
                raise ErrorUser('The parameter in fun_comFiles() is not the path of %s file.Please check...'%(fileformat))
        return True
    else:
        raise ErrorUser('Your input is not correct')
def subfunNormCsvAdArff(incsvFile):
    try:
        outCsvPth,outArfPth,isFormatRight = checkFormatIsCorrect(incsvFile,'csv')
    except Exception as e:
        print (e)
    if isFormatRight:
        if outCsvPth is None:
            raise ErrorUser('The input filePth is not a string form, please recorect it...')
        else:
            df_featureAdClass = pd.read_csv(incsvFile)
            featureData = df_featureAdClass.drop(columns=['class'])
            columnNames = df_featureAdClass.columns.values.tolist()
            stdsc=StandardScaler()
            normedData = stdsc.fit_transform(featureData.T)
            classColData = df_featureAdClass['class']
            newFeatureData = np.vstack([classColData.T,normedData.T]).T
            newFeatDf = pd.DataFrame(newFeatureData, columns = columnNames)
            writeDf2csv(newFeatDf,outCsvPth)
            fun_chgCsv2Arff(outCsvPth,outArfPth,'s')
def main():
    parser = argparse.ArgumentParser(description="Normalize the original csv file")
    parser.add_argument('-i', '--infile', help="The input file should be saved in the csv format, other file types are not supported at present", required=True)
    args = parser.parse_args()
    subfunNormCsvAdArff(args.infile)
if __name__ == "__main__":
    main()