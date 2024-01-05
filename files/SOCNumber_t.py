#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, platform, os, re
import numpy as np
import pandas as pd
pPath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pPath)

try:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT
    from files.checkFasta import *
    from files.readFasta import *
    from files.saveCode import *
    from files import globSet
except:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
    from checkFasta import *
    from readFasta import *
    from saveCode import *
    import globSet
USAGE = """
USAGE:
    python SOCNumber.py input.fasta <nlag> <output>
    input.fasta:      the input protein sequence file in fasta format.
    nlag:             the nlag value, integer, defaule: 30
    output:           the encoding file, default: 'encodings.tsv'
"""
def SOCNumber(fastas, nlag=30, **kw):
    if minSequenceLengthWithNormalAA(fastas) < nlag + 1:
        print('Error(SOCNumber): all the sequence length should be larger than the nlag+1: ' + str(nlag + 1) + '\n\n')
        return 0
    dataFile_SW = f_geneAbsPath_frmROOT('data','Schneider-Wrede.txt')
    dataFile_G = f_geneAbsPath_frmROOT('data','Grantham.txt')
    AA = 'ACDEFGHIKLMNPQRSTVWY'
    AA1 = 'ARNDCQEGHILKMFPSTWYV'
    DictAA = {}
    for i in range(len(AA)):
        DictAA[AA[i]] = i
    DictAA1 = {}
    for i in range(len(AA1)):
        DictAA1[AA1[i]] = i
    with open(dataFile_SW) as f:
        records = f.readlines()[1:]
    AADistance = []
    for i in records:
        array = i.rstrip().split()[1:] if i.rstrip() != '' else None
        AADistance.append(array)
    AADistance = np.array(
        [float(AADistance[i][j]) for i in range(len(AADistance)) for j in range(len(AADistance[i]))]).reshape((20, 20))
    with open(dataFile_G) as f:
        records = f.readlines()[1:]
    AADistance1 = []
    for i in records:
        array = i.rstrip().split()[1:] if i.rstrip() != '' else None
        AADistance1.append(array)
    AADistance1 = np.array(
        [float(AADistance1[i][j]) for i in range(len(AADistance1)) for j in range(len(AADistance1[i]))]).reshape(
        (20, 20))
    header = ['#']
    for n in range(1, nlag + 1):
        header.append('Schneider.lag' + str(n))
    for n in range(1, nlag + 1):
        header.append('gGrantham.lag' + str(n))
    ls_mFeats = []
    for i in fastas:
        name, sequence = i[0], re.sub('-', '', i[1])
        code = [name]
        for n in range(1, nlag + 1):
            code.append(sum(
                [AADistance[DictAA[sequence[j]]][DictAA[sequence[j + n]]] ** 2 for j in range(len(sequence) - n)]) / (
                        len(sequence) - n))
        for n in range(1, nlag + 1):
            code.append(sum([AADistance1[DictAA1[sequence[j]]][DictAA1[sequence[j + n]]] ** 2 for j in
                             range(len(sequence) - n)]) / (len(sequence) - n))
        ls_mFeats.append(code)
    df_feats = pd.DataFrame(ls_mFeats,columns=header)
    status = True
    return df_feats,status
def myfun_calcSOCnumber(fastafile, nlag):
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    nlag = d_allParas['socnumber']
    fastas = readFasta(fastafile)
    status = False
    df_feats,status = SOCNumber(fastas, nlag)
    return df_feats,status