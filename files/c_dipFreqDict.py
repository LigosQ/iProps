#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class c_dipFreqDict(object):
    def __init__(self,s_curAAs):
        self.s_AAs = s_curAAs
    def f_geneDipepDict(self):
        s_AAs = self.s_AAs
        ls_allCurDipep = [''.join([s_AAs[i1],s_AAs[i2]]) for i1 in range(len(s_AAs)) for i2 in range(len(s_AAs))]
        ls_allFreq = [0]*(len(s_AAs)**2)
        d_curDipep = dict(zip(ls_allCurDipep, ls_allFreq))
        return d_curDipep,ls_allCurDipep