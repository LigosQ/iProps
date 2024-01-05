#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:59:06 2023
@author: sealight
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
class ErrorCoding(Exception):
    pass
def f_calcCorre(aa_1, aa_2, arr_aaProp, d_aaIndex):
    f_corr = sum([(arr_aaProp[i_type][d_aaIndex[aa_1]]-arr_aaProp[i_type][d_aaIndex[aa_2]])**2 for i_type in range(len(arr_aaProp))]) / len(arr_aaProp)
    return f_corr
def f_PAAC(s_1seq, i_lambda, f_w):
    ls_index = range(20)
    ls_20AA = list('ARNDCQEGHILKMFPSTWYV')
    d_20AA_idx = dict(zip(ls_20AA,ls_index))
    arr_aaProp = np.array([[0.62,  -2.53,  -0.78,  -0.9,  0.29,  -0.85,  -0.74,  0.48,  -0.4,  1.38,  1.06,  -1.5,  0.64,  1.19,  0.12,  -0.18,  -0.05,  0.81,  0.26,  1.08],
                          [-0.5,  3,  0.2,  3,  -1,  0.2,  3,  0,  -0.5,  -1.8,  -1.8,  3,  -1.3,  -2.5,  0,  0.3,  -0.4,  -3.4,  -2.3,  -1.5],
                          [15,  101,  58,  59,  47,  72,  73,  1,  82,  57,  57,  73,  75,  91,  42,  31,  45,  130,  107,  43]])
    scaler = StandardScaler()
    arr_aaProp_stded = scaler.fit_transform(arr_aaProp.T).T
    ls_PAAC = []
    ls_theta = []
    if i_lambda >= (len(s_1seq)):
        i_lambda = (len(s_1seq)-1)
        print('Warning: The lambda value was adapted to the max value to make the coding run...')
    else:
        pass
    for n_skip in range(1, i_lambda + 1):
        ls_corr_nSkip = [f_calcCorre(s_1seq[j], s_1seq[j + n_skip], arr_aaProp_stded, d_20AA_idx) for j in range(len(s_1seq) - n_skip)]
        ls_theta.append(sum(ls_corr_nSkip) / (len(s_1seq) - n_skip))
    d_20aaFreq_inSeq = {}
    for aa in ls_20AA:
        d_20aaFreq_inSeq[aa] = s_1seq.count(aa)
    ls_PAAC.extend([round(d_20aaFreq_inSeq[aa] / (1 + f_w * sum(ls_theta)),6) for aa in ls_20AA])
    ls_PAAC.extend([round((f_w * j) / (1 + f_w * sum(ls_theta)),6) for j in ls_theta])
    return ls_PAAC
def f_PAAC_1type(ls_multiSeqs, i_lambda, s_posOrNeg,fl_w):
    ls_colNamesList = []
    for idx in range(1, i_lambda+1):
        s_propNam_i = ''.join(['PAAC.L',str(idx)])
        ls_colNamesList.append(s_propNam_i)
    ls_20AA = list('ARNDCQEGHILKMFPSTWYV')
    ls_20AAComps = [''.join(['PAAC.Comp.', ls_20AA[j]]) for j in range(len(ls_20AA))]
    ls_colNamesList.extend(ls_20AAComps)
    ls_colNamesList.append('class')
    ls_featMat = []
    for idx, s_seq_i in enumerate(ls_multiSeqs):
        ls_dipVal = f_PAAC(s_seq_i, i_lambda,fl_w)
        if s_posOrNeg.lower()=='pos':
            ls_dipVal.append(1)
        elif s_posOrNeg.lower()=='neg':
            ls_dipVal.append(0)
        else:
            raise ErrorCoding('The second parameter is wrong. Only "pos"/"neg" is supportted.')
        ls_featMat.append(ls_dipVal)
    arr_featMat = np.array(ls_featMat)
    return np.array(ls_colNamesList), arr_featMat
def f_PAAC_2types(d_seqs_in2types,i_lambda,fl_w):
    ls_colnames_pos, arr_feats_pos = f_PAAC_1type(d_seqs_in2types['pos'],i_lambda,'pos',fl_w)
    ls_colNames_neg, arr_feats_neg = f_PAAC_1type(d_seqs_in2types['neg'],i_lambda,'neg',fl_w)
    if (ls_colnames_pos == ls_colNames_neg).all():
        arr_feats_2types = np.vstack((arr_feats_pos, arr_feats_neg))
        df_feats_2types = pd.DataFrame(arr_feats_2types, columns=ls_colnames_pos)
    else:
        raise ErrorCoding('The column name lists are different. Please check your CTDC codes...')
    return df_feats_2types
    