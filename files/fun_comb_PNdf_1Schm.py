#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 10:49:09 2022
@author: sealight
"""
from files.class_clac1Dipep_1schm import *
import pandas as pd
def f_genePosNegFeat_by1Schm(s_posPth,s_negPth,d_alphabet):
    df_final3Feats = None
    for i_dipepType in range(3):
        obj  = c_calc1Dipep_1schm(i_dipepType)
        obj.inFilePth = s_posPth
        obj.alphaBet = d_alphabet
        obj.negOrPos = 'pos'
        obj.recodeSeq(i_dipepType)
        df_dipepFeats_pos = obj.f_getDipepDf_AdCsv_ofCurShm()
        obj.inFilePth = s_negPth
        obj.negOrPos = 'neg'
        obj.recodeSeq(i_dipepType)
        df_dipepFeats_neg = obj.f_getDipepDf_AdCsv_ofCurShm()
        if i_dipepType == 0:
            df_final3Feats = pd.concat([df_dipepFeats_pos,df_dipepFeats_neg],axis=0,join='inner')
        else:
            df_curDipepType = pd.concat([df_dipepFeats_pos,df_dipepFeats_neg],axis=0,join='inner')
            df_curDipepType_noCls = df_curDipepType.drop(columns=['class'])
            df_final3Feats = df_final3Feats.reset_index(drop= True)
            df_curDipepType_noCls = df_curDipepType_noCls.reset_index(drop= True)
            df_final3Feats = pd.concat([df_final3Feats,df_curDipepType_noCls],axis=1,join='inner')
    return df_final3Feats
def f_combDipep_PosNeg_1schm(p_infile_p, p_infile_n, d_curReduceAlphabet):
    df_3dipeps = f_genePosNegFeat_by1Schm(p_infile_p, p_infile_n, d_curReduceAlphabet)
    return df_3dipeps