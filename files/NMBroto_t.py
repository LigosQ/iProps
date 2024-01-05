#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
import numpy as np
import pandas as pd
pPath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pPath)
try:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT
    from files import globSet
    from files import checkFasta
    from files import readFasta
    from files import saveCode
except:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
    import globSet
    import checkFasta
    import readFasta
    import saveCode
def NMBroto(fastas, props=['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102',
                                         'CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201'],
                nlag = 30, **kw):
    if checkFasta.minSequenceLengthWithNormalAA(fastas) < nlag + 1:
        print('Error(NMBroto): all the sequence length should be larger than the nlag+1: ' + str(nlag + 1) + '\n\n')
        print('The NMBroto feature will not be used as a candidate feature in this operation.\n')
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
    AAidx = AAidx1.reshape((len(AAidx),20))
    pstd = np.std(AAidx, axis=1)
    pmean = np.average(AAidx, axis=1)
    for i in range(len(AAidx)):
        for j in range(len(AAidx[i])):
            AAidx[i][j] = (AAidx[i][j] - pmean[i]) / pstd[i]
    index = {}
    for i in range(len(AA)):
        index[AA[i]] = i
    status = False
    header = ["#"]
    for p in props:
        for n in range(1, nlag + 1):
            header.append(p + '.lag' + str(n))
    ls_mFeats = []
    for i in fastas:
        name, sequence = i[0], re.sub('-', '', i[1])
        code = [name]
        N = len(sequence)
        for prop in range(len(props)):
            for n in range(1, nlag + 1):
                if len(sequence) > nlag:
                    rn = sum([AAidx[prop][index.get(sequence[j], 0)] * AAidx[prop][index.get(sequence[j + n], 0)] for j in range(len(sequence)-n)]) / (N - n)
                else:
                    rn = 'NA'
                code.append(rn)
        ls_mFeats.append(code)    
    df_feats = pd.DataFrame(ls_mFeats,columns = header)
    status = True
    return df_feats,status
def myFun_calcNmbroto(file,nlag):
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    nlag = d_allParas['numbroto']
    fastas = readFasta.readFasta(file)
    props = ['CIDH920105', 'BHAR880101', 'CHAM820101', 'CHAM820102','CHOC760101', 'BIGC670101', 'CHAM810101', 'DAYM780201']
    status = False
    df_data,status = NMBroto(fastas, props, nlag)
    return df_data,status