#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:17:47 2020
@author: tafch
"""
import sys
class ErrorUser(Exception):
    pass
class putFastaSeqInOneline(object):
    def __int__(self):
        self._inputFastaFile = None
        self._outFileSeqInOneline = None
    @property
    def inputFastaFile(self):
        return self._inputFastaFile
    @inputFastaFile.setter
    def inputFastaFile(self, inFilePth):
        inputFastaPthList = inFilePth.split('.')
        inputFileSuffix = inputFastaPthList[-1]
        if inputFileSuffix=='fasta':
            self._inputFastaFile = inFilePth
        else:
            raise ErrorUser('The infile path is error,please check and ensure it is fasta format!...')
            sys.exit()
    @property
    def outFileSeqInOneline(self):
        inputFilePthStr = self.inputFastaFile
        pathList1 = inputFilePthStr.split('\\')
        pathList2 = inputFilePthStr.split('/')
        if len(pathList1)>1:
            fileName = pathList1[-1]
            newFileName = self.geneOutfileName(fileName)
            pathList1[-1] = newFileName
            outFileFullPth = '\\'.join(pathList1)
        if len(pathList2)>1:
            fileName = pathList2[-1]
            newFileName = self.geneOutfileName(fileName)
            pathList2[-1] = newFileName
            outFileFullPth = '/'.join(pathList2)
        self._outFileSeqInOneline = outFileFullPth
        return self._outFileSeqInOneline
    @outFileSeqInOneline.setter
    def outFileSeqInOneline(self,name):
        nameList = name.split('.')
        if nameList[-1]=='fasta':
            self._outFileSeqInOneline = name
        else:
            raise ErrorUser('The infile path is error,please check and ensure it is fasta format!...')
            sys.exit()
    def isFitToFormat(self):
        lineNum = 0
        fid = open(self.inputFastaFile,'r')
        for line in fid.readlines():
            lineNum += 1
            if lineNum % 2 ==1:
                if not line.startswith('>'):
                    return False
        return True
    def geneOutfileName(self, name=''):
        if name =='':
            fullName = 'output_OneLineSeq.fasta'
        else:
            inputFastaPthList = name.split('.')
            inputFileSuffix = inputFastaPthList[-1]
            if inputFileSuffix=='fasta':
                newName = inputFastaPthList[0]+'_OneLineSeq'
                fullName = newName + '.fasta'
            else:
                raise ErrorUser('The output path is error,please check and ensure it is fasta format!...')
                sys.exit()
        return fullName
    def geneOutFastaFromInput(self):
        inputFilePthStr = self.inputFastaFile
        pathList1 = inputFilePthStr.split('\\')
        pathList2 = inputFilePthStr.split('/')
        if len(pathList1)>1:
            fileName = pathList1[-1]
            newFileName = self.geneOutfileName(fileName)
            pathList1[-1] = newFileName
            outFileFullPth = '\\'.join(pathList1)
        if len(pathList2)>1:
            fileName = pathList2[-1]
            newFileName = self.geneOutfileName(fileName)
            pathList2[-1] = newFileName
            outFileFullPth = '/'.join(pathList2)
        return outFileFullPth
    def dealWithBadFile(self):
        lineNumber = 0
        outputPth = self.outFileSeqInOneline
        fidOutput = open(outputPth,'w+')
        infilePth = self.inputFastaFile
        fidInput = open(infilePth,'r')
        isSeqInOneLine = self.isFitToFormat()
        for line in fidInput.readlines():
            lineNumber += 1
            if isSeqInOneLine:
                fidOutput.write(line)
            else:
                if line.startswith('>'):
                    if lineNumber==1:
                        fidOutput.write(line)
                    else:
                        fidOutput.write('\n'+line)
                else:
                    linestr = line.strip()
                    fidOutput.write(linestr)
        fidOutput.close()
        