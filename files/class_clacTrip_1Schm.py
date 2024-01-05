#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 17:30:14 2023
@author: sealight
"""
import sys
import numpy as np
import pandas as pd
import os
class ErrorUser(Exception):
    pass
class c_1schmRedSeq_calc1Tripes(object):
    def __init__(self, s_infile_tmp, d_alpha, s_posNeg_type, i_tripTypeNo):
        if isinstance(s_infile_tmp, str):
            self._s_inFilePth = s_infile_tmp
        else:
            raise ErrorUser(''.join(['The given value of infile should be string type, your given type is', type(s_infile_tmp)]))
        if isinstance(d_alpha, dict):
            self._d_alphaBet = d_alpha
        else:
            raise ErrorUser('Your input alphabet should be a dict style, please chech and retry...')
        if isinstance(s_posNeg_type, str):
            if (s_posNeg_type=='pos') or (s_posNeg_type=='neg'):
                self._s_negOrPos_type = s_posNeg_type
            else:
                raise ErrorUser(''.join(['The supporting value of neg/pos is only "pos" and "neg". However, your input value is ',(s_posNeg_type)]))
        else:
            raise ErrorUser(''.join(['The supporting value of neg/pos is only "pos" and "neg"(String type). However, your input type is ',type(s_posNeg_type)]))
        if isinstance(i_tripTypeNo, int):
            if i_tripTypeNo>=0 and i_tripTypeNo<=5:
                self._tripNo_i = i_tripTypeNo
            else:
                raise ErrorUser(''.join(['The supporting value of Tripep type is only 0~5(integer type). However, your value is ',str(i_tripTypeNo)]))
        else:
            raise ErrorUser(''.join(['The supporting value of Tripep type is only 0~5(integer type). However, your input type is ',type(i_tripTypeNo)]))
    def f_check_allParaStatus(self):
        self.geneRecodeAdFeatFilePth()
        if self._d_alphaBet is None:
            raise ErrorUser(''.join(['The element variable ', '﻿_d_alphaBet', 'is None, please check your codes ...']))
        if self._s_inFilePth is None:
            raise ErrorUser(''.join(['The element variable ', '﻿_s_inFilePth', 'is None, please check your codes ...']))
        if self._s_negOrPos_type is None:
            raise ErrorUser(''.join(['The element variable ', '﻿_s_negOrPos_type', 'is None, please check your codes ...']))
        if self._s_pthForRecodfile is None:
            raise ErrorUser(''.join(['The element variable ', '_s_pthForRecodfile', 'is None, please check your codes ...']))
        if self._s_pthForFeatfile is None:
            raise ErrorUser(''.join(['The element variable ', '_s_pthForFeatfile', 'is None, please check your codes ...']))
    def geneRecodeAdFeatFilePth(self):
        inFilPth = self._s_inFilePth
        pthList = inFilPth.split('/')
        fileNameStr = pthList[-1]
        filNameList = fileNameStr.split('.')
        pureFilename = filNameList[0]
        s_newName_recoded = ''.join([pureFilename, '_recoded.fasta'])
        if self._tripNo_i is None:
            raise ErrorUser('The typeNumber should be 0~5, please check your initialization codes...')
        else:
            pass
        s_newName_Feat = ''.join(['../results/', pureFilename, '_trip_type', str(self._tripNo_i),'.csv'])
        newNamList_recoded = []
        newNamList_Feat = []
        lenNamList = len(pthList)
        for i in range(lenNamList):
            if i==(lenNamList-1):
                newNamList_recoded.append(s_newName_recoded)
                newNamList_Feat.append(s_newName_Feat)
            else:
                newNamList_recoded.append(pthList[i])
                newNamList_Feat.append(pthList[i])
        self._s_pthForRecodfile = '/'.join(newNamList_recoded)
        self._s_pthForFeatfile = '/'.join(newNamList_Feat)
    def prodAlphtDict(self):
        ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
        d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
        if self._d_alphaBet is None:
            raise ErrorUser('There is a error in the reduced dictionary assignment.')
        else:
            d_redStr2Dict = self._d_alphaBet
        for s_key,s_val in d_redStr2Dict.items():
            ls_curGropElems = list(s_val)
            numInList = len(ls_curGropElems)
            for i in range(numInList):
                s_curAmiAcid = s_val[i]
                d_origAmAcid_2RedStr[s_curAmiAcid] = s_key
        return d_origAmAcid_2RedStr
    def f_clac1AaCompList(self, s_seq, ls_remRedAmAcids):
        ls_remRedAmAcids.sort()
        d_redAaComp = {}
        for i in range(len(ls_remRedAmAcids)):
            d_redAaComp[ls_remRedAmAcids[i]] = 0
        i_seqLen = len(s_seq)
        for s_item in s_seq:
            d_redAaComp[s_item] += 1
        for s_key, i_keyFreq in d_redAaComp.items():
            d_redAaComp[s_key] = i_keyFreq/i_seqLen
        ls_redAaFreq = []
        ls_redAaNames = []
        for i_ind in range(len(ls_remRedAmAcids)):
            ls_redAaFreq.append(d_redAaComp[ls_remRedAmAcids[i_ind]])
            ls_redAaNames.append(ls_remRedAmAcids[i_ind])
        return ls_redAaFreq, ls_redAaNames
    def recodeSeq(self,i_tripeTypeNo):
        d_origAA_2_redAA = self.prodAlphtDict()
        f_id = open(self._s_inFilePth)
        f_id_out = open(self._s_pthForRecodfile,'w+')
        for s_curLine in f_id.readlines():
            if s_curLine.startswith('>'):
                f_id_out.write(s_curLine)
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
                f_id_out.write(s_recdSeqStr+'\n')
        f_id.close()
        f_id_out.close()
    def f_recod_1LineSeq(self, s_1lineSeq_str):
        s_1line_0Ending = s_1lineSeq_str.strip()
        d_curRecordDict =  self.prodAlphtDict()
        ls_recodedAA = []
        for i in range(len(s_1line_0Ending)):
            s_orig_AA = s_1line_0Ending[i]
            s_transed_AA = d_curRecordDict[s_orig_AA]
            ls_recodedAA.append(s_transed_AA)
        s_trandedSeq = ''.join(ls_recodedAA)
        return s_trandedSeq
    def f_normDict_withSeqLen(self, d_tripeFreq, i_seqLen):
        for s_key,i_val in d_tripeFreq.items():
            d_tripeFreq[s_key] = round(i_val/i_seqLen,4)
        return d_tripeFreq
    def transSeq2TripeVal(self,curSeq,d_tripDict,i_typeNo):
        curSeq = curSeq.strip('\n')
        lenSeq = len(curSeq)
        if isinstance(i_typeNo, int):
            if i_typeNo>=0 and i_typeNo<=5:
                self._tripNo_i = i_typeNo
            else:
                raise ErrorUser('Your input tripepitd type shoule be 0~5, please check your input...')
        for s_key, s_recdAmAcids in d_tripDict.items():
            d_tripDict[s_key] = 0
        if i_typeNo == 0:
            for i in range(lenSeq-2):
                s_curTripe = ''.join([curSeq[i],curSeq[i+1],curSeq[i+2]])
                d_tripDict[s_curTripe] += 1
        elif i_typeNo == 1:
            for i in range(lenSeq-3):
                s_curTripe = ''.join([curSeq[i],curSeq[i+2],curSeq[i+3]])
                d_tripDict[s_curTripe] += 1
        elif i_typeNo == 2:
            for i in range(lenSeq-3):
                s_curTripe = ''.join([curSeq[i],curSeq[i+1],curSeq[i+3]])
                d_tripDict[s_curTripe] += 1
        elif i_typeNo == 3:
            for i in range(lenSeq-4):
                s_curTripe = ''.join([curSeq[i],curSeq[i+3],curSeq[i+4]])
                d_tripDict[s_curTripe] += 1
        elif i_typeNo == 4:
            for i in range(lenSeq-4):
                s_curTripe = ''.join([curSeq[i],curSeq[i+1],curSeq[i+4]])
                d_tripDict[s_curTripe] += 1
        elif i_typeNo == 5:
            for i in range(lenSeq-4):
                s_curTripe = ''.join([curSeq[i],curSeq[i+2],curSeq[i+4]])
                d_tripDict[s_curTripe] += 1
        else:
            raise ErrorUser('The i_tpyeNo is in the range of 0~5, other typeNumber is not support now...')
        return d_tripDict,lenSeq
    def calcSeqDipep(self, s_curSeq, i_gap, d_dipDict):
        s_curSeq = s_curSeq.strip('\n')
        i_lenSeq = len(s_curSeq)
        for s_key, s_recdAmAcids in d_dipDict.items():
            d_dipDict[s_key] = 0
        if i_gap == 0:
            for i in range(i_lenSeq-1):
                s_curDipep = ''.join([s_curSeq[i],s_curSeq[i+1]])
                d_dipDict[s_curDipep] += 1
        elif i_gap == 1:
            for i in range(i_lenSeq-2):
                s_curDipep = ''.join([s_curSeq[i],s_curSeq[i+2]])
                d_dipDict[s_curDipep] += 1
        elif i_gap == 2:
            for i in range(i_lenSeq-3):
                s_curDipep = ''.join([s_curSeq[i],s_curSeq[i+3]])
                d_dipDict[s_curDipep] += 1
        elif i_gap == 3:
            for i in range(i_lenSeq-4):
                s_curDipep = ''.join([s_curSeq[i],s_curSeq[i+4]])
                d_dipDict[s_curDipep] += 1
        elif i_gap == 4:
            for i in range(i_lenSeq-5):
                s_curDipep = ''.join([s_curSeq[i],s_curSeq[i+5]])
                d_dipDict[s_curDipep] += 1
        else:
            raise ErrorUser('The i_tpyeNo is in the range of 0~5, other typeNumber is not support now...')
        return d_dipDict,i_lenSeq
    def f_geneTripDict_byRemRedAAs(self,ls_remRedAmAcids):
        numAlphabet = len(ls_remRedAmAcids)
        d_tripList_0 = [''.join([ls_remRedAmAcids[i],ls_remRedAmAcids[j], ls_remRedAmAcids[k]])
                            for i in range(numAlphabet) for j in range(numAlphabet) for k in range(numAlphabet)]
        i_valOfTripe = [0 for i in range(numAlphabet*numAlphabet*numAlphabet)]
        d_tripDict = dict(zip(d_tripList_0,i_valOfTripe))
        return d_tripDict
    def f_geneDipepDict_byRemRedAAs(self,ls_remRedAmAcids):
        numAlphabet = len(ls_remRedAmAcids)
        d_dipepList_0 = [''.join([ls_remRedAmAcids[i],ls_remRedAmAcids[j]])
                            for i in range(numAlphabet) for j in range(numAlphabet)]
        i_valOfDipep = [0 for i in range(numAlphabet*numAlphabet)]
        d_dipepDict = dict(zip(d_dipepList_0,i_valOfDipep))
        return d_dipepDict
    def f_geneTripFeat_curSchm(self):
        self.f_check_allParaStatus()
        ls_remRAAs_temp = []
        d_origAA_2_redAA = self.prodAlphtDict()
        for s_key,s_val in d_origAA_2_redAA.items():
            s_redAmAcids = s_val
            ls_remRAAs_temp.append(s_redAmAcids)
        ls_allRemRedAmAcids = sorted(set(ls_remRAAs_temp),key=ls_remRAAs_temp.index)
        isInitState = True
        featMatrix_1D = []
        fid_feat = open(self._s_inFilePth)
        for s_curLine in fid_feat.readlines():
            if s_curLine.startswith('>'):
                pass
            else:
                s_trandedCurLine_seq = self.f_recod_1LineSeq(s_curLine)
                d_allTripFreq = self.f_geneTripDict_byRemRedAAs(ls_allRemRedAmAcids)
                if self._tripNo_i is None:
                    raise ErrorUser('The tripeTypeNumber is None in the object. please check your initialization step...')
                else:
                    pass
                d_allTripFreq, i_seqLen = self.transSeq2TripeVal(s_trandedCurLine_seq,d_allTripFreq,self._tripNo_i)
                d_allTripFreq = self.f_normDict_withSeqLen(d_allTripFreq, i_seqLen)
                ls_1TypeTrip_ofCurSeq = []
                if self._s_negOrPos_type=='neg':
                    ls_1TypeTrip_ofCurSeq.append(0)
                elif self._s_negOrPos_type == 'pos':
                    ls_1TypeTrip_ofCurSeq.append(1)
                else:
                    raise ErrorUser('There is a problem in saving the label into list')
                if isInitState:
                    ls_colNamesInFeatCsv=[]
                    ls_colNamesInFeatCsv.append('class')
                if self._tripNo_i == 0:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join([s_key[0],s_key[1],s_key[2]]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._tripNo_i == 1:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join([s_key[0],'*',s_key[1],s_key[2]]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._tripNo_i == 2:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join([s_key[0],s_key[1],'*',s_key[2]]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._tripNo_i == 3:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join([s_key[0],'**',s_key[1],s_key[2]]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._tripNo_i == 4:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join([s_key[0],s_key[1],'**',s_key[2]]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                elif self._tripNo_i == 5:
                    for s_key,i_freq in d_allTripFreq.items():
                        if isInitState:
                            ls_colNamesInFeatCsv.append(''.join([s_key[0],'*',s_key[1],'*',s_key[2]]))
                        ls_1TypeTrip_ofCurSeq.append(i_freq)
                else:
                    raise ErrorUser('The typeNumber should be 0~5, please check your initialization codes...')
                isInitState = False
                featMatrix_1D.append(ls_1TypeTrip_ofCurSeq)
        fid_feat.close()
        arr_featNparray = np.array(featMatrix_1D)
        df_tripeFeat_1type = pd.DataFrame(arr_featNparray,columns=ls_colNamesInFeatCsv)
        df_tripeFeat_1type.to_csv(self._s_pthForFeatfile, index=False)
        return df_tripeFeat_1type
