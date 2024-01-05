#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:14:36 2023
@author: sealight
"""
import re
import math
class ErrorCoding(Exception):
    pass
def f_calcDc(s_1seq, d_Dc):
    for s_key,i_freqVal in d_Dc.items():
        d_Dc[s_key] = 0
    i_mLength = len(s_1seq)-1
    for i in range(i_mLength):
        s_dipep = ''.join([s_1seq[i], s_1seq[i+1]])
        d_Dc[s_dipep] = d_Dc[s_dipep] + 1
    for s_key,i_freqVal in d_Dc.items():
        d_Dc[s_key] = (d_Dc[s_key]/i_mLength)
    return d_Dc
def f_calcTm(d_allCodons, d_Tm):
    for s_key,i_freqVal in d_Tm.items():
        d_Tm[s_key] = 0
    for s_key,i_freqVal in d_Tm.items():
        d_Tm[s_key] = (d_allCodons[s_key[0]]/61)*(d_allCodons[s_key[1]]/61)
    return d_Tm
def f_calcTv(d_Tm, d_Tv, i_length):
    for s_key, f_val in d_Tv.items():
        d_Tv[s_key] = 0
    for s_key, f_val in d_Tv.items():
        d_Tv[s_key] = (d_Tm[s_key]*(1-d_Tm[s_key]))/(i_length-1)
    return d_Tv
def f_DDE(s_1seq, d_Dc, d_Tm, d_Tv, d_allCodons, d_DDE):
    d_Dc = f_calcDc(s_1seq, d_Dc)
    d_Tm = f_calcTm(d_allCodons, d_Tm)
    d_Tv = f_calcTv(d_Tm, d_Tv, len(s_1seq))
    for s_key, f_val in d_DDE.items():
        d_DDE[s_key] = 0
    for s_key, f_val in d_DDE.items():
        f_val = d_Tv[s_key]
        if f_val == 0:
            f_delta = 1e-5
            d_DDE[s_key] = round((d_Dc[s_key] - d_Tm[s_key])/math.sqrt(f_val+f_delta),6)
        else:
            d_DDE[s_key] = round((d_Dc[s_key] - d_Tm[s_key])/math.sqrt(f_val),6)
    return d_DDE