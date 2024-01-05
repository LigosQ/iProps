#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:26:09 2023
@author: sealight
"""
import numpy as np
import pandas as pd
from f_geneFastaDict import *
import pickle
class ErrorCoding(Exception):
    pass
def f_CTDT_1type(ls_fastaSeq, s_posOrNeg):
    s_pickFilePth = './data/redSchm3Len.pkl'
    with open(s_pickFilePth,'rb') as fid_pick:
        d_all3Len_redDict = pickle.load(fid_pick)
    d_propGroup1 = d_all3Len_redDict['group1']
    d_propGroup2 = d_all3Len_redDict['group2']
    d_propGroup3 = d_all3Len_redDict['group3']
    ls_propGroups = [d_propGroup1, d_propGroup2, d_propGroup3]
    tup_property = (
    'redSchm_2', 'redSchm_33', 'redSchm_44', 'redSchm_80', 'redSchm_105', 'redSchm_126', 
    'redSchm_149', 'redSchm_166', 'redSchm_182', 'redSchm_183', 'redSchm_189', 'redSchm_192', 
    'redSchm_194', 'redSchm_196', 'redSchm_199', 'redSchm_216', 'redSchm_234', 'redSchm_248', 
    'redSchm_262', 'redSchm_292', 'redSchm_317', 'redSchm_382', 'redSchm_400', 'redSchm_426', 
    'redSchm_442', 'redSchm_460', 'redSchm_478', 'redSchm_498', 'redSchm_499', 'redSchm_503', 
    'redSchm_520', 'redSchm_529', 'redSchm_546', 
    'hydrophobicity_PRAM900101', 'hydrophobicity_ARGP820101', 'hydrophobicity_ZIMJ680101', 'hydrophobicity_PONP930101',
    'hydrophobicity_CASG920101', 'hydrophobicity_ENGD860101', 'hydrophobicity_FASG890101', 'normwaalsvolume',
    'polarity', 'polarizability', 'charge', 'secondarystruct', 'solventaccess')
    ls_colNames = []
    for s_propName in tup_property:
        for s_tr in ['Tr1221', 'Tr1331', 'Tr2332']:
            ls_colNames.append(''.join([s_propName,'.',s_tr]))
    ls_colNames.append('class')
    ls_comp_all = []
    for s_1seq in ls_fastaSeq:
        ls_comp_1seq = []
        ls_aaPairs = [s_1seq[idx:idx+2] for idx in range(len(s_1seq)-1)]
        for s_propName in tup_property:
            i_1221, i_1331, i_2332 = 0,0,0
            for s_1aaPair in ls_aaPairs:
                if (s_1aaPair[0] in d_propGroup1[s_propName] and s_1aaPair[1] in d_propGroup2[s_propName]) or (s_1aaPair[0] in d_propGroup2[s_propName] and s_1aaPair[1] in d_propGroup1[s_propName]):
                    i_1221 = i_1221+1
                    continue
                if (s_1aaPair[0] in d_propGroup1[s_propName] and s_1aaPair[1] in d_propGroup3[s_propName]) or (s_1aaPair[0] in d_propGroup3[s_propName] and s_1aaPair[1] in d_propGroup1[s_propName]):
                    i_1331 = i_1331+1
                    continue
                if (s_1aaPair[0] in d_propGroup2[s_propName] and s_1aaPair[1] in d_propGroup3[s_propName]) or (s_1aaPair[0] in d_propGroup3[s_propName] and s_1aaPair[1] in d_propGroup2[s_propName]):
                    i_2332 = i_2332+1
            i_numOfPairs = len(ls_aaPairs)
            ls_comp_1seq.extend([round(i_1221/i_numOfPairs,4), round(i_1331/i_numOfPairs,4), round(i_2332/i_numOfPairs,4)])
        if s_posOrNeg.lower()=='pos':
            ls_comp_1seq.append(1)
        elif s_posOrNeg.lower()=='neg':
            ls_comp_1seq.append(0)
        else:
            raise ErrorCoding('Your given pos/neg is wrong. Only "pos"/"neg" is supportted.')
        ls_comp_all.append(ls_comp_1seq)
    arr_feats = np.array(ls_comp_all)
    return np.array(ls_colNames), arr_feats
def f_CTDT_in2types(d_seqs_in2types):
    ls_colnames_pos, arr_feats_pos = f_CTDT_1type(d_seqs_in2types['pos'],'pos')
    ls_colNames_neg, arr_feats_neg = f_CTDT_1type(d_seqs_in2types['neg'],'neg')
    if (ls_colnames_pos == ls_colNames_neg).all():
        arr_feats_2types = np.vstack((arr_feats_pos, arr_feats_neg))
        df_feats_2types = pd.DataFrame(arr_feats_2types, columns=ls_colnames_pos)
    else:
        raise ErrorCoding('The column name lists are different. Please check your CTDC codes...')
    return df_feats_2types
