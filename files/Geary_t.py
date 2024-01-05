#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
import numpy as np
import pandas as pd
pPath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pPath)
import checkFasta
import readFasta
import saveCode
try:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
except:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT
from files import globSet
def Geary_0(fastas, props=['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102',
                         'CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201'],nlag = 30, **kw):
    if checkFasta.minSequenceLengthWithNormalAA(fastas) < nlag + 1:
        print('Error(Geary): all the sequence length should be larger than the nlag+1: ' + str(nlag + 1) + '\n\n')
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
    propMean = np.mean(AAidx, axis=1)
    propStd = np.std(AAidx, axis=1)
    for i in range(len(AAidx)):
        for j in range(len(AAidx[i])):
            AAidx[i][j] = (AAidx[i][j] - propMean[i]) / propStd[i]
    index = {}
    for i in range(len(AA)):
        index[AA[i]] = i
    encodings = []
    header = ['#']
    for p in props:
        for n in range(1, nlag+1):
            header.append(p + '.lag' + str(n))
    encodings.append(header)
    for i in fastas:
        name, sequence = i[0], re.sub('-', '', i[1])
        code = [name]
        N = len(sequence)
        for prop in range(len(props)):
            xmean = sum([AAidx[prop][index[aa]] for aa in sequence]) / N
            for n in range(1, nlag + 1):
                if len(sequence) > nlag:
                    rn = (N-1)/(2*(N-n)) * ((sum([(AAidx[prop][index.get(sequence[j], 0)] - AAidx[prop][index.get(sequence[j + n], 0)])**2 for j in range(len(sequence)-n)])) / (sum([(AAidx[prop][index.get(sequence[j], 0)] - xmean) ** 2 for j in range(len(sequence))])))
                else:
                    rn = 'NA'
                code.append(rn)
        encodings.append(code)
    status = True
    return encodings,status
def Geary(fastas, props=['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102',
                         'CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201'],nlag = 30, **kw):
    if checkFasta.minSequenceLengthWithNormalAA(fastas) < nlag + 1:
        print('Error(Geary): all the sequence length should be larger than the nlag+1: ' + str(nlag + 1) + '\n\n')
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
    propMean = np.mean(AAidx, axis=1)
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
    ls_featVecs = []
    for i in fastas:
        name, sequence = i[0], re.sub('-', '', i[1])
        code = [name]
        N = len(sequence)
        for prop in range(len(props)):
            xmean = sum([AAidx[prop][index[aa]] for aa in sequence]) / N
            for n in range(1, nlag + 1):
                if len(sequence) > nlag:
                    rn = (N-1)/(2*(N-n)) * ((sum([(AAidx[prop][index.get(sequence[j], 0)] - AAidx[prop][index.get(sequence[j + n], 0)])**2 for j in range(len(sequence)-n)])) / (sum([(AAidx[prop][index.get(sequence[j], 0)] - xmean) ** 2 for j in range(len(sequence))])))
                else:
                    rn = 'NA'
                code.append(rn)
        ls_featVecs.append(code)
    status = True
    df_geary = pd.DataFrame(ls_featVecs, columns=header)
    return df_geary,status
def myFun_calcGeary(file,nlag):
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    nlag = d_allParas['geary']
    fastas = readFasta.readFasta(file)
    props = ['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102','CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201']
    status = False
    df_feat,status = Geary(fastas, props, nlag)
    return df_feat,status