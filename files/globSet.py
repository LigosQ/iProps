#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:01:28 2022
@author: sealight
"""
import pickle,platform
from files import geneSmartPth
class ErrorCoding(Exception):
    pass
def _init():
    global _d_userSlction
    _d_userSlction = dict()
    global _ls_taskID
    _ls_taskID = ['000']
    global _glob_doneTasks_ls
    _glob_doneTasks_ls = ['None']
    global _glob_allTask
    _glob_allTask = ['None']
    global _d_finalProps
    _d_finalProps = dict()
    global _b_ls_taskFinished
    _b_ls_taskFinished = [False]
    global _d_finalResults
    _d_finalResults = dict()
    global _ls_plotDone
    _ls_plotDone = [False]
    global _ls_UmapPlotDone
    _ls_UmapPlotDone = [False]
    global _d_bothDispTsneUmapInfo
    _d_bothDispTsneUmapInfo = {
        'tsne':[False],
        'umap':[False],
        'tsne_violin_progPloted':[False],
        'umap_violin_progPloted':[False],
        'tsne_violin_disped':[False],
        'umap_violin_disped':[False],
        }
    global _d_task_isDone
    _d_task_isDone = {
        'accSortList_disped':[False],
        'accSortList_progPloted':[False],
        }
    global _d_figFilePth
    _d_figFilePth = dict()
    global _d_readyStateForFS
    _d_readyStateForFS = dict()
    _d_readyStateForFS['fsProcession'] = [False]
    _d_readyStateForFS['fsResltDisped'] = [False]
    global _ls_p_bestCsv
    _ls_p_bestCsv = [False]
    global _d_perform_elems
    _d_perform_elems = dict()
    global _d_featCsvPth
    _d_featCsvPth = dict()
    global _d_ReduceSchm
    _d_ReduceSchm = dict()
    global _ls_PairNum
    _ls_PairNum = [2]
    global _d_uniqueRedDict
    _d_uniqueRedDict = dict()
    global _ls_minSeqLen
    _ls_minSeqLen = [100000000]
    global _ls_isAllTaskFish
    _ls_isAllTaskFish = [False]
    global _d_clacStatus
    _d_clacStatus = dict()
    _d_clacStatus['isFeatCalcDone'] = [False]
    _d_clacStatus['isCombCalcDone'] = [False]
    _d_clacStatus['failProps'] = [' ']
    global _ls_rootPth
    _ls_rootPth = ['']
    global _ls_pcPlatform
    _ls_pcPlatform = ['']
    global _glbParas
    _glbParas = {'0':0}
def addFail1Props(s_propName):
    _d_clacStatus['failProps'].append(s_propName)
def getFailProps():
    return _d_clacStatus['failProps']
def getGlobParas():
    p_pickPth = geneSmartPth.geneSmartPth('data','paras.data')
    with open(p_pickPth, 'rb') as f:
        _glbParas = pickle.load(f)
    return _glbParas
def get_pcPlatformInfo():
    try:
        if _ls_pcPlatform[-1]=='':
           set_pcPlatformInfo(platform.platform().lower())
    except:
        raise ErrorCoding('Error output device platform information')
def set_pcPlatformInfo(s_platform):
    if isinstance(s_platform, str):
        _ls_pcPlatform.append(s_platform)
    else:
        raise ErrorCoding('The platform info you provide is not a string type')
def get_rootPth():
    try:
        return _ls_rootPth[-1]
    except:
        raise ErrorCoding('Unable to get the root directory path')
def set_rootPth(s_givenPth):
    if isinstance(s_givenPth, str):
        _ls_rootPth.append(s_givenPth)
    else:
        raise ErrorCoding('The argument you provide is not a string type')
def setAllTaskFish():
    _ls_isAllTaskFish.append(True)
def isAllTaskFish():
    try:
        return _ls_isAllTaskFish[-1]
    except:
        return False
def setFeatCalcFinish():
    _d_clacStatus['isFeatCalcDone'].append(True)
def getIsFeatCalcDone():
    try:
        return _d_clacStatus['isFeatCalcDone'][-1]
    except:
        return False
def setInCombPhase():
    _d_clacStatus['isCombCalcDone'].append(True)
def getIsInCombPhase():
    try:
        return _d_clacStatus['isCombCalcDone'][-1]
    except:
        return False
def setMinSeqLen(i_val):
    if i_val==0:
        raise ErrorCoding('There is a empty line in the fasta file. This line will affect the running ot this file.')
    if isinstance(i_val, int):
        _ls_minSeqLen.append(i_val)
    else:
        raise ErrorCoding('The first parameter should be the int format.')
def getMinSeqLen():
    try:
        _ls_minSeqLen
    except:
        return _ls_minSeqLen[-1]
    else:
        return _ls_minSeqLen[-1]
def f_isProdReduceDict():
    try:
        _d_uniqueRedDict
    except:
        return False
    else:
        if len(_d_uniqueRedDict)>=1:
            return True
        else:
            return False
def f_chgStr2Dict(s_line_i):
    d_curRedSchm = dict()
    s_line_temp_i = s_line_i.strip()
    ls_subGrpList = s_line_temp_i.split('#')
    for s_subGrp in ls_subGrpList:
        for s_1AA in s_subGrp:
            d_curRedSchm[s_1AA] = s_subGrp[0]
    return d_curRedSchm
def getFeatNumInPairs(defVal=None):
    try:
        _ls_PairNum
    except:
        return _ls_PairNum[-1]
    else:
        return _ls_PairNum[-1]
def setFeatNumInPairs(i_number):
    _ls_PairNum.append(int(i_number))
def f_tranTxt2Dict(s_alphaTxt):
    import pickle
    d_allSchm = dict()
    i_schmNo = 0
    try:
        with open(s_alphaTxt,'rb') as fid_schmPkl:
            s_allSchmLines = pickle.load(fid_schmPkl)
    except:
        raise ErrorCoding('Error: the code cannot open the group scheme pkl file.')
    ls_allGrpSchmStr = s_allSchmLines.split('\n')
    for i,s_schmStr_i in enumerate(ls_allGrpSchmStr):
        i_schmNo += 1
        d_schm_i = dict()
        s_line_strip = s_schmStr_i.strip()
        ls_subSchm = s_line_strip.split('#')
        if ls_subSchm[0]=='':
            ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
            d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
            d_schm_i = d_origAmAcid_2RedStr
        else:
            for s_item in ls_subSchm:
                d_schm_i[s_item[0]] = s_item
        d_allSchm[str(i_schmNo)] = d_schm_i
    return d_allSchm
def setRedSchmIsFull(p_redSchmTxt):
    _d_ReduceSchm['redSchmDict'] = f_tranTxt2Dict(p_redSchmTxt)
def setReduceSchm(d_allSchmInfo):
    _d_ReduceSchm['redSchmDict'] = d_allSchmInfo
def getReduceSchm(defVal=None):
    try:
        return _d_ReduceSchm['redSchmDict']
    except:
        return defVal
def setGlobID(s_taskID):
    _ls_taskID.append(s_taskID)
def getGlobID(defVal=None):
    try:
        return _ls_taskID[-1]
    except:
        return defVal
def setUserFsMthd(s_FS_mthd):
    _d_userSlction['FS_mthd'] = s_FS_mthd
def getUserFsMthd(defVal=None):
    try:
        return _d_userSlction['FS_mthd']
    except:
        return defVal
def add_doneFeat(val):
    # _glob_doneTasks_ls.append(val)
    if _glob_doneTasks_ls[-1]=='None':
        _glob_doneTasks_ls[-1] = val
    else:
        _glob_doneTasks_ls.append(val)
def get_doneFeat(defVal=None):
    # try:
    #     return _glob_doneTasks_ls
    # except KeyError:
    #     return defVal
    try:
        if _glob_doneTasks_ls[-1]=='None':
            return []
        else:
            return _glob_doneTasks_ls
    except KeyError:
        return defVal
def add_allTask(ls_taskNames):
    _glob_allTask.extend(ls_taskNames)
def get_allTasks(defVal=None):
    try:
        return _glob_allTask
    except:
        return defVal
def add_finalProp(s_propName, fv_accVal):
    if fv_accVal=='omitted':
        pass
    else:
        _d_finalProps[s_propName] = fv_accVal
def get_finalProps():
    try:
        return _d_finalProps
    except:
        return 0
def set_taskFinishStatus(b_status):
    if b_status:
        _b_ls_taskFinished.append(True)
def get_taskFinishStatus():
    return _b_ls_taskFinished[-1]
def set_finalTaskResults(s_resultFileName, p_resultFilePth):
    _d_finalResults[s_resultFileName] = p_resultFilePth
def get_finalTaskResults(s_resultFileKeyName):
    try:
        return _d_finalResults[s_resultFileKeyName]
    except:
        return None
def set_plotTaskStatus(b_ifFinished):
    if b_ifFinished==True:
        _ls_plotDone.append(True)
def get_plotTaskStatus():
    try:
        return _ls_plotDone[-1]
    except:
        return None
def set_umapTask_done():
    _ls_UmapPlotDone.append(True)
def get_umapTask_status():
    try:
        return _ls_UmapPlotDone[-1]
    except:
        return None
def set_bothTsneUmapDisp_done(s_tsneOrUmap):
    _d_bothDispTsneUmapInfo[s_tsneOrUmap].append(True)
def get_bothTsneUmapDisp_status(s_tsneOrUmap):
    try:
        return _d_bothDispTsneUmapInfo[s_tsneOrUmap][-1]
    except:
        return None
def set_violPlot_status_done(s_tsneOrUmap):
    _d_bothDispTsneUmapInfo[s_tsneOrUmap].append(True)
def get_violPlot_status(s_tsneOrUmap):
    try:
        return _d_bothDispTsneUmapInfo[s_tsneOrUmap][-1]
    except:
        return None
def set_task_done(s_task):
    _d_task_isDone[s_task].append(True)
def get_task_isDone(s_task):
    try:
        return _d_task_isDone[s_task][-1]
    except:
        return None
def set_figFilePth(s_figName, p_figFilePth):
    _d_figFilePth[s_figName] = p_figFilePth
def get_figFilePth(s_figName):
    try:
        return _d_figFilePth[s_figName]
    except:
        return ''
def set_FSreadyStatusOK():
    _d_readyStateForFS['fsProcession'].append(True)
def is_readyFS():
    try:
        return _d_readyStateForFS['fsProcession'][-1]
    except:
        return False
def set_FS_dispState_Ok():
    _d_readyStateForFS['fsResltDisped'].append(True)
def is_disped_FSresults():
    try:
        return _d_readyStateForFS['fsResltDisped'][-1]
    except:
        return False
def set_bestFeat_csvPth(s_csvPth):
    _ls_p_bestCsv.append(s_csvPth)
def get_bestFeat_csvPth():
    try:
        if _ls_p_bestCsv[-1]==False:
            return None
        else:
            return _ls_p_bestCsv[-1]
    except:
        return None
def set_perform_paras(s_key, s_val):
    try:
        _d_perform_elems[s_key] = s_val
    except:
        raise ErrorCoding('You give a wrong key or value in setting function.')
def get_perform_paras(s_key):
    try:
        return _d_perform_elems[s_key]
    except:
        return None
def set_featCsvPth(s_featName,s_pth):
    _d_featCsvPth[s_featName] = s_pth
def get_featCsvPth(s_featName):
    try:
        return _d_featCsvPth[s_featName]
    except:
        return None
if __name__ == '__main__':
    _init()
    if getUniqueRedDict() is None:
        d = getUniqueRedDict()
        setReduceSchm(d)
    else:
        pass