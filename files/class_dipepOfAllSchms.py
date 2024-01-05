# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:14:34 2021
@author: tafch
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 14:25:31 2021
@author: tafch
"""
import os
from files.class_clac1Dipep_1schm import c_calc1Dipep_1schm
from files.class_showProcessBar import c_showProcessBar
class ErrorUser(Exception):
    pass
class c_dipepOfAllSchms(object):
    def __init__(self, s_givenPosFastaPth, s_givenNegFastaPth, s_rDictStrTxtPth):
        #
        self._s_posFastaPth = None
        self._s_negFastaPth = None
        self._s_rDictTxtPth = None
        #-----------------------------------------
        fname,ext = os.path.splitext(s_givenPosFastaPth)
        if ext=='.fasta' and os.path.isfile(s_givenPosFastaPth):
            self._s_posFastaPth = s_givenPosFastaPth
        else:
            raise ErrorUser('The given positive path is not a fasta file. please check...')
        #####\\\\\\\\\\\\\\\\\\\\\\\\\\
        fname_n,ext_n = os.path.splitext(s_givenNegFastaPth)
        if ext_n=='.fasta' and os.path.isfile(s_givenNegFastaPth):
            self._s_negFastaPth = s_givenNegFastaPth
        else:
            raise ErrorUser('The given negative path is not a fasta file. please check...')
        ####-----------------------------------------
        if os.path.isfile(s_rDictStrTxtPth):
            #check if it is a txt file
            ls_rDictTxtPth = s_rDictStrTxtPth.split('.')
            if ls_rDictTxtPth[-1]=='txt':
                self._s_rDictTxtPth = s_rDictStrTxtPth
            else:
                raise ErrorUser('The given reduction file should be a txt file. Please check your given path')
        else:
            raise ErrorUser('The given para in the initialization function is not a file. please check...')
    def f_geneRedStrDict(self):
        #
        if self._s_rDictTxtPth is None:
            raise ErrorUser('The reduction scheme txt is not set right in the initialization function...')
        else:
            fid = open(self._s_rDictTxtPth,'r')
        d_reductStrDict = {}
        i_curLineNum = 0# the
        for s_iterLine in fid.readlines():
            i_curLineNum += 1
            s_curlineStr = s_iterLine
            ls_curLineSplitGroup = s_curlineStr.split('#')
            i_groupNumCurLine = len(ls_curLineSplitGroup)
            ls_labedGroupElems = ls_curLineSplitGroup
            for i_index in range(i_groupNumCurLine):
                s_curGroupAAs = ls_curLineSplitGroup[i_index]
                s_labedGroupAAs = ''.join([s_curGroupAAs[0],'-',s_curGroupAAs])
                ls_labedGroupElems[i_index] = s_labedGroupAAs
            finalStrOfCurAlpha = '#'.join(ls_labedGroupElems)
            d_reductStrDict[str(i_curLineNum)] = finalStrOfCurAlpha
        return d_reductStrDict
    def chgStr2Dic(self, dicStr):
        if isinstance(dicStr,str):
            if '-' in dicStr:
                pass
            else:
                raise ErrorUser('The given paramenter of chgStr2Dict function should contain -, your given value is wrong...')
        else:
            raise ErrorUser('The given paramenter of chgStr2Dict function should be string, your given value is wrong type...')
        _d_str2Dict = {}
        dicList = dicStr.split('#')
        for item in dicList:
            itemList = item.split('-')
            _d_str2Dict[itemList[0]] = itemList[1]
        return _d_str2Dict
    def f_genePep_2_from1Fasta(self, s_PosOrNeg, i_tripType):
        if s_PosOrNeg=='pos' or s_PosOrNeg=='neg':
            pass
        else:
            raise ErrorUser('The given parameter of f_genePep_2_from1Fasta should be pos or neg. Pos or Neg are wrong. Please check...')
        if s_PosOrNeg=='pos':
            s_readFastaPth = self._s_posFastaPth
        elif s_PosOrNeg=='neg':
            s_readFastaPth = self._s_negFastaPth
        else:
            raise ErrorUser('Only pos/neg is supported in this version. Pos or Neg are wrong')
        d_reductSchmDict = self.f_geneRedStrDict()
        i_schemesNum = len(d_reductSchmDict)
        obj_processBar = c_showProcessBar(i_schemesNum, 'prop_dipep done!') 
        for i_schm in range(i_schemesNum):
            s_curSchmStr = d_reductSchmDict[str(i_schm+1)]
            d_curSchmDict = self.chgStr2Dic(s_curSchmStr)
            if isinstance(i_tripType, int):
                pass
            else:
                raise ErrorUser('The second para of Function:f_genePep_2_from1Fasta should be int, your input is wrong...')
            obj = c_calc1Dipep_1schm(i_tripType)
            obj.inFilePth = self._s_posFastaPth
            obj.alphaBet = d_curSchmDict
            obj.negOrPos = s_PosOrNeg
            obj.recodeSeq(i_tripType)
            df_dipepCurSchm = obj.f_getDipepDf_AdCsv_ofCurShm()
            obj_processBar.show_process()
        return df_dipepCurSchm
    def f_genePep_1_from1Fasta(self, s_PosOrNeg, i_tripType):
        if s_PosOrNeg=='pos' or s_PosOrNeg=='neg':
            pass
        else:
            raise ErrorUser('The given parameter of f_genePep_1_from1Fasta should be pos or neg. Pos or Neg are wrong. Please check...')
        if s_PosOrNeg=='pos':
            s_readFastaPth = self._s_posFastaPth
        elif s_PosOrNeg=='neg':
            s_readFastaPth = self._s_negFastaPth
        else:
            raise ErrorUser('Only pos/neg is supported in this version. Pos or Neg are wrong')
        d_reductSchmDict = self.f_geneRedStrDict()
        i_schemesNum = len(d_reductSchmDict)
        obj_processBar = c_showProcessBar(i_schemesNum, 'prop_dipep done!') 
        for i_schm in range(i_schemesNum):
            s_curSchmStr = d_reductSchmDict[str(i_schm+1)]
            d_curSchmDict = self.chgStr2Dic(s_curSchmStr)
            if isinstance(i_tripType, int):
                pass
            else:
                raise ErrorUser('The second para of Function:f_genePep_1_from1Fasta should be int, your input is wrong...')
            obj = c_calc1Dipep_1schm(i_tripType)
            obj.inFilePth = self._s_posFastaPth
            obj.alphaBet = d_curSchmDict
            obj.negOrPos = s_PosOrNeg
            obj.recodeSeq(i_tripType)
            df_AAcompsCurSchm = obj.f_getFreq_rAmAcid()
            obj_processBar.show_process()
            obj = c_calc1Dipep_1schm(i_tripType)
            obj.inFilePth = self._s_posFastaPth
            obj.alphaBet = d_curSchmDict
            obj.negOrPos = s_PosOrNeg
            obj.recodeSeq(i_tripType)
            df_AAcompsCurSchm = obj.f_getFreq_rAmAcid()
            obj_processBar.show_process()
        return df_AAcompsCurSchm