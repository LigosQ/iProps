#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 20:19:15 2023
@author: sealight
"""
import numpy as np
import pandas as pd
from files import globSet
class ErrorCoding(Exception):
    pass
def f_chgStr2Dict(s_redSchm):
    if "#" in s_redSchm:
        ls_eachSchmGrup = s_redSchm.split('#')
        ls_20AAs = list('ACDEFGHIKLMNPQRSTVWY')
        d_20AAs_redSchm = dict(zip(ls_20AAs,ls_20AAs))
        for s_miniGrup in ls_eachSchmGrup:
            for c_eachAA in s_miniGrup:
                d_20AAs_redSchm[c_eachAA] = s_miniGrup[0]
    else:
        raise ErrorCoding('The reduce string expression should use # as the delimiter.')
    return d_20AAs_redSchm
def f_CKSAAGP_1fasta(s_1fastaSeq, d_redSchm_20AAs, d_uniqAAPairs_comp,ls_uniqAAPairs, i_gap):
    ls_rededSeq = [d_redSchm_20AAs[s_1fastaSeq[i]] for i in range(len(s_1fastaSeq))]
    i_sum =0
    for i_pre in range(len(ls_rededSeq)-i_gap-1):
        i_sum = i_sum +1 
        i_suff = i_pre+i_gap+1
        s_curPairs_inSeq = ''.join([ls_rededSeq[i_pre],ls_rededSeq[i_suff]])
        d_uniqAAPairs_comp[s_curPairs_inSeq] = d_uniqAAPairs_comp[s_curPairs_inSeq]+1
    for key,val in d_uniqAAPairs_comp.items():
        d_uniqAAPairs_comp[key] = round(val/i_sum,6)
    ls_parisCompList = []
    for s_1AAPair in ls_uniqAAPairs:
        ls_parisCompList.append(d_uniqAAPairs_comp[s_1AAPair])
    return ls_parisCompList
def f_initPairCompZero(d_uniqAAPairs):
    for key,val in d_uniqAAPairs.items():
        d_uniqAAPairs[key] = 0
    return d_uniqAAPairs
def f_CKSAAGP_1type(ls_fastaSeqs, redSchm, i_gap, s_posOrNeg):
    if isinstance(redSchm, dict):
        d_redSchm_20AAs = redSchm
    elif isinstance(redSchm, str):
        d_redSchm_20AAs = f_chgStr2Dict(redSchm)
    else:
        raise ErrorCoding('The second parameter only support string or dictionary type.')
    ls_AAs_repeat = []
    for key,val in d_redSchm_20AAs.items():
        ls_AAs_repeat.append(val)
    ls_uniqAAs = list(set(ls_AAs_repeat))
    ls_uniqAAPairs = []
    d_uniqAAPairs_comp = dict()
    for c_preAA in ls_uniqAAs:
        for c_suffAA in ls_uniqAAs:
            s_curAAPair = ''.join([c_preAA,c_suffAA])
            d_uniqAAPairs_comp[s_curAAPair] = 0
            ls_uniqAAPairs.append(s_curAAPair)
    ls_dipepComp_1type = []
    for s_1fastaSeq in ls_fastaSeqs:
        d_uniqAAPairs_comp = f_initPairCompZero(d_uniqAAPairs_comp)
        ls_dipepComp_1Seq = f_CKSAAGP_1fasta(s_1fastaSeq, d_redSchm_20AAs, d_uniqAAPairs_comp,ls_uniqAAPairs, i_gap)
        if s_posOrNeg.lower()=='pos':
            ls_dipepComp_1Seq.append(1)
        elif s_posOrNeg.lower()=='neg':
            ls_dipepComp_1Seq.append(0)
        else:
            raise ErrorCoding('The 4th parameter is wrong. Only "pos"/"neg" is supportted.')
        ls_dipepComp_1type.append(ls_dipepComp_1Seq)
    ##transform the list type to the nd.array format
    arr_dipepComp_1type = np.array(ls_dipepComp_1type)
    ls_uniqAAPairs.append('class')
    return np.array(ls_uniqAAPairs), arr_dipepComp_1type
def f_CKSAAGP_in2types(d_seqs_in2types,redSchm,i_gap):
    if i_gap < (globSet.getMinSeqLen()-2):
        pass
    else:
        raise ErrorCoding(''.join(['The third parameter should be less then the minimum length:',str(globSet.getMinSeqLen()-2)]))
    ls_colnames_pos, arr_feats_pos = f_CKSAAGP_1type(d_seqs_in2types['pos'],redSchm, i_gap,'pos')
    ls_colNames_neg, arr_feats_neg = f_CKSAAGP_1type(d_seqs_in2types['neg'],redSchm, i_gap,'neg')
    if (ls_colnames_pos == ls_colNames_neg).all():
        arr_feats_2types = np.vstack((arr_feats_pos, arr_feats_neg))
        df_feats_2types = pd.DataFrame(arr_feats_2types, columns=ls_colnames_pos)
    else:
        raise ErrorCoding('The column name lists are different. Please check your codes...')
    return df_feats_2types
