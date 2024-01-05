#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 19:59:22 2019
@author: admin
"""
import numpy as np
import pandas as pd
from files.cmdcsv2arff import *
from files.cmdNormCsv import *
class ErrorUser(Exception):
    pass
class combineNegAdPos2CSV(object):
    def __int__(self):
        self._posFile = None
        self._negFile = None
        self._combdCsv = None
        self.__combdArff = None
        self._typeNum = None
    def checkFormatIsCorrect(self, pth, fileformat):
        if isinstance(pth,str):
            infStrList = pth.split('.')
            if infStrList[-1]==fileformat:
                return True
            else:
                raise ErrorUser('The parameter in fun_comFiles() is not the path of %s file.Please check...'%(fileformat))
        elif isinstance(pth,list):
            for i in range(len(pth)):
                curFormat = pth[i].split('.')
                if curFormat[-1]!=fileformat:
                    raise ErrorUser('The parameter in fun_comFiles() is not the path of %s file.Please check...'%(fileformat))
            return True
        else:
            raise ErrorUser('Your input is not correct')
    @property
    def posFile(self):
        return self._posFile
    @posFile.setter
    def posFile(self, val):
        if self.checkFormatIsCorrect(val,'csv'):
            self._posFile = val
        else:
            raise ErrorUser('the supported format of posFile is only csv currently, please check and correct your code')
    @property
    def negFile(self):
        return self._negFile
    @negFile.setter
    def negFile(self, val):
        if self.checkFormatIsCorrect(val,'csv'):
            self._negFile = val
        else:
            raise ErrorUser('the supported format of negFile is only csv currently, please check and correct your code')
    @property
    def typeNum(self):
        return self._typeNum
    @typeNum.setter
    def typeNum(self,val):
        if isinstance(val,str):
            self._typeNum = val
        else:
            raise ErrorUser('The given typeNum value in not string type, please check and correct it...')
    def geneCmbdFilPth(self):
        posPth = self.posFile
        if isinstance(posPth,str):
            pthList = posPth.split('/')
            lenList = len(pthList)
            newPthList_csv = []
            newPthList_arff = []
            dictTypeNum = self.typeNum
            if dictTypeNum is None:
                raise ErrorUser('your feature csv attr in class_comb.. has not setted yet,please check the code and correct it...')
            else:
                finalFeatCsvNam = 'finalDepipFeat_' + dictTypeNum + '.csv'
                finalFeatArffNam = 'finalDepipFeat_' + dictTypeNum + '.arff'
            for i in range(lenList):
                if i==(lenList-1):
                    newPthList_csv.append(finalFeatCsvNam)
                    newPthList_arff.append(finalFeatArffNam)
                else:
                    newPthList_csv.append(pthList[i])
                    newPthList_arff.append(pthList[i])
            theCmbCsvPth = '/'.join(newPthList_csv)
            theCmbArffPth = '/'.join(newPthList_arff)
            self._combdCsv = theCmbCsvPth
            self.__combdArff = theCmbArffPth
        else:
            raise ErrorUser('The pos pth is not string, it cannot be processed in current version. please check and correct it..')
    def is2ColEqal(self,namelst1,nameLst2):
        len1 = len(namelst1)
        len2 = len(nameLst2)
        isEqual = False
        if len1==len2:
            for i in range(len1):
                if namelst1[i]==nameLst2[i]:
                    pass
                else:
                    raise ErrorUser('The column name at the index %d is not same in the 2 column lists, please check this prob...'%{i})
        else:
            raise ErrorUser('The length of 2 column names are not equal, please check this question')
        isEqual = True
        return isEqual
    def combine2files(self):
        df_pos = pd.read_csv(self._posFile)
        list_posColname = df_pos.columns.values.tolist()
        df_neg = pd.read_csv(self._negFile)
        list_negColname = df_neg.columns.values.tolist()
        if self.is2ColEqal(list_posColname,list_negColname):
            pd_posAdNeg = pd.concat([df_pos, df_neg],keys = df_pos.columns.values.tolist())
            return pd_posAdNeg
        else:
            raise ErrorUser('The column names do not same, please check')
