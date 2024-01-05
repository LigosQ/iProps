#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 20:47:47 2023
@author: sealight
"""
import numpy as np
import pandas as pd
from f_geneFastaDict import *
import pickle
class ErrorCoding(Exception):
    pass
def f_countNum(s_minSeq, s_targetSeq):
    i_num = 0
    for c_aa in s_minSeq:
        i_num = i_num + s_targetSeq.count(c_aa)
    return i_num
def f_CTDC_1type(ls_fastaSeq, s_posOrNeg):
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
        for i_groupNum in range(1,len(ls_propGroups)+1):
            ls_colNames.append(''.join([s_propName,'.G',str(i_groupNum)]))
    ls_colNames.append('class')
    ls_comp_all = []
    for s_1seq in ls_fastaSeq:
        ls_comp_1seq = []
        for s_propName in tup_property:
            f_comp_group1 = f_countNum(d_propGroup1[s_propName],s_1seq)/len(s_1seq)
            f_comp_group2 = f_countNum(d_propGroup2[s_propName],s_1seq)/len(s_1seq)
            f_comp_group3 = 1 - f_comp_group1 - f_comp_group2
            ls_comp_1seq = ls_comp_1seq + [round(f_comp_group1,4),round(f_comp_group2,4),round(f_comp_group3,4)]
        if s_posOrNeg.lower()=='pos':
            ls_comp_1seq.append(1)
        elif s_posOrNeg.lower()=='neg':
            ls_comp_1seq.append(0)
        else:
            raise ErrorCoding('Your given pos/neg is wrong. Only "pos"/"neg" is supportted.')
        ls_comp_all.append(ls_comp_1seq)
    arr_feats = np.array(ls_comp_all)
    return np.array(ls_colNames), arr_feats
def f_CTDC_in2types(d_seqs_in2types):
    ls_colnames_pos, arr_feats_pos = f_CTDC_1type(d_seqs_in2types['pos'],'pos')
    ls_colNames_neg, arr_feats_neg = f_CTDC_1type(d_seqs_in2types['neg'],'neg')
    if (ls_colnames_pos == ls_colNames_neg).all():
        arr_feats_2types = np.vstack((arr_feats_pos, arr_feats_neg))
        df_feats_2types = pd.DataFrame(arr_feats_2types, columns=ls_colnames_pos)
    else:
        raise ErrorCoding('The column name lists are different. Please check your CTDC codes...')
    return df_feats_2types
