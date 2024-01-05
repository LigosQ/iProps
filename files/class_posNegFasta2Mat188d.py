#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 09:05:03 2021
@author: tafch
"""
import os
import numpy as np
import pandas as pd
from files.class_1fasta2FeatMat import *
class ErrorUser(Exception):
    pass
class c_2fastaHybrid188FeatMat(object):
    def __init__(self, givenPosPth, givenNegPth):
        self._s_posPth = None
        self._s_negPth = None
        if os.path.isfile(givenPosPth):
            ls_posPth = givenPosPth.split('.')
            s_givenSffix = ls_posPth[-1]
            if s_givenSffix == 'fasta':
                self._s_posPth = givenPosPth
            else:
                raise ErrorUser('Your given positive file is not a fasta file. Please check ...')
        if os.path.isfile(givenNegPth):
            ls_negPth = givenNegPth.split('.')
            s_givenSffix = ls_negPth[-1]
            if s_givenSffix== 'fasta':
                self._s_negPth = givenNegPth
            else:
                raise ErrorUser('Your given negative file is not a fasta file. Please check ...')
    def f_geneFeatAdCombine(self):
        if self._s_posPth is None:
            raise ErrorUser('object has no attribute:_s_posPth')
        else:
            obj_posFasta = c_1FastaToFeatMat(self._s_posPth)
        if self._s_negPth is None:
            raise ErrorUser('object has no attribute:_s_negPth')
        else:
            obj_negFasta = c_1FastaToFeatMat(self._s_negPth)
        arr_posFasta = obj_posFasta.f_readFile_calcFeatArr(1)
        arr_negFasta = obj_negFasta.f_readFile_calcFeatArr(0)
        arr_posiNegFasta = np.vstack([arr_posFasta,arr_negFasta])
        ls_hybMatShape = arr_posiNegFasta.shape
        if ls_hybMatShape[1]==189:
            ls_colNameStr = [''.join(['188d_p',str(i)]) for i in range(188)]
            ls_colNameStr.append('class')
            df_hybMat_posNeg = pd.DataFrame(arr_posiNegFasta, columns=ls_colNameStr)
            return df_hybMat_posNeg
        else:
            raise ErrorUser('The hybrid matrix is wrong, the dimension of its columns are not 188. Please check...')