#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 17:03:09 2020
@author: tafch
"""
import sys, os, re
import numpy as np
import pandas as pd
pPath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pPath)
try:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
    from checkFasta import *
    from readFasta import *
except:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT
    from files.checkFasta import *
    from files.readFasta import *
from files import globSet
def Moran(fastas, props=['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102',
                         'CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201'],
                nlag = 30, **kw):
    if minSequenceLengthWithNormalAA(fastas) < nlag + 1:        
        print('Error: all the sequence length should be larger than the nlag+1: ' + str(nlag + 1) + '\n\n')
        print('The Moran feature will not be used as a candidate feature in this operation.\n')
        print('You should set an appropriate nlag value for the next calculation\n')
        return 0
    AA = 'ARNDCQEGHILKMFPSTWYV'
    fileAAidx = f_geneAbsPath_frmROOT('data','AAidx.txt')
    with open(fileAAidx) as f:
        records = f.readlines()[1:]
    myDict = {}
    for i in records:
        array = i.rstrip().split('\t')
        myDict[array[0]] = array[1:]
    AAidx = []
    AAidxName = []
    for i in props:
        if i in myDict:
            AAidx.append(myDict[i])
            AAidxName.append(i)
        else:
            print('"' + i + '" properties not exist.')
            return None
    AAidx1 = np.array([float(j) for i in AAidx for j in i])
    AAidx = AAidx1.reshape((len(AAidx), 20))
    propMean = np.mean(AAidx,axis=1)
    propStd = np.std(AAidx, axis=1)
    for i in range(len(AAidx)):
        for j in range(len(AAidx[i])):
            AAidx[i][j] = (AAidx[i][j] - propMean[i]) / propStd[i]
    index = {}
    for i in range(len(AA)):
        index[AA[i]] = i
    header = ['#']
    for p in props:
        for n in range(1, nlag+1):
            header.append(p + '.lag' + str(n))
    ls_mFeats = []
    for i in fastas:
        name, sequence = i[0], re.sub('-', '', i[1])
        code = [name]
        N = len(sequence)
        for prop in range(len(props)):
            xmean = sum([AAidx[prop][index[aa]] for aa in sequence]) / N
            for n in range(1, nlag + 1):
                if len(sequence) > nlag:
                    fenzi = sum([(AAidx[prop][index.get(sequence[j], 0)] - xmean) * (AAidx[prop][index.get(sequence[j + n], 0)] - xmean) for j in range(len(sequence) - n)]) / (N - n)
                    fenmu = sum([(AAidx[prop][index.get(sequence[j], 0)] - xmean) ** 2 for j in range(len(sequence))]) / N
                    rn = fenzi / fenmu
                else:
                    rn = 'NA'
                code.append(rn)
        ls_mFeats.append(code)
    try:
        df_feats = pd.DataFrame(ls_mFeats, columns=header)
    except:
        return ls_mFeats,False
    return df_feats,True
def Moran_initSet_Calc1(file,nlag):
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    nlag = d_allParas['Moran']
    fastas = readFasta(file)
    props = ['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102','CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201']
    df_feats,b_status = Moran(fastas, props, nlag)
    return df_feats,b_status
    