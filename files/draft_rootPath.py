#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:49:29 2023
@author: sealight
"""
import os,platform
class ErrorCoding(Exception):
    pass
class C_geneRootFolderPth(object):
    def __init__(self):
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
        self._p_rootPth = curWorkPth_proced
    @property()
    def RootPth(self):
        return self._p_rootPth
def f_geneRooter():
    P_rootObj = C_geneRootFolderPth()
    return P_rootObj.RootPth()
