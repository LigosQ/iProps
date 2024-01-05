#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 09:51:26 2019
@author: admin
"""
import argparse
import pandas as pd
import numpy as np
class ErrorUser(Exception):
    pass
def isTheMember(dataSet,val):
    logicList = [1 if i==val else 0 for i in dataSet]
    sumVal = np.sum(logicList)
    if sumVal!=0:
        return True
    else:
        return False
def findIdx(labelData,val):
    b = np.array(labelData)
    c = b.reshape(len(b),)
    idxList = [i for i in range(len(c)) if c[i]==val]
    return idxList
def findTheIdxOfLable(dataSet,val):
    firstIdx = 3.1415
    if isTheMember(dataSet,val):
        indexForclass = findIdx(dataSet,val)
        if len(indexForclass)!=0:
            firstIdx = indexForclass[0]
            return firstIdx
        else:
            raise ErrorUser('When check the data, there is not "class" column in the CSV file')
    else:
        raise ErrorUser('Error: There is the second parameter in the data')
def arrangFeatList(columnNameList,lablePosIdx):
    numColumns = len(columnNameList)
    if lablePosIdx==0:
        newFeatlist = []
        for i in range(numColumns):
            if i>=1:
                newFeatlist.append(columnNameList[i])
        newFeatlist.append(columnNameList[0])
        return newFeatlist
    elif lablePosIdx==(numColumns-1):
        newFeatlist = [columnNameList[i] for i in range(numColumns)]
        return newFeatlist
    else:
        raise ErrorUser('The position of class column in csv file is wrong please check...')
def fun_chgCsv2Arff(infilePth,outfilePth,lableType):
    df_csvData = pd.read_csv(infilePth)
    fid_w = open(outfilePth,'w')
    columnName = df_csvData.columns.tolist()
    firstIdx = findTheIdxOfLable(columnName,'class')
    colNameForWritter = arrangFeatList(columnName,firstIdx)
    numFeats = len(columnName)
    fid_w.write('@Relation Protein\n')
    for i in range(numFeats):
        if i==(numFeats-1):
            if lableType=='n':
                fid_w.write('@attribute class {1,0}\n')
            elif lableType=='s':
                fid_w.write('@attribute calss {positive,negative}\n')
            else:
                raise ErrorUser('The value of parameter "-t" only support "n" and "s". Please check your input...')
        else:
            fid_w.write('@attribute '+colNameForWritter[i]+' real\n')
    fid_w.write('@data\n')
    for i in range(len(df_csvData.index)):
        curRowData = df_csvData.loc[i]
        arrangedData = arrangFeatList(curRowData,firstIdx)
        numCurRow = len(arrangedData)
        for j in range(numCurRow):
            if j==(numCurRow-1):
                curLable = (arrangedData[j])
                isOne = (curLable=='1' or curLable==1)
                isZero = (curLable=='0' or curLable==0)
                if (isOne or isZero):
                    if lableType=='s':
                        if isOne:
                            curLable = 'positive'
                        else:
                            curLable = 'negative'
                    else:
                        curLable = str(curLable)
                fid_w.write(str(curLable)+'\n')
            else:
                fid_w.write(str(arrangedData[j])+',')
    fid_w.close()
def main():
    parser = argparse.ArgumentParser(description="Transfrom the csv file to arff format")
    parser.add_argument('-i', '--infile', help="The input file should be csv format, other file types are not supported at present", required=True)
    parser.add_argument('-o', '--outfile', help='The name of output picture: .arff type', required=True)
    parser.add_argument('-t', '--type', help='value:n/s.==>n(for0/1) & s(positive/negative)', required=True)
    args = parser.parse_args()
    fun_chgCsv2Arff(args.infile, args.outfile,args.type)
if __name__ == "__main__":
    main()