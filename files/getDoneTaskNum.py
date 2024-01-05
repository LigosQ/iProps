#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:42:48 2022
@author: sealight
"""
from files import globSet
# from files.globSet import get_finalProps
def f_getDoneTaskNum():
    ls_allTasks = globSet.get_allTasks()
    ls_doneTasks = globSet.get_doneFeat()
    return ls_allTasks, ls_doneTasks