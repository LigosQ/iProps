#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 20:53:15 2023
@author: sealight
"""
import numpy as np
import pandas as pd
class ErrorCoding(Exception):
    pass
def f_calc_ASDC_1seq(s_prot_Seq):
    if isinstance(s_prot_Seq, str):
        pass
    else:
        raise ErrorCoding('Your given peremeters is not the string type.')
    AA = 'ACDEFGHIKLMNPQRSTVWY'
    ls_dipepNames = []
    for i_p in range(20):
        for j_n in range(20):
            s_pre = AA[i_p]
            s_suf = AA[j_n]
            ls_dipepNames.append(''.join([s_pre,s_suf]))
    d_dipep_freq = dict()
    for item in ls_dipepNames:
        d_dipep_freq[item] = 0
    i_seqLen = len(s_prot_Seq)
    i_allFreqNum = 0
    for i in range(i_seqLen):
        for j in range(i+1, i_seqLen):
            s_curDipep = ''.join([s_prot_Seq[i], s_prot_Seq[j]])
            d_dipep_freq[s_curDipep] += 1
            i_allFreqNum += 1
    for key,val in d_dipep_freq.items():
        d_dipep_freq[key] = val/i_allFreqNum
    ls_outNormFreq = []
    for i,s_aaPair in enumerate(ls_dipepNames):
        f_normFreq = d_dipep_freq[s_aaPair]
        ls_outNormFreq.append(float(format(f_normFreq,'.6f')))
    return ls_outNormFreq,ls_dipepNames
def f_isSameNames(ls_posNames,ls_negNames):
    for i,s_featName_p in enumerate(ls_posNames):
        if s_featName_p == ls_negNames[i]:
            pass
        else:
            return False
    return True
def f_calc_ASDC_1type(p_filePth):
    ls_allFeats = []
    try:
        with open(p_filePth,'r') as fid_fasta:
            for s_curLine in fid_fasta.readlines():
                if s_curLine.startswith('>'):
                    pass
                else:
                    s_stripSeq = s_curLine.strip()
                    ls_feat_1seq,ls_dipepNames = f_calc_ASDC_1seq(s_stripSeq)
                    ls_allFeats.append(ls_feat_1seq)
        arr_allFeats = np.array(ls_allFeats)
        return arr_allFeats,ls_dipepNames
    except IOError:
        raise ErrorCoding(''.join(["There is an erroe when open and load ", p_filePth]))
def f_ASDC_comb2FeatFiles(posFilPth, negFilePth):
    arr_posFeats,ls_featNames_pos = f_calc_ASDC_1type(posFilPth)
    arr_label_pos = np.array([1 for item in range(arr_posFeats.shape[0])])
    arr_featAdLabel_pos = np.vstack((arr_posFeats.T,arr_label_pos.T)).T
    arr_negFeats,ls_featNames_neg = f_calc_ASDC_1type(negFilePth)
    arr_label_neg = np.array([0 for item in range(arr_negFeats.shape[0])])
    arr_featAdLabel_neg = np.vstack((arr_negFeats.T,arr_label_neg.T)).T
    if f_isSameNames(ls_featNames_pos,ls_featNames_neg):
        arr_posAdNeg = np.vstack((arr_featAdLabel_pos,arr_featAdLabel_neg))
        ls_finalFeatNames = ls_featNames_pos
        ls_finalFeatNames.append('class')
        df_finalfeatAdType = pd.DataFrame(arr_posAdNeg,columns=ls_finalFeatNames)
        return df_finalfeatAdType
    else:
        raise ErrorCoding('The feature names are inconsistencies.')
