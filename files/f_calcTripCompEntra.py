#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 21:14:20 2023
@author: sealight
"""
from files.class_clacTrip_1Schm import c_1schmRedSeq_calc1Tripes
from files import globSet
from files.geneSmartPth import geneSmartPth
import pandas as pd
class ErrorCoding(Exception):
    pass
def f_getRedDict():
    var_redDict = globSet.getReduceSchm()
    if var_redDict is None:
        p_redSchmTxt = geneSmartPth('data','groupSchms.pkl')
        globSet._init()
        globSet.setRedSchmIsFull(p_redSchmTxt)
        d_redSchmFull = globSet.getReduceSchm()
    else:
        if isinstance(var_redDict, dict):
            d_redSchmFull = globSet.getReduceSchm()
        else:
            p_redSchmTxt = geneSmartPth('data','groupSchms.pkl')
            globSet._init()
            globSet.setRedSchmIsFull(p_redSchmTxt)
            d_redSchmFull = globSet.getReduceSchm()
    return d_redSchmFull
def f_getCurRedDict(i_schmNo):
    d_redSchmFull = f_getRedDict()
    d_curSchm_i = d_redSchmFull[str(i_schmNo)]
    return d_curSchm_i
def f_redsimpDict2Str(i_schmNo):
    d_simpDict = f_getCurRedDict(i_schmNo)
    ls_groupAAs = []
    for key,val in d_simpDict.items():
        ls_groupAAs.append(val)
    s_groupdDict = '#'.join(ls_groupAAs)
    return s_groupdDict
def f_geneTripep_P_N(pospth,negpth,d_redSchm_i,i_tripTypeNo):
    obj_trip_pos = c_1schmRedSeq_calc1Tripes(pospth,d_redSchm_i,'pos',i_tripTypeNo)
    df_trip_pos=obj_trip_pos.f_geneTripFeat_curSchm()
    obj_trip_neg = c_1schmRedSeq_calc1Tripes(negpth,d_redSchm_i,'neg',i_tripTypeNo)
    df_trip_neg=obj_trip_neg.f_geneTripFeat_curSchm()
    if df_trip_pos.columns.values.tolist() == df_trip_neg.columns.values.tolist():
        df_trip_p_n = pd.concat([df_trip_pos,df_trip_neg])
    return df_trip_p_n
def f_clacTriDf_P_N(pospth,negpth,i_schmNo,i_tripTypeNo):
    d_redSchm_i = f_getCurRedDict(i_schmNo)
    df_trip_p_n = f_geneTripep_P_N(pospth,negpth,d_redSchm_i,i_tripTypeNo)
    return df_trip_p_n
