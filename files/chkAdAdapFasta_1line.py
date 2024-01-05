#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 16:41:16 2021
@author: tafch
"""
from files.class_putFastaSeqInOneline import *
class ErrorUser(Exception):
    pass
def fun_checkNormState(fastapth):
    normStat = True
    fid = open(fastapth,'r')
    lineNo = 0
    for curline in fid.readlines():
        if curline.endswith('\n'):
            s_curLine_t = curline.strip()
            lineNo  += 1
        if int(lineNo%2)==1:
            if curline.startswith('>'):
                normStat = True
            else:
                normStat = False
                return normStat
        else:
            if curline.startswith('>'):
                normStat = False
                return normStat
            else:
                normStat = True
    fid.close()
    return normStat
def fun_checkAdAdaptSeqInOneLine(fastapth):
    if fun_checkNormState(fastapth):
        pass
    else:
        fastaObj = putFastaSeqInOneline()
        fastaObj.inputFastaFile = fastapth
        fastaObj.dealWithBadFile()
        pathSplitList = fastapth.split('.')
        if pathSplitList[-1]=='fasta':
            pathSplitList[-2] = pathSplitList[-2]+'_OneLineSeq'
            fastapth = '.'.join(pathSplitList)
        if fun_checkNormState(fastapth):
            raise ErrorUser('The fasta file is not in the normilized format, please check...')
    return fastapth