#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 02:01:35 2023

@author: sealight
"""
import pickle


# s_pklName = './paras.data'
# try:
#     with open(s_pklName, 'rb') as f:
#         s_grpSchms = pickle.load(f)
#         # ls_schmStrs = s_grpSchms.split('\n')
# except:
#     raise
    
# print(s_grpSchms)


s_pklName = './redSchm3Len.pkl'
try:
    with open(s_pklName, 'rb') as f:
        s_grpSchms = pickle.load(f)
        # ls_schmStrs = s_grpSchms.split('\n')
except:
    raise
    
s_grpSchms['group1']['redSchm_292']='AY'
s_grpSchms['group2']['redSchm_292']='CFLMVWT'
s_grpSchms['group3']['redSchm_292']='DEGHKNPQRST'

try:
    with open(s_pklName, 'wb') as f:
        pickle.dump(s_grpSchms,f)
        # ls_schmStrs = s_grpSchms.split('\n')
except:
    raise