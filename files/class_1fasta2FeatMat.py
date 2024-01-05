#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:37:23 2021
@author: tafch
"""
from files.class_1Seq2_1x188Feat import *
import numpy as np
import pandas as pd
import os
class ErrorUser(Exception):
    pass
class c_1FastaToFeatMat(object):
    def __init__(self, givenFastaPth):
        listOfSplitedPth = givenFastaPth.split('.')
        nameOfSuffix = listOfSplitedPth[-1]
        if (nameOfSuffix=='fasta') and os.path.isfile(givenFastaPth):
            self._fastaPth = givenFastaPth
        else:
            raise  ErrorUser('The infile path is error,please check and ensure it is fasta format!...')
    def f_checkFilePth(self, givenPth,s_stdSuffix):
        if os.path.isfile(givenPth):
            ls_givenPth = givenPth.split('.')
            s_suffixInPth = ls_givenPth[-1]
            if s_suffixInPth==s_stdSuffix:
                pass
            else:
                raise ErrorUser(''.join(['The given pth is not a ',s_stdSuffix,' file, please check...']))
        else:
            raise ErrorUser('Your given pth is not a file path, please check it...')
    def f_addClassColumn(self, arrData, i_lable):
        ls_arrShape = arrData.shape
        ls_classCol = [i_lable for i in range(ls_arrShape[0])]
        arr_classCol = np.array(ls_classCol)
        arr_FeatWithClassCol = np.vstack([arrData.T, arr_classCol.T]).T
        return arr_FeatWithClassCol
    def f_readFile_calcFeatDf(self):
        ls_featMat_nx188 = []
        fid_r = open(self._fastaPth, 'r')
        for line in fid_r.readlines():
            if line.startswith('>'):
                pass
            else:
                if line.endswith('\r\n'):
                    s_curSeq = line.strip('\r\n')
                elif line.endswith('\n'):
                    s_curSeq = line.strip('\n')
                else:
                    s_curSeq = line
                obj_curSeq = proteinSeq(s_curSeq)
                ls_1x188d_curSeq = obj_curSeq.f_main_gene188d()
                ls_featMat_nx188.append(ls_1x188d_curSeq)
        arr_featMat_nx188 = np.array(ls_featMat_nx188)
        ls_colNameStr = [''.join(['188Prop-', str(i)]) for i in range(188)]
        df_featMat_nx188 = pd.DataFrame(arr_featMat_nx188, columns = ls_colNameStr)
        return df_featMat_nx188
    def f_readFile_calcFeatArr(self, lable):
        ls_featMat_nx188 = []
        fid_r = open(self._fastaPth, 'r')
        for line in fid_r.readlines():
            if line.startswith('>'):
                pass
            else:
                if line.endswith('\r\n'):
                    s_curSeq = line.strip('\r\n')
                elif line.endswith('\n'):
                    s_curSeq = line.strip('\n')
                else:
                    s_curSeq = line
                obj_curSeq = proteinSeq(s_curSeq)
                ls_1x188d_curSeq = obj_curSeq.f_main_gene188d()
                ls_featMat_nx188.append(ls_1x188d_curSeq)
        arr_featMat_nx188 = np.array(ls_featMat_nx188)
        arr_featMat_withClass = self.f_addClassColumn(arr_featMat_nx188,lable)
        return arr_featMat_withClass
    def f_save188dMat2csv(self, df_featMat, givenCsvPth):
        self.f_checkFilePth(givenCsvPth,'csv')
        df_featMat.to_csv(givenCsvPth, index=False)
    def f_main(self, outputCsvPth):
        df_featMat_nx188d = self.f_readFile_calcFeatMat()
        self.f_save188dMat2csv(df_featMat_nx188d, outputCsvPth)
        return df_featMat_nx188d