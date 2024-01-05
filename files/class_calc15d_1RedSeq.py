#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 08:50:18 2021
@author: tafch
"""
import numpy as np
import pandas as pd
class ErrorUser(Exception):
    pass
class c_get21Dfeat_redSeq(object):
    def __init__(self, s_givenRedSeq, ls_given_repLeter, ls_given_DepAcBc, d_redCast):
        self._ls_1x3_eachGrup_norm = None
        self._ls_1x3_eachGrup_orig = None
        self._ls_1x3_fAbBc = None
        self._ls_1x15_fQuater = None
        self._ls_1x21_allFeat = None
        self._s_redSeq = None
        self._ls_repLetter = None
        self._ls_DepAcBc = None
        self._d_redCast = None
        if isinstance(s_givenRedSeq,str):
            self._s_redSeq = s_givenRedSeq
        else:
            raise ErrorUser('Your given para in the class construct function is not a string')
        if isinstance(ls_given_repLeter,list):
            self._ls_repLetter = ls_given_repLeter
        else:
            raise ErrorUser('Your given para of representative list is not a list type')
        if isinstance(ls_given_DepAcBc, list):
            self._ls_DepAcBc = ls_given_DepAcBc
        else:
            raise ErrorUser('Your given para of DeptideAcBc is not a list type')
        if isinstance(d_redCast, dict):
            self._d_redCast = d_redCast
        else:
            raise ErrorUser('your given para of dictRedutctionCast is not a dict type')
    def __countGroupNumber(self):
        ls_freq = []
        for i in range(len(self._ls_repLetter)):
            i_freqVal = 0
            s_cur_AmAcidLetter = self._ls_repLetter[i]
            i_freqVal = self._s_redSeq.count(s_cur_AmAcidLetter)
            ls_freq.append(i_freqVal)
        ls_freq_norm = [ls_freq[i]/len(self._s_redSeq) for i in range(len(ls_freq))]
        self._ls_1x3_eachGrup_norm = ls_freq_norm
        self._ls_1x3_eachGrup_orig = ls_freq
    def __countDipepAbBc(self):
        ls_freqDipep = []
        for i in range(len(self._ls_DepAcBc)):
            s_curDipep = self._ls_DepAcBc[i]
            i_freqDipep_1 = self._s_redSeq.count(s_curDipep)
            i_freqDipep_2 = self._s_redSeq.count(''.join([s_curDipep[1],s_curDipep[0]]))
            if s_curDipep[1]==s_curDipep[0]:
                i_freqDipep = (i_freqDipep_1+i_freqDipep_2)/2
            else:
                i_freqDipep = (i_freqDipep_1+i_freqDipep_2)
            ls_freqDipep.append(i_freqDipep)
        ls_freqDep_n = [ls_freqDipep[i]/(len(self._s_redSeq)-1) for i in range(len(ls_freqDipep))]
        self._ls_1x3_fAbBc = ls_freqDep_n
    def __calc_1x5_quarterIndVec(self, givenCurRepLetter, i_freqCurGroup):
        i_repeatNum = 0
        arr_quartInd_1x5 = np.zeros(5)
        for i in range(len(self._s_redSeq)):
            s_curSeqLetter = self._s_redSeq[i]
            if s_curSeqLetter == givenCurRepLetter:
                i_repeatNum += 1
                if i_repeatNum ==1:
                    arr_quartInd_1x5[0] = (i+1)/len(self._s_redSeq)
                if i_repeatNum == int(0.25*i_freqCurGroup):
                    arr_quartInd_1x5[1] = (i+1)/len(self._s_redSeq)
                if i_repeatNum == int(0.5*i_freqCurGroup):
                    arr_quartInd_1x5[2] = (i+1)/len(self._s_redSeq)
                if i_repeatNum == int(0.75*i_freqCurGroup):
                    arr_quartInd_1x5[3] = (i+1)/len(self._s_redSeq)
                if i_repeatNum == (i_freqCurGroup):
                    arr_quartInd_1x5[4] = (i+1)/len(self._s_redSeq)
        ls_quartInd_1x5 = arr_quartInd_1x5.tolist()
        return ls_quartInd_1x5
    def __calcQuartIndVal(self):
        ls_quartFeat_1x15 = []
        ls_repLetter = self._ls_repLetter
        for i in range(len(ls_repLetter)):
            s_curRepLetter = ls_repLetter[i]
            i_freq_curGroup = self._ls_1x3_eachGrup_orig[i]
            ls_quarterFeat_1x5 = self.__calc_1x5_quarterIndVec(s_curRepLetter,i_freq_curGroup)
            ls_quartFeat_1x15.extend(ls_quarterFeat_1x5)
        self._ls_1x15_fQuater = ls_quartFeat_1x15
    def f_checkValidation(self, givenVar,varname):
        if givenVar is None:
            raise ErrorUser('The member variable '+ varname+' is None, please check')
    def f_checkValidation_g(self, givenVar,varname):
        if givenVar is None:
            raise ErrorUser('The member variable did not generated in function, '+ varname+
                            '"s current state is None, please check...')
    def f_comb3feat_1x21Vec(self, ls_3featlist):
        ls_1x21_finalFeat = []
        for i in range(len(ls_3featlist)):
            ls_curFeatList_i = ls_3featlist[i]
            ls_1x21_finalFeat.extend(ls_curFeatList_i)
        return ls_1x21_finalFeat
    def f_gene21dVector(self):
        self.f_checkValidation(self._s_redSeq,'redSeq')
        self.f_checkValidation(self._ls_repLetter,'repLetter')
        self.f_checkValidation(self._ls_DepAcBc,'DepAcBc')
        self.f_checkValidation(self._d_redCast,'redCast')
        self.__countGroupNumber()
        self.f_checkValidation_g(self._ls_1x3_eachGrup_norm, 'group_1x3')
        self.__countDipepAbBc()
        self.f_checkValidation_g(self._ls_1x3_fAbBc, 'dipep_1x3')
        self.__calcQuartIndVal()
        self.f_checkValidation_g(self._ls_1x15_fQuater, 'quarter_1x15')
        self._ls_1x21_allFeat = self.f_comb3feat_1x21Vec([self._ls_1x3_eachGrup_norm,self._ls_1x3_fAbBc,self._ls_1x15_fQuater])
