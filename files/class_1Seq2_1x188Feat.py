#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:54:19 2021
@author: tafch
"""
import numpy as np
import pandas as pd
import copy
from files.class_calc15d_1RedSeq import *
class ErrorUser(Exception):
    pass
class proteinSeq(object):
    __prop_H=["RKEDQN","GASTPHY","CVLIMFW"]
    __prop_N= [ "GASCTPD","NVEQIL","MHKFRYW" ]
    __prop_Pe =["LIFWCMVY","PATGS","HQRKNED" ]
    __prop_Pa=  ["GASDT","CPNVEQIL","KMHFRYW" ]
    __prop_C=["KR", "ANCQGHILMFPSTWYV","DE" ]
    __prop_ST=["GQDNAHR", "KTSEC","ILMFPWYV" ]
    __prop_SS=["EALMQKRH", "VIYCWFT","GNPSD" ]
    __prop_SA=["ALFCGIVW", "RKQEND","MPSTHY" ]
    __alphaDictList=(__prop_H, __prop_N , __prop_Pe , __prop_Pa , __prop_C , __prop_ST , __prop_SS , __prop_SA)
    def __init__(self, givenSeq):
        self._transdSeq = None
        self._feat188 = None
        self._feat_comp20 = None
        if isinstance(givenSeq, str):
            self._origSeq = givenSeq
        else:
            raise ErrorUser('The given parameter in fun:origSeq is not a string')
    def f_transSeqAaCaps(self):
        s_origseq_t = self._origSeq
        self._origSeq = s_origseq_t.upper()
    def f_cacl20Comp_vec(self):
        s_20AmAcids = 'ACDEFGHIKLMNPQRSTVWY'
        d_20AmAcids = {}
        for i in range(len(s_20AmAcids)):
            s_curAmAcid = s_20AmAcids[i]
            d_20AmAcids[s_curAmAcid] = 0
        for s_aaInSeq in self._origSeq:
            d_20AmAcids[s_aaInSeq] += 1
        ls_comp20_t = []
        for i in range(len(s_20AmAcids)):
            s_curAmAcid = s_20AmAcids[i]
            i_val_curAa = d_20AmAcids[s_curAmAcid]
            ls_comp20_t.append(i_val_curAa)
        ls_comp20_t_norm = [item/len(self._origSeq) for item in  ls_comp20_t]
        self._feat_comp20 = ls_comp20_t_norm
    def f_getRepLetLsAdDict(self, alpBetList):
        ls_represLetters = []
        ls_dipepAbAc = []
        d_redCast = {}
        for s_curClusGroup in alpBetList:
            if len(s_curClusGroup)==0:
                raise ErrorUser('The current cluster group is empty, please check...')
            else:
                ls_represLetters.append(s_curClusGroup[0])
            curRedLetter = s_curClusGroup[0]
            for origLetter in s_curClusGroup:
                d_redCast[origLetter] = curRedLetter
        for i in range(len(ls_represLetters)-1):
            for j in range(i+1, len(ls_represLetters)):
                s_curDipepAbAc = ''.join([ls_represLetters[i],ls_represLetters[j]])
                ls_dipepAbAc.append(s_curDipepAbAc)
        return ls_represLetters, ls_dipepAbAc,d_redCast
    def f_recodeSeqByDict(self, d_redcast):
        ls_recodedLetters = []
        for i in range(len(self._origSeq)):
            s_curAmAcid = self._origSeq[i]
            s_recdAaLetter = d_redcast[s_curAmAcid]
            ls_recodedLetters.append(s_recdAaLetter)
        s_recdSeq = ''.join(ls_recodedLetters)
        self._transdSeq = s_recdSeq
    def f_recodeSeqByAlphabet(self, alpbetList):
        ls_repLetter, ls_dipepAbBc, d_redcCast = self.f_getRepLetLsAdDict(alpbetList)
        obj_21dFeat = c_get21Dfeat_redSeq(self._transdSeq,ls_repLetter, ls_dipepAbBc, d_redcCast)
        obj_21dFeat.f_gene21dVector()
        ls_1x21_redSchm = obj_21dFeat._ls_1x21_allFeat
        return ls_1x21_redSchm
    def f_main_gene188d(self):
        self.f_transSeqAaCaps()
        self.f_cacl20Comp_vec() 
        ls_1x168_propFeat = []
        for i in range(len(self.__alphaDictList)):
            ls_curRedSchm = self.__alphaDictList[i]
            ls_represLetters, ls_dipepAbAc,d_redCast  = self.f_getRepLetLsAdDict(ls_curRedSchm)
            self.f_recodeSeqByDict(d_redCast)
            if self._transdSeq is None:
                raise ErrorUser('The output of the recode fun is not produced, please check...')
            ls_1x21_curRedSchm = self.f_recodeSeqByAlphabet(ls_curRedSchm)
            ls_1x168_propFeat.extend(ls_1x21_curRedSchm)
        self._feat188 = copy.deepcopy(self._feat_comp20)
        self._feat188.extend(ls_1x168_propFeat)
        return self._feat188
