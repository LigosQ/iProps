#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 21:21:13 2019
@author: admin
"""
import sys
import numpy as np
import pandas as pd
from fun_dfData2Csv import *
class ErrorUser(Exception):
    pass
class RecodeSeq(object):
    def __int__(self):
        self._inFilePth = None
        self._alphaBet = None
        self._pthForRecodfile = None
        self._pthForFeatfile = None
        self._negOrPos = None
    @property
    def inFilePth(self):
        return self._inFilePth
    @inFilePth.setter
    def inFilePth(self,inFilePth):
        listOfSplitedPth = inFilePth.split('.')
        nameOfSuffix = listOfSplitedPth[-1]
        if nameOfSuffix=='fasta':
            pass
        elif nameOfSuffix=='txt':
            pass
        else:
            raise ErrorUser('The infile path is error,please check and ensure it is fasta or txt format!...')
            sys.exit()
        self._inFilePth = inFilePth            
    @property
    def alphaBet(self):
        return self._alphaBet
    @alphaBet.setter
    def alphaBet(self, dictVal):
        if isinstance(dictVal,dict):
            pass
        else:
            raise ErrorUser('Your input alphabet should be a dict style, please chech and retry...')
        self._alphaBet = dictVal
    @property
    def negOrPos(self):
        return self._negOrPos
    @negOrPos.setter
    def negOrPos(self,val):
        if val=='neg':
            self._negOrPos = 'neg'
        elif val == 'pos':
            self._negOrPos = 'pos'
        else:
            raise ErrorUser('The value of negOrPos is limited in "neg" or "pos",please check your input and verify it')
    def geneRecodeAdFeatFilePth(self):
        inFilPth = self._inFilePth
        pthList = inFilPth.split('/')
        fileNameStr = pthList[-1]
        filNameList = fileNameStr.split('.')
        pureFilename = filNameList[0]
        newName_recoded = pureFilename + '_recoded.fasta'
        newName_Feat = pureFilename + '_feat.csv'
        newNamList_recoded = []
        newNamList_Feat = []
        lenNamList = len(pthList)
        for i in range(lenNamList):
            if i==(lenNamList-1):
                newNamList_recoded.append(newName_recoded)
                newNamList_Feat.append(newName_Feat)
            else:
                newNamList_recoded.append(pthList[i])
                newNamList_Feat.append(pthList[i])
        self._pthForRecodfile = '/'.join(newNamList_recoded)
        self._pthForFeatfile = '/'.join(newNamList_Feat)
    def prodAlphtDict(self):
        origAminoAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
        origAmAcDict = dict(zip(origAminoAcid,origAminoAcid))
        userDic = self.alphaBet
        for key,val in userDic.items():
            listTmp = list(val)
            numInList = len(listTmp)
            for i in range(numInList):
                curAminoAcid = val[i]
                origAmAcDict[curAminoAcid] = key
        return origAmAcDict
    def recodeSeq(self):
        self.geneRecodeAdFeatFilePth()
        recodeDict = self.prodAlphtDict()
        f_id = open(self._inFilePth)
        f_id_out = open(self._pthForRecodfile,'w+')
        for line in f_id.readlines():
            if line.startswith('>'):
                f_id_out.write(line)
            else:
                curSequence = line.strip('\n')
                curSequence = line.strip('\t')
                curSequence = line.strip('\n')
                lenCurSeq = len(curSequence)
                recodedSeqList = []
                for i in range(lenCurSeq):
                    acid = curSequence[i]
                    recodeAcid = recodeDict[acid]
                    recodedSeqList.append(recodeAcid)
                recodedStr = ''.join(recodedSeqList)
                f_id_out.write(recodedStr+'\n')
        f_id.close()
        f_id_out.close()
    def transSeq2DipepVal(self,curSeq,dictDipep,gap):
        curSeq = curSeq.strip('\n')
        lenSeq = len(curSeq)
        for key, value in dictDipep.items():
            dictDipep[key] = 0
        for i in range(lenSeq-gap-1):
            curDipep = ''.join([curSeq[i],curSeq[i+gap+1]])
            dictDipep[curDipep] += 1
        return dictDipep
    def geneDepipDictByRecdlist(self,recodedList):
        numAlphabet = len(recodedList)
        dipepList_0 = [''.join([recodedList[i],recodedList[j]])for i in range(numAlphabet) for j in range(numAlphabet)]
        valOfDipep = [0 for i in range(numAlphabet*numAlphabet)]
        dictDipep = dict(zip(dipepList_0,valOfDipep))
        return dictDipep
    def getPropSetOfAlphabet(self):
        properList = []
        recodeDict = self.prodAlphtDict()
        for key,val in recodeDict.items():
            properList.append(val)
        finalSymbList = sorted(set(properList),key=properList.index)
        isInitState = True
        csvColNameList = []
        featMatrix_1D = []
        lableList1D = []
        fid_feat = open(self._pthForRecodfile)
        for line in fid_feat.readlines():
            if line.startswith('>'):
                pass
            else:
                dictDipep_0 = self.geneDepipDictByRecdlist(finalSymbList)
                dictDipep_1 = self.geneDepipDictByRecdlist(finalSymbList)
                dictDipep_2 = self.geneDepipDictByRecdlist(finalSymbList)
                dictDipep_0 = self.transSeq2DipepVal(line,dictDipep_0,0)
                dictDipep_1 = self.transSeq2DipepVal(line,dictDipep_1,1)
                dictDipep_2 = self.transSeq2DipepVal(line,dictDipep_2,2)
                curSeq3DepipList = []
                if self._negOrPos=='neg':
                    curSeq3DepipList.append(0)
                elif self._negOrPos == 'pos':
                    curSeq3DepipList.append(1)
                else:
                    raise ErrorUser('There is a problem in saving the label into list')
                if isInitState:
                    csvColNameList.append('class')
                for key,val in dictDipep_0.items():
                    if isInitState:
                        csvColNameList.append(key)
                    curSeq3DepipList.append(val)
                for key,val in dictDipep_1.items():
                    if isInitState:
                        csvColNameList.append(''.join([key[0],'*',key[1]]))
                    curSeq3DepipList.append(val)
                for key,val in dictDipep_2.items():
                    if isInitState:
                        csvColNameList.append(''.join([key[0],'**',key[1]]))
                    curSeq3DepipList.append(val)
                isInitState = False
                featMatrix_1D.append(curSeq3DepipList)
        featNparray = np.array(featMatrix_1D)
        dfAllFeat = pd.DataFrame(featNparray,columns=csvColNameList)
        writeDf2csv(dfAllFeat,self._pthForFeatfile)
    