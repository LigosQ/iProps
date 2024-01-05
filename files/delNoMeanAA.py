#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:43:38 2021
@author: tafch
"""
import os
class ErrorUser(object):
    pass
def genePthForProcedFile(pth):
    parentPth,filename = os.path.split(os.path.abspath(pth))
    filenameList = filename.split('.')
    filenameList[0] += '_delOtherAA'
    newFileName = '.'.join(filenameList)
    newFullPth = os.path.join(parentPth,newFileName)
    str_newFullPth = str(newFullPth)
    return str_newFullPth
def delNoMeanAA_mainFun(fastaPth):
    common20AA = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    newFastaPth_delOthAA =genePthForProcedFile(fastaPth)
    fid_r = open(fastaPth,'r')
    fid_w = open(newFastaPth_delOthAA,'w+')
    numSeqDeleted = 0
    for line in fid_r.readlines():
        curLine = line.strip()
        if curLine.startswith('>'):
            curLine.strip('\n')
            curLine.strip('\r')
            dealedTwoLines = ''
            dealedTwoLines += curLine
            dealedTwoLines += '\n'
        else:
            set_curLine = set(curLine)
            isHasOtherAA = False
            for elem in set_curLine:
                if elem in common20AA:
                    pass
                else:
                    if isHasOtherAA==False:
                        isHasOtherAA=True
                    else:
                        pass
            if isHasOtherAA==False:
                dealedTwoLines += curLine
                dealedTwoLines += '\n'
                fid_w.write(dealedTwoLines)
            else:
                numSeqDeleted += 1 
    fid_r.close()
    fid_w.close()
    if numSeqDeleted>=1:
        print('Some sequences that contains meaningless AA are removed. The number'
          ' of deleted sequences is '+str(numSeqDeleted)+'\r\n')
    return newFastaPth_delOthAA
