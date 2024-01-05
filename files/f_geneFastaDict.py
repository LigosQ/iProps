#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:24:21 2023
@author: sealight
"""
from files import globSet
class ErrorCoding(Exception):
    pass
def f_openExtractSeqList(s_fastaPth):
    ls_allSeqInFasta = []
    try:
        with open(s_fastaPth,'r') as fid:
            for s_line_i in fid.readlines():
                if s_line_i.startswith('>'):
                    pass
                else:
                    s_line_strip = s_line_i.strip()
                    if len(s_line_strip)<globSet.getMinSeqLen():
                        globSet.setMinSeqLen(len(s_line_strip))
                    ls_allSeqInFasta.append(s_line_strip)
    except IOError:
        print(''.join(["there is an erroe when open and load ", s_fastaPth]))
    return ls_allSeqInFasta
def f_geneFastaDict(s_posPth, s_negPth):
    d_fastaSeq = dict()
    ls_fastaSeq_pos = f_openExtractSeqList(s_posPth)
    ls_fastaSeq_neg = f_openExtractSeqList(s_negPth)
    d_fastaSeq['pos'] = ls_fastaSeq_pos
    d_fastaSeq['neg'] = ls_fastaSeq_neg
    return d_fastaSeq
    