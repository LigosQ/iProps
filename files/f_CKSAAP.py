#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:48:14 2023
@author: sealight
"""
"""
Created on Thu Jun 15 20:19:15 2023
@author: sealight
"""
import numpy as np
import pandas as pd
from f_geneFastaDict import *
from files import globSet
class ErrorCoding(Exception):
    pass
def f_CKSAAP_1fasta(s_1fastaSeq, d_uniqAAPairs_comp,ls_uniqAAPairs, i_gap):
    ls_rededSeq = s_1fastaSeq
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
    ls_colNames = [''.join([s_1AApair,'.G',str(i_gap)]) for s_1AApair in ls_uniqAAPairs]
    return ls_parisCompList,ls_colNames
def f_initPairCompZero(d_uniqAAPairs):
    for key,val in d_uniqAAPairs.items():
        d_uniqAAPairs[key] = 0
    return d_uniqAAPairs
def f_CKSAAP_1type(ls_fastaSeqs, i_gap, s_posOrNeg):
    ls_uniqAAs = list('ACDEFGHIKLMNPQRSTVWY')
    d_uniqAAPairs_comp = dict()
    ls_uniqAAPairs = []
    for c_preAA in ls_uniqAAs:
        for c_suffAA in ls_uniqAAs:
            s_curAAPair = ''.join([c_preAA,c_suffAA])
            d_uniqAAPairs_comp[s_curAAPair] = 0
            ls_uniqAAPairs.append(s_curAAPair)
    ls_dipepComp_1type = []
    ls_colNames_mGaps = []
    i_counter_seq = 0
    for s_1fastaSeq in ls_fastaSeqs:
        i_counter_seq = i_counter_seq+1
        d_uniqAAPairs_comp = f_initPairCompZero(d_uniqAAPairs_comp)
        ls_1seqComp_mGap = []
        for i_gap in range(i_gap+1):
            ls_dipepComp_1Seq, ls_colnames_gap_i = f_CKSAAP_1fasta(s_1fastaSeq, d_uniqAAPairs_comp,ls_uniqAAPairs, i_gap)
            ls_1seqComp_mGap.extend(ls_dipepComp_1Seq)
            if i_counter_seq == 1:
                ls_colNames_mGaps.extend(ls_colnames_gap_i)
        if s_posOrNeg.lower()=='pos':
            ls_1seqComp_mGap.append(1)
        elif s_posOrNeg.lower()=='neg':
            ls_1seqComp_mGap.append(0)
        else:
            raise ErrorCoding('The 4th parameter is wrong. Only "pos"/"neg" is supportted.')
        ls_dipepComp_1type.append(ls_1seqComp_mGap)
    arr_dipepComp_1type = np.array(ls_dipepComp_1type)
    ls_colNames_mGaps.append('class')
    return np.array(ls_colNames_mGaps), arr_dipepComp_1type
def f_CKSAAP_in2types(d_seqs_in2types,i_gap):
    if i_gap < (globSet.getMinSeqLen()-2):
        pass
    else:
        raise ErrorCoding(''.join(['The third parameter should be less then the minimum length:',str(globSet.getMinSeqLen()-2)]))
    ls_colnames_pos, arr_feats_pos = f_CKSAAP_1type(d_seqs_in2types['pos'],i_gap,'pos')
    ls_colNames_neg, arr_feats_neg = f_CKSAAP_1type(d_seqs_in2types['neg'],i_gap,'neg')
    if (ls_colnames_pos == ls_colNames_neg).all():
        arr_feats_2types = np.vstack((arr_feats_pos, arr_feats_neg))
        df_feats_2types = pd.DataFrame(arr_feats_2types, columns=ls_colnames_pos)
    else:
        raise ErrorCoding('The column name lists are different. Please check your CTDC codes...')
    return df_feats_2types
