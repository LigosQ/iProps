#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 16:07:45 2023
@author: sealight
"""
import numpy as np
import pandas as pd
from files import globSet
from collections import Counter
from files.geneSmartPth import geneSmartPth_fromRoot,geneSmartPth
def f_chgStr2Dict(s_line_i):
    d_curRedSchm = dict()
    s_line_temp_i = s_line_i.strip()
    ls_subGrpList = s_line_temp_i.split('#')
    for s_subGrp in ls_subGrpList:
        for s_1AA in s_subGrp:
            d_curRedSchm[s_1AA] = s_subGrp[0]
    return d_curRedSchm
def f_tranTxt2Dict_pkl(s_groupPkl):
    import pickle
    d_allSchm = dict()
    i_schmNo = 0
    try:
        with open(s_groupPkl,'rb') as fid_schmPkl:
            s_allSchmLines = pickle.load(fid_schmPkl)
    except:
        raise ErrorCoding('Error: the code cannot open the group scheme pkl file.')
    ls_allGrpSchmStr = s_allSchmLines.split('\n')
    for i,s_schmStr_i in enumerate(ls_allGrpSchmStr):
        i_schmNo += 1
        d_schm_i = dict()
        s_line_strip = s_schmStr_i.strip()
        ls_subSchm = s_line_strip.split('#')
        if ls_subSchm[0]=='':
            ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
            d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
            d_schm_i = d_origAmAcid_2RedStr
        else:
            d_schm_i = f_chgStr2Dict(s_line_strip)
        d_allSchm[str(''.join(['redSchm_',str(i_schmNo)]))] = d_schm_i
    return d_allSchm
def f_pkl2RedSchmDict():
    s_redPklPth = geneSmartPth('data','groupSchms.pkl')
    d_568RedSchm = f_tranTxt2Dict_pkl(s_redPklPth)
    return d_568RedSchm
class ErrorCoding(Exception):
    pass
def f_modSchmDictEq20(d_redSchm, ls_origAAs):
    d_dictKeys = d_redSchm.keys()
    for i,s1AA in enumerate(ls_origAAs):
        if s1AA in d_dictKeys:
            pass
        else:
            d_redSchm[s1AA] = s1AA
    return d_redSchm
def f_repairCounterRslt(d_counterRslt,ls_origAAs):
    d_dictKeys = d_counterRslt.keys()
    for i,s1AA in enumerate(ls_origAAs):
        if s1AA in d_dictKeys:
            pass
        else:
            d_counterRslt[s1AA] = 0
    return d_counterRslt
def f_EAAC_1seq_1Schm(s_seq,d_Dict_i,s_dictName):
    ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    d_groupDict_i = f_modSchmDictEq20(d_Dict_i,ls_origAmAcid)
    ls_redAAs = []
    for s_origAA,s_redAA in d_groupDict_i.items():
        ls_redAAs.append(s_redAA)
    ls_redKeys = list(set(ls_redAAs))
    ls_redKeys.sort()
    d_counterRslt = Counter(s_seq)
    d_freqInOrigSeq = f_repairCounterRslt(d_counterRslt,ls_origAmAcid)
    n_seqLength = len(s_seq)
    if len(ls_redKeys)==20:
        ls_featVal = [float(format(d_freqInOrigSeq[s1AA]/n_seqLength,'.4f')) for i,s1AA in enumerate(ls_origAmAcid)]
        ls_featColName = [''.join([s_dictName,'_', item]) for i,item in enumerate(ls_origAmAcid)]
        return ls_featVal,ls_featColName
    else:
        pass
    ls_freqTemp = [0 for item in ls_redKeys]
    d_redAAFreq = dict(zip(ls_redKeys,ls_freqTemp))
    for i,s_origAA in enumerate(ls_origAmAcid):
        i_oldFreq = d_redAAFreq[d_groupDict_i[s_origAA]]
        d_redAAFreq[d_groupDict_i[s_origAA]]=i_oldFreq+d_freqInOrigSeq[s_origAA]
    ls_featVal = [float(format(d_redAAFreq[s1AA]/n_seqLength,'.4f')) for i,s1AA in enumerate(ls_redKeys)]
    ls_featColName = [''.join([s_dictName,'_', s1AA]) for i,s1AA in enumerate(ls_redKeys)]
    return ls_featVal,ls_featColName
def f_EAAC_1seq_schms(s_1seq):
    d_reversDict569 = f_pkl2RedSchmDict()
    ls_all569_Names = []
    ls_all569FeatValue = []
    for key,d_schm_i in d_reversDict569.items():
        ls_featVal_i,ls_colName_i = f_EAAC_1seq_1Schm(s_1seq,d_schm_i,key)
        ls_all569_Names.extend(ls_colName_i)
        ls_all569FeatValue.extend(ls_featVal_i)
    return ls_all569FeatValue,ls_all569_Names
def f_EAAC_seqs_1type(p_fastaPth,s_posOrNeg):
    try:
        with open(p_fastaPth,'r') as f_fasta:
            ls_multiSeq_featVal = []
            for s_curLine in f_fasta.readlines():
                if s_curLine.startswith('>'):
                    pass
                else:
                    s_1seq_striped = s_curLine.strip()
                    ls_1seqEaac_val,ls_eaacFeatNames = f_EAAC_1seq_schms(s_1seq_striped)
                    if s_posOrNeg=="pos":
                        ls_1seqEaac_val.append(1)
                    else:
                        ls_1seqEaac_val.append(0)
                    ls_multiSeq_featVal.append(ls_1seqEaac_val)
    except:
        raise ErrorCoding('Cannot read the fasta file.')
    ls_eaacFeatNames.append('class')
    arr_multiSeq_featVal = np.array(ls_multiSeq_featVal)
    return arr_multiSeq_featVal,ls_eaacFeatNames
def f_EAAC_seqs_posAdNeg(p_posPth,p_negPth):
    arr_eaacFeat_pos,ls_eaacFeatNames = f_EAAC_seqs_1type(p_posPth,'pos')
    arr_eaacFeat_neg,ls_eaacFeatNames = f_EAAC_seqs_1type(p_negPth,'neg')
    arr_eaac_2Types = np.vstack((arr_eaacFeat_pos,arr_eaacFeat_neg))
    df_eaac = pd.DataFrame(arr_eaac_2Types,columns=ls_eaacFeatNames)
    return df_eaac
