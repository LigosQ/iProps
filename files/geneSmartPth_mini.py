#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:28:37 2023
@author: sealight
"""
"""
Created on Tue Mar 23 17:17:18 2021
@author: tafch
"""
import platform
import os
import time
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
def f_getIpropsRoot():
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
    elif  (("linux" in s_osInfo) or ('macos' in s_osInfo)):
        if ('/' in curWorkPth_abs):
            curWorkPth_proced = curWorkPth_abs
        else:
            raise ErrorCoding('There is no / in the path string.')
    else:
        raise ErrorCoding('Your current OS is not windows or Linux, \n'
                        'this version can not support your OS...')
    ls_allFilesInCurDir = os.listdir(curWorkPth_proced)
    if ('interpReport' in ls_allFilesInCurDir) and ('files' in ls_allFilesInCurDir) and ('results' in ls_allFilesInCurDir):
        if curWorkPth_proced[-1]=='/':
            p_prjROOT = curWorkPth_proced[:-1]
        else:
            p_prjROOT = curWorkPth_proced
        return p_prjROOT
    else:
        p_parDir = os.path.dirname(curWorkPth_proced)
        ls_filesInParDir = os.listdir(p_parDir)
        if ('interpReport' in ls_filesInParDir) and ('files' in ls_filesInParDir) and ('results' in ls_filesInParDir):
            if ls_filesInParDir[-1]=='/':
                p_prjROOT = p_parDir[:-1]
            else:
                p_prjROOT = p_parDir
            return p_prjROOT
        else:
            raise ErrorCoding('The root folder cannot be probed. You may have modified or renamed the directory. It is worth noting that this version of the code does not support the modification of subdirectory names inside the root folder, otherwise it may not be recognized.')
def f_geneAbsPath_frmROOT(*args):
    p_ROOT_absPth = f_getIpropsRoot()
    ls_fullPathDirNames = [p_ROOT_absPth]
    for i,pathElem in enumerate(args):
        if pathElem == '':
            pass
        else:
            ls_fullPathDirNames.append(pathElem)
    joinedPath = '/'.join(ls_fullPathDirNames)
    return joinedPath
    