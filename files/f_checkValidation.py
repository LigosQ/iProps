#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 23:06:29 2022
@author: sealight
"""
import os
import pandas as pd
class Error_P(Exception):
    pass
def f_isUsefulFasta(p_fastaPth, s_posOrNeg):
    s_status = ''
    if p_fastaPth is None:
        if s_posOrNeg == 'pos':
            s_status = 'p_nS'
            return s_status
        elif s_posOrNeg=='neg':
            s_status = 'n_nS'
            return s_status
    if os.path.exists(p_fastaPth):
        if p_fastaPth.split('.')[-1]=='fasta':
            s_status = 'ok'
        else:
            if s_posOrNeg == 'pos':
                s_status = 'p_not_fasta'
            else:
                s_status = 'n_not_fasta'   
    else:
        if s_posOrNeg == 'pos':
            s_status = 'p_nE'
        elif s_posOrNeg=='neg':
            s_status = 'n_nE'
    return s_status
def f_isUsefulSampMethod(s_sendedMethod):
    s_status = ''
    if s_sendedMethod is None:
        s_status = 'n_Samp'
    else:
        s_status = 'ok'
    return s_status
def f_isClickedClassifier(s_clickedClassfier):
    s_status = ''
    if s_clickedClassfier is None:
        s_status = 'n_classfier'
    else:
        s_status = 'ok'
    return s_status
def f_isClickProps(s_sendedProps, p_userCsv):
    s_status = ''
    if s_sendedProps == '':
        s_status = 'n_prop'
    else:
        if 'userGivenFeat' in s_sendedProps:
            s_csvStatus = f_isValidCsvFile(p_userCsv)
            if s_csvStatus == 'ok':
                s_status = 'ok'
            else:
                s_status = s_csvStatus
        else:
            s_status = 'ok'
    return s_status
def f_isChoseFeatNum(para_featNum):
    s_status = ''
    if para_featNum == None:
        s_status = 'n_featNum'
    else:
        if isinstance(para_featNum, int):
            if para_featNum in [1,2,3,4]:
                s_status = 'ok'
            else:
                s_status = 'n_featNum'
    if s_status == '':
        return 'n_featNum'
    else:
        return s_status
def f_isValidCsvFile(para_csvFilePth):
    s_status = ''
    if para_csvFilePth == 'nk':
        s_status = 'userGivenFeat'
    else:
        if os.path.exists(para_csvFilePth):
            try:
                df_csvData = pd.read_csv(para_csvFilePth)
            except:
                s_status = 'userGivenFeat'
            else:
                ls_columnNames = df_csvData.columns.values.tolist()
                ls_colNames_lower = [item.lower() for item in ls_columnNames]
                if 'class' in ls_colNames_lower:
                    s_status = 'ok'
                else:
                    s_status = 'userGivenFeat1'
        else:
            s_status = 'userGivenFeat'
    return s_status
def f_checkParas(p_posfile, p_negfile, s_sampleMthd,s_classifer,s_props,para_featNum,p_usrCsv):
    d_problems = {
        'p_nS':'Not select the positive fasta file',
        'n_nS':'Not select the negative fasta file',
        'p_nE':'Positive fasta file doesn\'t exist',
        'n_nE':'Negative fasta file doesn\'t exist',
        'p_not_fasta':'Pos-file is not a fasta file',
        'n_not_fasta':'Neg-file is not a fasta file',
        'n_Samp':'Not choose the resampling method',
        'n_classfier':'Not choose the embedded classifier',
        'n_prop':'Not choose the perperty',
        'n_featNum':'Not choose the feature number',
        'userGivenFeat':'The path of your csv file is wrong(set up by paraSetting.py)',
        'userGivenFeat1':'Type should be lablled as class in the csv column'
    }
    ls_status = []
    ls_status.append(f_isUsefulFasta(p_posfile,'pos'))
    ls_status.append(f_isUsefulFasta(p_negfile,'neg'))
    ls_status.append(f_isUsefulSampMethod(s_sampleMthd))
    ls_status.append(f_isClickedClassifier(s_classifer))
    ls_status.append(f_isClickProps(s_props,p_usrCsv))
    ls_status.append(f_isChoseFeatNum(para_featNum))
    ls_forGeneStr = ["Error: "]
    for i in range(len(ls_status)):
        s_status_i = ls_status[i]
        if s_status_i == 'ok':
            pass
        else:
            ls_forGeneStr.append(d_problems[s_status_i])
    if len(ls_forGeneStr)==1:
        s_problemStr = ''
    else:
        s_problemStr = '\r\n'.join(ls_forGeneStr)
    return s_problemStr