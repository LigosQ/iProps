#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 14:29:08 2020
@author: tafch
"""
import os
from files.arff2csv import *
import pandas as pd
import numpy as np
import subprocess,pickle,os
from files.Moran_t import *
from files.Geary_t import *
from files.NMBroto_t import *
from files.SOCNumber_t import *
from files.QSOrder_t import *
from files.pse_t import *
from files.acc_t import *
from files.fun_dfData2Csv import *
from files.geneSmartPth import *
from files.class_posNegFasta2Mat188d import *
from files import f_CKSAAGP,f_CKSAAP,f_CTDC,f_CTDD_v1,f_CTDT,f_PAAC,f_DDE_intra
from files.f_geneFastaDict import f_geneFastaDict
from files import globSet
from files.f_calcTripCompEntra import f_clacTriDf_P_N,f_redsimpDict2Str
from files import f_eaac_e
from files import f_APAAC
from files import f_ASDC
class ErrorUser(Exception):
    pass
def isFileExist(filePth):
    if(os.path.isfile(filePth)):
        return True
    else:
        return False
def chgDfClassLabel(dfdata,newlabel):
    seriOrigClass = dfdata['class']
    newClass = [newlabel for i in range(len(seriOrigClass))]
    dfdata['class'] = newClass
    return dfdata
def fun_calcFeat188d(posfile,negfile,s_taskID):
    outArffPth_p = geneSmartPth('results','pos.arff')
    outArffPth_n = geneSmartPth('results','neg.arff')
    outcsvfilePth_p = geneSmartPth('results','pos.csv')
    outcsvfilePth_n = geneSmartPth('results','neg.csv')
    obj_188d = c_2fastaHybrid188FeatMat(posfile, negfile)
    df_feat188_all = obj_188d.f_geneFeatAdCombine()
    return df_feat188_all
def fun_adaptMoranDfReslt(df_csvdata,newlab):
    df_csvdata.rename(columns={'#':'class'},inplace=True)
    df_transed = chgDfClassLabel(df_csvdata,newlab)
    return df_transed
def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err  = ex.communicate()
    status = ex.wait()
    return out.decode()
def clacPropByAdaptParas(posfile,negfile,method):
    isNeedLoop = True
    initNlag = 5
    while isNeedLoop:
        try:
            if method.lower()=="moran":
                df_p, status_p = Moran_initSet_Calc1(posfile,initNlag)
                df_n, status_n = Moran_initSet_Calc1(negfile,initNlag)
            elif method.lower()=="geary":
                df_p, status_p = myFun_calcGeary(posfile,initNlag)
                df_n, status_n = myFun_calcGeary(negfile,initNlag)
            elif method.lower()=="nmbroto":
                df_p, status_p = myFun_calcNmbroto(posfile,initNlag)
                df_n, status_n = myFun_calcNmbroto(negfile,initNlag)
            elif method.lower()=="qsorder":
                df_p, status_p = myfun_calcQsOrder(posfile,initNlag)
                df_n, status_n = myfun_calcQsOrder(negfile,initNlag)
            elif method.lower()=="socnumber":
                df_p, status_p = myfun_calcSOCnumber(posfile,initNlag)
                df_n, status_n = myfun_calcSOCnumber(negfile,initNlag)
            else:
                raise ErrorUser(''.join(['There was an error in computing ',method]))
            isNeedLoop = False
            return status_p, status_n,df_p,df_n
        except Exception as e:
            if initNlag>=2:
                initNlag -= 1
                print(e)
            else:
                initNlag =1
def f_comb2dfFeats_1prop(posfile,negfile,s_taskID,s_propName):
    status_p,status_n,df_p,df_n = clacPropByAdaptParas(posfile,negfile,s_propName)
    if (status_p and status_n):
        df_poslabl = fun_adaptMoranDfReslt(df_p,1)
        df_neglabl = fun_adaptMoranDfReslt(df_n,0)
        df_moran_all = pd.concat((df_poslabl,df_neglabl))
        return df_moran_all
    else:
        raise ErrorUser(f'The {s_propName} value do not correcttly calculated')
def calcCombPsePropCsvs(posfile,negfile,method,s_taskID,v_w,v_lambda):
    csvpth_p = geneSmartPth('results',''.join([method,'_p_',s_taskID,'.csv']))
    csvpth_n = geneSmartPth('results',''.join([method,'_n_',s_taskID,'.csv']))
    status_p = myfun_calcPseProp(posfile,csvpth_p,method,v_w,v_lambda)
    status_n = myfun_calcPseProp(negfile,csvpth_n,method,v_w,v_lambda)
    if (status_p and status_n):
        df_all_pos = pd.read_csv(csvpth_p)
        df_poslabl = fun_adaptMoranDfReslt(df_all_pos,1)
        df_all_neg = pd.read_csv(csvpth_n)
        df_neglabl = fun_adaptMoranDfReslt(df_all_neg,0)
        df_moran_all = pd.concat((df_poslabl,df_neglabl))
        return df_moran_all
    else:
        raise ErrorUser('The current Pse prop do not correcttly calculated') 
def calcAccPropCsvs(posfile,negfile,method,s_taskID):
    csvpth_p = geneSmartPth('results',''.join([method,'_p_',s_taskID,'.csv']))
    csvpth_n = geneSmartPth('results',''.join([method,'_n_',s_taskID,'.csv']))
    df_csv_p, status_p = calcAcc_MainFun_forEmbed(posfile,csvpth_p,method)
    df_csv_n, status_n = calcAcc_MainFun_forEmbed(negfile,csvpth_n,method)
    if (status_p and status_n):
        df_all_pos = df_csv_p
        df_poslabl = fun_adaptMoranDfReslt(df_all_pos,1)
        df_all_neg = df_csv_n
        df_neglabl = fun_adaptMoranDfReslt(df_all_neg,0)
        if (not (df_poslabl is None)) and (not (df_neglabl is None)):
            df_moran_all = pd.concat((df_poslabl,df_neglabl))
        else:
            raise ErrorUser('one of readed data is None....')
        return df_moran_all
    else:
        raise ErrorUser('The ACC prop do not correcttly calculated') 
def calcMultiFeats(posfile,negfile,methodname,taskId,userFeatCsvPth=0):
    if (isFileExist(posfile) and isFileExist(negfile)):
        pass
    else:
        raise ErrorUser('Your given sequence file is not exist...')
    if (methodname is None):
        raise ErrorUser('You do not support the name of used method')
    else:
        pass
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    csv_filePth = geneSmartPth('results',''.join([methodname,'_', str(taskId),'.csv']))
    if methodname=='188d':
        dfFeat_188d = fun_calcFeat188d(posfile,negfile,taskId)
        writeDf2csv(dfFeat_188d.applymap(lambda x: '%.5f'%x),csv_filePth)
        return dfFeat_188d
    if methodname in ['Moran','Geary','nmbroto','Socnumber','Qsorder']:
        dfFeat = f_comb2dfFeats_1prop(posfile,negfile,taskId,methodname)
        writeDf2csv(dfFeat.applymap(lambda x: '%.5f'%x),csv_filePth)
        return dfFeat
    if methodname in ['SC-PseAAC-General','SC-PseAAC','PC-PseAAC']:
        if methodname == 'SC-PseAAC':
            s_propName = 'ScPseAAC'
        else:
            s_propName = 'ScGeneral'
        v_lambda = d_allParas[s_propName]['lambda']
        v_w = d_allParas[s_propName]['w']
        dfFeat_pseFamily = calcCombPsePropCsvs(posfile,negfile,methodname,taskId,v_w,v_lambda)
        writeDf2csv(dfFeat_pseFamily.applymap(lambda x: '%.5f'%x),csv_filePth)
        return dfFeat_pseFamily
    if methodname in ['AC','CC','ACC']:
        dfFeat_ACFamily = calcAccPropCsvs(posfile,negfile,methodname,taskId)
        writeDf2csv(dfFeat_ACFamily.applymap(lambda x: '%.5f'%x),csv_filePth)
        return dfFeat_ACFamily
    if methodname in ['CKSAAGP','CKSAAP','PAAC','CTDC','CTDD','CTDT','DDE']:
        s_method = methodname
        try:
            d_fastaSeqs
        except:
            d_fastaSeqs = f_geneFastaDict(posfile,negfile)
        else:
            pass
        if s_method.upper()=='DDE':
            df_feats = f_DDE_intra.f_DDE_in2types(d_fastaSeqs)
        elif s_method.upper()=='PAAC':
            i_lambda = d_allParas['PAAC']['lambda']
            f_wVal = d_allParas['PAAC']['w']
            df_feats = f_PAAC.f_PAAC_2types(d_fastaSeqs,i_lambda,f_wVal)
        elif s_method.upper()=='CTDT':
            df_feats = f_CTDT.f_CTDT_in2types(d_fastaSeqs)
        elif s_method.upper()=='CTDD':
            df_feats = f_CTDD_v1.f_CTDD_in2types(d_fastaSeqs)
        elif s_method.upper()=='CTDC':
            df_feats = f_CTDC.f_CTDC_in2types(d_fastaSeqs)
        elif s_method.upper()=='CKSAAP':
            i_gap = d_allParas['CKSAAP']
            df_feats = f_CKSAAP.f_CKSAAP_in2types(d_fastaSeqs,i_gap)
        elif s_method.upper()=='CKSAAGP':
            i_gap = d_allParas['CKSAAGP']['nlag']
            i_redSchmNo = d_allParas['CKSAAGP']['redSchmNo']
            s_1redSchm = f_redsimpDict2Str(i_redSchmNo)
            df_feats = f_CKSAAGP.f_CKSAAGP_in2types(d_fastaSeqs,s_1redSchm,i_gap)
        else:
            raise ErrorCoding('The name of the method you provided is incorrect, please confirm its accuracy')
        writeDf2csv(df_feats,csv_filePth)
        return df_feats
    if methodname=='rTripComp':
        try:
            d_allParas['rTrip']['i_redSchmNo']
        except:
            raise ErrorUser('You did not set the reduction scheme NO. required to calculate the Tripeptide composition')
        try:
            d_allParas['rTrip']['i_tripepTypeNo']
        except:
            raise ErrorUser('You did not set the tripeptide type NO. required to calculate the Tripeptide composition')
        df_feats_tripComp = f_clacTriDf_P_N(posfile,negfile,d_allParas['rTrip']['i_redSchmNo'],
                                            d_allParas['rTrip']['i_tripepTypeNo'])
        writeDf2csv(df_feats_tripComp.applymap(lambda x: '%.5f'%x),csv_filePth)
        return df_feats_tripComp
    if methodname=='userGivenFeat':
        if userFeatCsvPth==0:
            raise ErrorUser('The csv file pth in function fun_geneMultiFeat.py'
                            '->calcMultiFeats is wrong(Line 349), please check...')
        else:
            dfFeat_giveCSV = pd.read_csv(userFeatCsvPth)
            writeDf2csv(dfFeat_giveCSV.applymap(lambda x: '%.5f'%x),csv_filePth)
            return dfFeat_giveCSV
    if methodname=='ASDC':
        df_ASDC = f_ASDC.f_ASDC_comb2FeatFiles(posfile,negfile)
        writeDf2csv(df_ASDC,csv_filePth)
        return df_ASDC
    elif methodname=='EAAC':
        df_EAAC = f_eaac_e.f_EAAC_seqs_posAdNeg(posfile,negfile)
        writeDf2csv(df_EAAC,csv_filePth)
        return df_EAAC
    elif methodname=='APAAC':
        ilambda = d_allParas['APAAC']['lambda']
        f_w_val = d_allParas['APAAC']['w']
        df_APAAC = f_APAAC.f_APAAC_seqs_2types(posfile,negfile,ilambda,f_w_val)
        writeDf2csv(df_APAAC,csv_filePth)
        return df_APAAC
    raise ErrorUser('Your given method '+methodname+' is wrong.\n'
                    'Check if your method is in our support method list...... ')
def main():
    parser = argparse.ArgumentParser(description="Calc multiple features and return a csv feature file")
    parser.add_argument('-p', '--posFile', help="The input file should be saved in the txt format(txt,or fasta), other file types are not supported at present", required=True)
    parser.add_argument('-n', '--negFile', help="The input file should be saved in the txt format(txt,or fasta), other file types are not supported at present", required=True)
    parser.add_argument('-m', '--methodname', help='The feature name:(string type), which is used for labeling csv file under different alphabets', required=True)
    args = parser.parse_args()
    calcMultiFeats(args.posFile, args.negFile, args.methodname)
if __name__ == "__main__":
    main()