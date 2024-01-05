#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 15:13:37 2022
@author: sealight
"""
"""
Created on Thu May 20 16:40:42 2021
@author: tafch
"""
import sys
import numpy as np
import pandas as pd
import os
class ErrorUser(Exception):
    pass
class c_calc1Dipep_1schm(object):
    def __init__(self, givenTripTypeNo):
        self._s_inFilePth = None
        self._d_alphaBet = None
        self._s_pthForRecodfile = None
        self._s_pthForFeatfile = None
        self._s_negOrPos = None
        self._i_tripTypeNo = None
        self._s_pthForAAcomps = None
        self._ls_allRecodedLines = None
        if isinstance(givenTripTypeNo, int):
            self._i_tripTypeNo = givenTripTypeNo
        else:
            raise ErrorUser('The given tripetides type number should belongs to int type, please check you codes...')
    @property
    def inFilePth(self):
        return self._s_inFilePth
    @inFilePth.setter
    def inFilePth(self,inFilePth):
        if isinstance(inFilePth,str):
            pass
        else:
            raise ErrorUser('The path s_recdAmAcids in inFilePth function should be string, pleased check...')
        if os.path.isfile(inFilePth):
            pass
        else:
            raise ErrorUser('The input of inFilePth function should a existing file, your given s_recdAmAcids is not a file, pleased check...')
        listOfSplitedPth = inFilePth.split('.')
        nameOfSuffix = listOfSplitedPth[-1]
        if nameOfSuffix=='fasta':
            pass
        else:
            raise ErrorUser('The infile path is error,please check and ensure it is fasta or txt format!...')
            sys.exit()
        self._s_inFilePth = inFilePth            
    @property
    def alphaBet(self):
        return self._d_alphaBet
    @alphaBet.setter
    def alphaBet(self, dictVal):
        if isinstance(dictVal,dict):
            pass
        else:
            raise ErrorUser('Your input alphabet should be a dict style, please chech and retry...')
        self._d_alphaBet = dictVal
    @property
    def negOrPos(self):
        return self._s_negOrPos
    @negOrPos.setter
    def negOrPos(self,s_val):
        if s_val=='neg':
            self._s_negOrPos = 'neg'
        elif s_val == 'pos':
            self._s_negOrPos = 'pos'
        else:
            raise ErrorUser('The s_recdAmAcids of negOrPos is limited in "neg" or "pos",please check your input and verify it')
    def f_genePth_ForRecodedFasta_featCsv(self, i_tripTypeNo, i_schmNo):
        inFilPth = self._s_inFilePth
        pthList = inFilPth.split('/')
        fileNameStr = pthList[-1]
        filNameList = fileNameStr.split('.')
        pureFilename = filNameList[0]
        s_newName_recoded = ''.join([pureFilename,'_',str(i_schmNo),'_recoded.fasta'])
        if i_tripTypeNo is None:
            raise ErrorUser('The typeNumber should be 0~5, please check your initialization codes...')
        else:
            pass
        s_newName_Feat = ''.join([pureFilename, '_Dipep_type', str(i_tripTypeNo),'.csv'])
        s_csvName_compAA = ''.join([pureFilename, '_AAcomp.csv'])
        newNamList_recoded = []
        newNamList_Feat = []
        ls_namePthList_compAA = []
        lenNamList = len(pthList)
        for i in range(lenNamList):
            if i==(lenNamList-1):
                newNamList_recoded.append(s_newName_recoded)
                newNamList_Feat.append(s_newName_Feat)
                ls_namePthList_compAA.append(s_csvName_compAA)
            else:
                newNamList_recoded.append(pthList[i])
                newNamList_Feat.append(pthList[i])
                ls_namePthList_compAA.append(pthList[i])
        self._s_pthForRecodfile = '/'.join(newNamList_recoded)
        self._s_pthForFeatfile = '/'.join(newNamList_Feat)
        self._s_pthForAAcomps = '/'.join(ls_namePthList_compAA)
    def f_geneAlphaDict(self):
        ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
        d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
        d_redStr2Dict = self.alphaBet
        for s_key,s_val in d_redStr2Dict.items():
            ls_curGropElems = list(s_val)
            numInList = len(ls_curGropElems)
            for i in range(numInList):
                s_curAmiAcid = s_val[i]
                d_origAmAcid_2RedStr[s_curAmiAcid] = s_key
        return d_origAmAcid_2RedStr
    def f_clac1AaCompList(self, s_seq, ls_remRedAmAcids):
        s_seq.strip('\n')
        s_seq.strip('\r')
        ls_remRedAmAcids.sort()
        d_redAaComp = {}
        for i in range(len(ls_remRedAmAcids)):
            d_redAaComp[ls_remRedAmAcids[i]] = 0
        i_seqLen = len(s_seq)
        for i_item in range(len(s_seq)):
            if s_seq[i_item]=='\n':
                pass
            else:
                d_redAaComp[s_seq[i_item]] += 1
        for s_key, i_keyFreq in d_redAaComp.items():
            d_redAaComp[s_key] = i_keyFreq/i_seqLen
        ls_redAaFreq = []
        ls_redAaNames = []
        for i_ind in range(len(ls_remRedAmAcids)):
            ls_redAaFreq.append(d_redAaComp[ls_remRedAmAcids[i_ind]])
            ls_redAaNames.append(ls_remRedAmAcids[i_ind])
        return ls_redAaFreq, ls_redAaNames
    def recodeSeq(self,i_tripeTypeNo, i_schmNo):
        self.f_genePth_ForRecodedFasta_featCsv(i_tripeTypeNo,i_schmNo)
        d_origAA_2_redAA = self.f_geneAlphaDict()
        f_id = open(self._s_inFilePth)
        ls_all_recodedLines = []
        for s_curLine in f_id.readlines():
            if s_curLine.startswith('>'):
                pass
            else:
                s_curSequence = s_curLine.strip('\n')
                s_curSequence = s_curLine.strip('\t')
                s_curSequence = s_curLine.strip('\n')
                i_lenCurSeq = len(s_curSequence)
                ls_recodedSeqElems = []
                for i in range(i_lenCurSeq):
                    s_acid = s_curSequence[i]
                    s_recdAmAcid = d_origAA_2_redAA[s_acid]
                    ls_recodedSeqElems.append(s_recdAmAcid)
                s_recdSeqStr = ''.join(ls_recodedSeqElems)
                ls_all_recodedLines.append(s_recdSeqStr)
        f_id.close()
        self._ls_allRecodedLines = ls_all_recodedLines
    def f_normDict_withSeqLen(self, d_tripeFreq, i_seqLen):
        return d_tripeFreq
    def f_geneFreqDict_eachDipep(self,curSeq,d_tripDict,i_typeNo):
        curSeq = curSeq.strip('\n')
        lenSeq = len(curSeq)
        for s_key, s_recdAmAcids in d_tripDict.items():
            d_tripDict[s_key] = 0
        if i_typeNo == 0:
            for i in range(lenSeq-1):
                s_curDipep = ''.join([curSeq[i],curSeq[i+1]])
                d_tripDict[s_curDipep] += 1
        elif i_typeNo == 1:
            for i in range(lenSeq-2):
                s_curDipep = ''.join([curSeq[i],curSeq[i+2]])
                d_tripDict[s_curDipep] += 1
        elif i_typeNo == 2:
            for i in range(lenSeq-3):
                s_curDipep = ''.join([curSeq[i],curSeq[i+3]])
                d_tripDict[s_curDipep] += 1
        else:
            raise ErrorUser('The i_tpyeNo is in the range of 0~2, other typeNumber is not support now...')
        return d_tripDict,lenSeq
    def f_geneEmptyDipDict_curSchm(self,ls_remRedAmAcids):
        numAlphabet = len(ls_remRedAmAcids)
        d_tripList_0 = [''.join([ls_remRedAmAcids[i],ls_remRedAmAcids[j]])
                            for i in range(numAlphabet) for j in range(numAlphabet)]
        i_valOfTripe = [0 for i in range(numAlphabet*numAlphabet)]
        d_tripDict = dict(zip(d_tripList_0,i_valOfTripe))
        return d_tripDict
    def f_getFreq_rAmAcid(self):
        ls_remRAAs_temp = []
        d_origAA_2_redAA = self.f_geneAlphaDict()
        for s_key,s_val in d_origAA_2_redAA.items():
            s_redAmAcids = s_val
            ls_remRAAs_temp.append(s_redAmAcids)
        ls_allRemRedAmAcids = sorted(set(ls_remRAAs_temp),key=ls_remRAAs_temp.index)
        isInitState = True
        fid_feat = open(self._s_pthForRecodfile)
        ls_colNamesInFeatCsv = []
        ls_featMat_eachAA = []
        for s_curLine in fid_feat.readlines():
            if s_curLine.startswith('>'):
                pass
            else:
                ls_freqEachAA, ls_nameEachAA = self.f_clac1AaCompList(s_curLine,ls_allRemRedAmAcids)
                ls_1TypeTrip_ofCurSeq = []
                if self._s_negOrPos=='neg':
                    ls_1TypeTrip_ofCurSeq.append(0)
                elif self._s_negOrPos == 'pos':
                    ls_1TypeTrip_ofCurSeq.append(1)
                else:
                    raise ErrorUser('There is a problem in saving the label into list')
                if isInitState:
                    ls_colNamesInFeatCsv.append('class')
                    ls_colNamesInFeatCsv.extend(ls_nameEachAA)
                    isInitState = False
                else:
                    pass
                ls_1TypeTrip_ofCurSeq.extend(ls_freqEachAA)
                ls_featMat_eachAA.append(ls_1TypeTrip_ofCurSeq)
        arr_featNparray = np.array(ls_featMat_eachAA)
        df_compAA_1type = pd.DataFrame(arr_featNparray,columns=ls_colNamesInFeatCsv)
        return df_compAA_1type
    def f_getDipepDf_AdCsv_ofCurShm(self):
        ls_remRAAs_temp = []
        d_origAA_2_redAA = self.f_geneAlphaDict()
        for s_key,s_val in d_origAA_2_redAA.items():
            s_redAmAcids = s_val
            ls_remRAAs_temp.append(s_redAmAcids)
        ls_allRemRedAmAcids = sorted(set(ls_remRAAs_temp),key=ls_remRAAs_temp.index)
        isInitState = True
        ls_colNamesInFeatCsv = []
        featMatrix_1D = []
        ls_all_recodedLines = self._ls_allRecodedLines
        for i_lineNo in range(len(ls_all_recodedLines)):
            s_curLine = ls_all_recodedLines[i_lineNo]
            if s_curLine.startswith('>'):
                pass
            else:
                d_allTripFreq = self.f_geneEmptyDipDict_curSchm(ls_allRemRedAmAcids)
                if self._i_tripTypeNo is None:
                    raise ErrorUser('The tripeTypeNumber is None in the object. please check your initialization step...')
                else:
                    pass
                d_allTripFreq, i_seqLen = self.f_geneFreqDict_eachDipep(s_curLine,d_allTripFreq,self._i_tripTypeNo)
                d_allTripFreq = self.f_normDict_withSeqLen(d_allTripFreq, i_seqLen)
                ls_1TypeTrip_ofCurSeq = []
                if self._s_negOrPos=='neg':
                    ls_1TypeTrip_ofCurSeq.append(0)
                elif self._s_negOrPos == 'pos':
                    ls_1TypeTrip_ofCurSeq.append(1)
                else:
                    raise ErrorUser('There is a problem in saving the label into list')
                if isInitState:
                    ls_colNamesInFeatCsv.append('class')
                if self._i_tripTypeNo == 0:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join(['XX-',s_key]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._i_tripTypeNo == 1:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join(['X*X-',s_key]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._i_tripTypeNo == 2:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join(['X**X-',s_key]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                else:
                    raise ErrorUser('The typeNumber should be 0~5, please check your initialization codes...')
                isInitState = False
                featMatrix_1D.append(ls_1TypeTrip_ofCurSeq)
        arr_featNparray = np.array(featMatrix_1D)
        df_dipepFeat_1type = pd.DataFrame(arr_featNparray,columns=ls_colNamesInFeatCsv)
        return df_dipepFeat_1type
