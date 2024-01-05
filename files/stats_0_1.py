#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 05:41:29 2023
@author: sealight
"""
import csv
class ErrorCoding(Exception):
    pass
def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('class') for buf in buf_gen)
def f_stats01(p_csvFile):
    if p_csvFile.endswith('.csv'):
        pass
    else:
        raise ErrorCoding('Error: You set a different file format, the current version only supports csv format')
    if iter_count(p_csvFile) == 0:
        raise ErrorCoding('''The column/feature name for the instance type column 
                           should be "class". Other names are not supported yet. 
                           After checking that the data you provided does not 
                           have class column, please check your csv data''')
    ls_y = []
    global i_colNum 
    i_colNum = 0
    with open(p_csvFile,'r') as f_csv:
        reader = csv.DictReader(f_csv)
        for count,row in enumerate(reader):
            ls_y.append(row['class'])
            if count==0:
                i_colNum = len(row)
    i_num_0 = 0
    i_num_1 = 1
    for i,s_val in enumerate(ls_y):
        try:
            i_num_i_inY = float(s_val)
            if i_num_i_inY == 0:
                i_num_0 += 1
            elif i_num_i_inY == 1:
                i_num_1 += 1
        except:
            pass
    return i_num_0,i_num_1,i_colNum