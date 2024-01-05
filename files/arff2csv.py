#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import argparse
import pandas as pd
import numpy as np
class ErrorUser(Exception):
    pass
def fun_arff2csv(infilePth,outfilePth):
    fid_r = open(infilePth)
    dataList = []
    flag = False
    savingStepNo = 0
    lenFeatList_1st = 0;
    for line in fid_r.readlines():
        if(flag):
            if line.strip()=='':
                continue
            curLineList = line.strip('\n').split(',')
            curFeatNumber = len(curLineList)
            if savingStepNo==1:
                lenFeatList_1st = curFeatNumber
                savingStepNo += 1
                TempList = []
                lable = curLineList[-1]
                if (lable=='positive' or lable=='Positive'):
                    TempList.append(1)
                elif (lable=='Negative' or lable=='negative'):
                    TempList.append(0)
                elif (lable==1 or lable=='1'):
                    TempList.append(1)
                elif (lable==0 or lable=='0'):
                    TempList.append(0)
                else:
                    raise ErrorUser('The class lable in arff file can be not idenfied!! only the lable:positive negative 1 0 is supported')
                for i in range(curFeatNumber-1):
                    TempList.append(curLineList[i])
                dataList.append(TempList)
            else:
                lenFeatList = curFeatNumber
                savingStepNo += 1
                if lenFeatList==lenFeatList_1st:
                    TempList = []
                    lable = curLineList[-1]
                    if (lable=='positive' or lable=='Positive'):
                        TempList.append(1)
                    elif (lable=='Negative' or lable=='negative'):
                        TempList.append(0)
                    elif (lable==1 or lable=='1'):
                        TempList.append(1)
                    elif (lable==0 or lable=='0'):
                        TempList.append(0)
                    else:
                        raise ErrorUser('The class lable in arff file can be idenfied....'
                                        'only the lable:positive negative 1 0 is supported')
                    for i in range(curFeatNumber-1):
                        TempList.append(curLineList[i])
                    dataList.append(TempList)
                else:
                    raise ErrorUser('The feature number of current line is different with previous line! Please check...')
        else:
            curLine = line.upper()
            if ((curLine.startswith('@DATA')) or flag):
                flag = True
                savingStepNo += 1
    fid_r.close()
    dataArray = np.zeros([savingStepNo-1,lenFeatList_1st])
    for i in range(savingStepNo-1):
        dataArray[i,:] = dataList[i]
    columnName = ['nFeat'+str(i+1) for i in range(lenFeatList_1st-1)]
    columnNameFull = ['class']
    columnNameFull[1:(lenFeatList_1st-1)] = columnName
    df_fullData = pd.DataFrame(data=dataArray, columns=columnNameFull)
    return df_fullData
def main():
    parser = argparse.ArgumentParser(description="Remove some features that is one member of higher correlation feature pair")
    parser.add_argument('-i', '--infile', help="The input file should be csv format, other file types are not supported at present", required=True)
    parser.add_argument('-o', '--outfile', help='The name of output picture: .csv type', required=True)
    args = parser.parse_args()
    fun_arff2csv(args.infile, args.outfile)
if __name__ == "__main__":
    main()