#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 19:05:07 2023
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
def f_APAAC(s_1seq, i_lambda, f_w=0.05):
    ls_index = range(20)
    ls_20AA = list('ARNDCQEGHILKMFPSTWYV')
    d_20AA_idx = dict(zip(ls_20AA,ls_index))
    arr_aaProp = np.array([[0.62,  -2.53,  -0.78,  -0.9,  0.29,  -0.85,  -0.74,  0.48,  -0.4,  1.38,  1.06,  -1.5,  0.64,  1.19,  0.12,  -0.18,  -0.05,  0.81,  0.26,  1.08],
                          [-0.5,  3,  0.2,  3,  -1,  0.2,  3,  0,  -0.5,  -1.8,  -1.8,  3,  -1.3,  -2.5,  0,  0.3,  -0.4,  -3.4,  -2.3,  -1.5]])
    scaler = StandardScaler()
    arr_aaProp_stded = scaler.fit_transform(arr_aaProp.T).T
    ls_featElemNames = [''.join(['Pc1.',s_elem]) for s_elem in ls_20AA]
    ls_aaPropNames = ['Hydrophobicity','Hydrophilicity']
    for j in range(1, i_lambda + 1):
        for s1PropName in ls_aaPropNames:
            ls_featElemNames.append(''.join(['Pc2.',s1PropName,'.',str(j)]))
    ls_APAAC = []
    ls_tao = []
    for i_lambda_i in range(1, i_lambda + 1):
        for j in range(len(arr_aaProp_stded)):
            ls_tempList = [arr_aaProp_stded[j][d_20AA_idx[s_1seq[k]]] * arr_aaProp_stded[j][d_20AA_idx[s_1seq[k + i_lambda_i]]] for k in
                              range(len(s_1seq) - i_lambda_i)]
            ls_tao.append(sum(ls_tempList) / (len(s_1seq) - i_lambda_i))
    d_freq_20AAs = {}
    for s_1AA in ls_20AA:
        d_freq_20AAs[s_1AA] = s_1seq.count(s_1AA)
    f_sumTau = sum(ls_tao)
    ls_APAAC.extend([float(format(d_freq_20AAs[s_1AA] / (1 + f_w * f_sumTau),'.6f')) for s_1AA in ls_20AA])
    ls_APAAC.extend([float(format(f_w * value / (1 + f_w * f_sumTau),'.6f')) for value in ls_tao])
    return ls_APAAC,ls_featElemNames
def f_APAAC_1type(p_fasta,s_posOrNeg,i_lambda,f_w):
    try:
        with open(p_fasta,'r') as f_fasta:
            ls_multiSeq_featVal = []
            for s_curLine in f_fasta.readlines():
                if s_curLine.startswith('>'):
                    pass
                else:
                    s_1seq_striped = s_curLine.strip()
                    ls_1seqAPAAC_val,ls_APAACNames = f_APAAC(s_1seq_striped,i_lambda,f_w)
                    if s_posOrNeg=="pos":
                        ls_1seqAPAAC_val.append(1)
                    else:
                        ls_1seqAPAAC_val.append(0)
                    ls_multiSeq_featVal.append(ls_1seqAPAAC_val)
    except:
        raise ErrorCoding('Cannot read the fasta file.')
    ls_APAACNames.append('class')
    arr_multiSeq_featVal = np.array(ls_multiSeq_featVal)
    return arr_multiSeq_featVal,ls_APAACNames
def f_getMaxLambdaVal(p_posFile,p_negFile):
    ls_seqLens = []
    try:
        with open(p_posFile,'r') as fid_pos:
            for s_curline in fid_pos.readlines():
                if s_curline.startswith('>'):
                    pass
                else:
                    ls_seqLens.append(len(s_curline.strip()))
        fid_pos.close()
    except:
        raise ErrorCoding('Cannot read the positive fasta sucessfully.')
    try:
        with open(p_negFile,'r') as fid_neg:
            for s_curline in fid_neg.readlines():
                if s_curline.startswith('>'):
                    pass
                else:
                    ls_seqLens.append(len(s_curline.strip()))
        fid_neg.close()
    except:
        raise ErrorCoding('Cannot read the negative fasta sucessfully.')
    i_MaxLambda = min(ls_seqLens)-1
    return i_MaxLambda
def f_APAAC_seqs_2types(p_posPth,p_negPth,i_lambda,f_w):
    i_MaxLambda = f_getMaxLambdaVal(p_posPth,p_negPth)
    if i_lambda > i_MaxLambda:
        i_lambda = i_MaxLambda
        print(''.join(['Warning: The lambda value you set was too large, and the value was adjusted to be ',str(i_MaxLambda),' in this task.']))
    else:
        pass
    arr_APAAC_pos,ls_ApaacNames = f_APAAC_1type(p_posPth,'pos',i_lambda,f_w)
    arr_APAAC_neg,ls_ApaacNames = f_APAAC_1type(p_negPth,'neg',i_lambda,f_w)
    arr_APAAC_2Types = np.vstack((arr_APAAC_pos,arr_APAAC_neg))
    df_APAAC = pd.DataFrame(arr_APAAC_2Types,columns=ls_ApaacNames)
    return df_APAAC
