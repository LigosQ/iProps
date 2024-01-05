#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 17:17:18 2021
@author: tafch
"""
import platform
import os
import time
from files import globSet
class ErrorCoding(Exception):
    pass
def f_gene6numId():
    s_time = time.strftime("%y%m%d-%H%M%S",time.localtime())
    return s_time
def geneSmartPth(*args):
    curWorkPth_abs = os.getcwd()
    curWorkPth_abs = str(curWorkPth_abs)
    s_osInfo = platform.platform().lower()
    if "windows" in s_osInfo:
        if '\\\\' in curWorkPth_abs:
            pthList = curWorkPth_abs.split('\\\\')
            curWorkPth_proced = '/'.join(pthList)
        elif '\\' in curWorkPth_abs:
            pthList = curWorkPth_abs.split('\\')
            curWorkPth_proced = '/'.join(pthList)
        else:
            raise ErrorCoding('The current version cannot process the return path:'+curWorkPth_abs)
    elif  ("linux" in s_osInfo) or ('macos' in s_osInfo):
        curWorkPth_proced = curWorkPth_abs
    else:
        raise ErrorCoding('Your current OS is not windows or Linux, \n'
                        'this version can not support your OS...')
    if len(args)==2:
        folderName = args[0]
        fileName = args[1]
        if folderName=='':
            joinedPath = str(os.path.join(curWorkPth_proced,fileName))
        else:
            joinedPath = str(os.path.join(curWorkPth_proced,folderName,fileName))
    elif len(args)==3:
        folderName0 = args[0]
        folderName1 = args[1]
        fileName = args[2]
        if (folderName0 is None) or (folderName1 is None):
            raise ErrorCoding('The 3 parameters should not be None. Please check your input...')
        else:
            joinedPath = str(os.path.join(curWorkPth_proced,folderName0,folderName1,fileName))
    else:
        raise ErrorCoding('The function only allow 2 parameter'
                'If you want to generate a file in the current folder,'
                            'please let the first parameter be ""or \'\'')
    return joinedPath
def geneSmartPth_fromRoot(*args):
    rootPth_abs = globSet.get_rootPth()
    s_osInfo = globSet.get_pcPlatformInfo()
    if "windows" in s_osInfo:
        if '\\\\' in rootPth_abs:
            pthList = rootPth_abs.split('\\\\')
            rootPth_proced = '/'.join(pthList)
        elif '\\' in rootPth_abs:
            pthList = rootPth_abs.split('\\')
            rootPth_proced = '/'.join(pthList)
        else:
            raise ErrorCoding('The current version cannot process the return path:'+rootPth_abs)
    elif  ("linux" in s_osInfo) or ('macos' in s_osInfo):
        rootPth_proced = rootPth_abs
    else:
        raise ErrorCoding('Your current OS is not windows or Linux, \n'
                        'this version can not support your OS...')
    if len(args)==2:
        folderName = args[0]
        fileName = args[1]
        if folderName=='':
            joinedPath = str(os.path.join(rootPth_proced,fileName))
        else:
            joinedPath = str(os.path.join(rootPth_proced,folderName,fileName))
    elif len(args)==3:
        folderName0 = args[0]
        folderName1 = args[1]
        fileName = args[2]
        if (folderName0 is None) or (folderName1 is None):
            raise ErrorCoding('The 3 parameters should not be None. Please check your input...')
        else:
            joinedPath = str(os.path.join(rootPth_proced,folderName0,folderName1,fileName))
    elif len(args)==4:
        folderName0 = args[0]
        folderName1 = args[1]
        folderName2 = args[2]
        fileName = args[3]
        if (folderName0 is None) or (folderName1 is None) or (folderName2 is None):
            raise ErrorCoding('The 3 parameters should not be None. Please check your input...')
        else:
            joinedPath = str(os.path.join(rootPth_proced,folderName0,folderName1,folderName2,fileName))
    else:
        raise ErrorCoding("The function only allow 2 parameter,If you want to generate a file in the current folder,please let the first parameter be ""or \'\'")
    return joinedPath
    