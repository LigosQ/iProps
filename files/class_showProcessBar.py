#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 17:45:22 2021
@author: tafch
"""
import sys, time
class c_showProcessBar():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 
    max_steps = 0 
    max_arrow = 50 
    infoDone = 'done'
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) 
        num_line = self.max_arrow - num_arrow 
        percent = self.i * 100.0 / self.max_steps 
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' 
        sys.stdout.write(process_bar) 
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()
    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0
