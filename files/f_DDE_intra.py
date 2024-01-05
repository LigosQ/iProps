#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 20:14:55 2023
@author: sealight
"""
from files.c_dipFreqDict import c_dipFreqDict
import copy
from f_DDE import f_DDE
import numpy as np
import pandas as pd
from f_geneFastaDict import f_geneFastaDict
class ErrorCoding(Exception):
    pass
def f_DDE_1seq(s_1seq):
    s_curAAs = 'ACDEFGHIKLMNPQRSTVWY'
    d_allCodons = {
        'A': 4,
        'C': 2,
        'D': 2,
        'E': 2,
        'F': 2,
        'G': 4,
        'H': 2,
        'I': 3,
        'K': 2,
        'L': 6,
        'M': 1,
        'N': 2,
        'P': 4,
        'Q': 2,
        'R': 6,
        'S': 6,
        'T': 4,
        'V': 4,
        'W': 1,
        'Y': 2
    }
    d_Dc,ls_DipNames = c_dipFreqDict(s_curAAs).f_geneDipepDict()
    d_Tm = copy.deepcopy(d_Dc)
    d_Tv = copy.deepcopy(d_Dc)
    d_DDE = copy.deepcopy(d_Dc)
    d_DDE = f_DDE(s_1seq, d_Dc, d_Tm, d_Tv, d_allCodons, d_DDE)
    ls_dipVal = [d_DDE[ls_DipNames[i]] for i in range(len(ls_DipNames))]
    return ls_DipNames, ls_dipVal
def f_DDE_1type(ls_fastaSeqs, s_posOrNeg):
    ls_colnames = []
    ls_featMat = []
    for idx, s_seq_i in enumerate(ls_fastaSeqs):
        ls_DipNames, ls_dipVal = f_DDE_1seq(s_seq_i)
        if idx ==0:
            ls_colnames = ls_DipNames
            ls_colnames.append('class')
        if s_posOrNeg.lower()=='pos':
            ls_dipVal.append(1)
        elif s_posOrNeg.lower()=='neg':
            ls_dipVal.append(0)
        else:
            raise ErrorCoding('The second parameter is wrong. Only "pos"/"neg" is supportted.')
        ls_featMat.append(ls_dipVal)
    arr_featMat = np.array(ls_featMat)
    return np.array(ls_colnames), arr_featMat
def f_DDE_in2types(d_seqs_in2types):
    ls_colnames_pos, arr_feats_pos = f_DDE_1type(d_seqs_in2types['pos'],'pos')
    ls_colNames_neg, arr_feats_neg = f_DDE_1type(d_seqs_in2types['neg'],'neg')
    if (ls_colnames_pos == ls_colNames_neg).all():
        arr_feats_2types = np.vstack((arr_feats_pos, arr_feats_neg))
        df_feats_2types = pd.DataFrame(arr_feats_2types, columns=ls_colnames_pos)
    else:
        raise ErrorCoding('The column name lists are different. Please check your CTDC codes...')
    return df_feats_2types
