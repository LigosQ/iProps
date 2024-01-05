#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 17:42:19 2023
@author: sealight
"""
import csv
import pandas as pd
class ErrorCoding(Exception):
    pass
def f_isContainClass(ls_colNames):
    b_isContain = False
    s_clsColName = ''
    for item in ls_colNames:
        if item.lower()=='class':
            b_isContain = True
            s_clsColName = item
            break
        else:
            pass
    if b_isContain:
        return True,s_clsColName
    else:
        return False,s_clsColName
def writeDf2csv(dfData, csvpath):
    columnNameList= dfData.columns.values.tolist()
    b_isContain,s_colName = f_isContainClass(columnNameList)
    if b_isContain:
        dfData.to_csv(csvpath, index=False)
    else:
        raise ErrorCoding('The csv file should set the type column name as "class",\
                          other name is not supported now.')