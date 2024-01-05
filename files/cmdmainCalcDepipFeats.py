# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 21:07:14 2019
@author: admin
"""
import argparse
import pandas as pd
import numpy as np
from files.class_recodeSeq import *
from files.class_combNegAdPos2CSV import *
def chgStr2Dic(dicStr):
    codeDict = {}
    dicList = dicStr.split('#')
    for item in dicList:
        itemList = item.split('-')
        codeDict[itemList[0]] = itemList[1]
    return codeDict
def calcFeats(posfile,negfile,typeNum,reduceDict):
    recodingDict = chgStr2Dic(reduceDict)
    tsk_pos = RecodeSeq()
    tsk_pos.inFilePth = posfile
    tsk_pos.alphaBet = recodingDict
    tsk_pos.negOrPos='pos'
    tsk_pos.recodeSeq()
    tsk_pos.getPropSetOfAlphabet()
    posPth = tsk_pos._pthForFeatfile
    tsk_neg = RecodeSeq()
    tsk_neg.inFilePth = negfile
    tsk_neg.alphaBet = recodingDict
    tsk_neg.negOrPos = 'neg'
    tsk_neg.recodeSeq()
    tsk_neg.getPropSetOfAlphabet()
    negPth = tsk_neg._pthForFeatfile
    cmbTsk = combineNegAdPos2CSV()
    cmbTsk.posFile = posPth
    cmbTsk.negFile = negPth
    if isinstance(typeNum,str):
        specialStr = "~!@#$%^&*()+-*/<>,.[]\/"
        for item in typeNum:
            if item in specialStr:
                raise ErrorUser('Your given type name contains special sysbol, like as ~!@#$%^&*()+-*/<>,.[]\/, please check and correct them...')
        cmbTsk.typeNum = typeNum
    else:
        raise ErrorUser('The given type name is not a string type.please check and correct them...')
    finalFeatPd = cmbTsk.combine2files()
    return finalFeatPd
def main():
    parser = argparse.ArgumentParser(description="Recoding the original txt/fasta file and gives a feature file finally")
    parser.add_argument('-p', '--posFile', help="The input file should be saved in the txt format(txt,or fasta), other file types are not supported at present", required=True)
    parser.add_argument('-n', '--negFile', help="The input file should be saved in the txt format(txt,or fasta), other file types are not supported at present", required=True)
    parser.add_argument('-t', '--typeNum', help='The feature name:(string type), which is used for labeling csv file under different alphabets', required=True)
    parser.add_argument('-d', '--dict', help='The used dict: x-abc#y-def} is supported, which denotes abc is recoded x and def is recoded y', required=True)   
    args = parser.parse_args()
    calcFeats(args.posFile, args.negFile, args.typeNum, args.dict)
if __name__ == "__main__":
    main()