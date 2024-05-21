#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:28:03 2024

@author: sealight
"""
import random
import math
import pandas as pd
import argparse
from f_geneDict_fromPkl import f_getAADict_dipDict

class ErrorCoding(Exception):
    pass

# Mish激活函数
def mish(x):
    f_temp = math.log(1 + math.exp(x))
    return x * math.tanh(f_temp)


def f_getList_noSpace(s_1line):
    ls_1lineELems_hasSpace = s_1line.split(' ')
    ls_1lineELems_noSpace = [item for item in ls_1lineELems_hasSpace if item != '']
    return ls_1lineELems_noSpace

#检验提取的信息是否正确
def f_varfPSSM_line1(ls_pssmData):
    s_20AAs = list('ARNDCQEGHILKMFPSTWYV')
    # 检验第一个元素和第二个元素是否均为20个氨基酸
    if (ls_pssmData[0][0] in s_20AAs) and (ls_pssmData[0][1] in s_20AAs):
        return True
    else:
        return False
    
# 检验第二个元素的第一个是是否为1，第二个元素为20个氨基酸
def f_varfPSSM_otherLines(ls_pssmData):
    s_20AAs = 'ARNDCQEGHILKMFPSTWYV'
    i_randInt = random.randint(2, len(ls_pssmData)+1)
    # 检验第一个元素和第二个元素是否均为20个氨基酸
    if (ls_pssmData[1][0] == '1' and ls_pssmData[i_randInt][0] == str(i_randInt) 
        and ls_pssmData[i_randInt][1] in s_20AAs):
        return True
    else:
        return False
    
# 函数：将序列划分为N个等长的片段，当前片段头部添加上一片段的后20%序列，尾部添加下一片段的前20%序列
def f_get7Segments(s_protSeq, i_segNum=7, f_overlap=0.2):
    i_protLen = len(s_protSeq)
    i_segmentLen = i_protLen // i_segNum
    ls_Segments = []
    i_overlapLen = int(i_segmentLen * f_overlap)
    for i in range(i_segNum):
        i_start = i * i_segmentLen
        i_end = (i + 1) * i_segmentLen
        if i == 0:
            if i_end + i_overlapLen < i_protLen:
                ls_start_end_ind = [i_start,i_end + i_overlapLen]
            else:
                ls_start_end_ind = [i_start,i_protLen-1]
        elif i == (i_segNum - 1):
            if i_start - i_overlapLen > 0:
                ls_start_end_ind = [i_start - i_overlapLen,i_end]
            else:
                ls_start_end_ind = [i_start,i_protLen-1]
        else:
            if i_start-i_overlapLen >=0 and i_end+i_overlapLen < i_protLen:
                ls_start_end_ind = [i_start-i_overlapLen,i_end+i_overlapLen]
            elif i_start-i_overlapLen >=0 and i_end+i_overlapLen >= i_protLen:
                ls_start_end_ind = [i_start-i_overlapLen,i_protLen-1]
            elif i_start-i_overlapLen <=0 and i_end+i_overlapLen < i_protLen:
                ls_start_end_ind = [0,i_end+i_overlapLen]
            else:
                ls_start_end_ind = [i_start,i_end]
        ls_Segments.append(ls_start_end_ind)
    return ls_Segments

#函数：输入dataframe类型数据df, 计算d_s,t其中，d_s,t = 1/L*sum((X_i,s - X_i+1,t)^2/2)
def f_get_s_t_val(df):
    i_protLen = df.shape[0]
    # i_pssmCols = df.shape[1]
    ls_20AAs = list('ARNDCQEGHILKMFPSTWYV')
    ls_allDipeNames = []
    # print(f'shape:{i_protLen}x{i_pssmCols}')
    d_dipeps = dict()
    for i in range(20):
        for j in range(20):
            #组合dict
            s_curDipep = ''.join([ls_20AAs[i],ls_20AAs[j]])
            ls_allDipeNames.append(s_curDipep)
            f_sum = 0
            for k in range(i_protLen-1):
                #print(f'{k}-{i}; {k}-{j}')
                f_sum += ((df.iloc[k,i] - df.iloc[k+1,j])**2 / 2)
            # df_d.iloc[i,j] = f_sum / i_protLen
            d_dipeps[s_curDipep] = f_sum
    #添加第一列ARN......YV到矩阵的第一列
    ls_allDipVals = [d_dipeps[s_dipName] for i,s_dipName in enumerate(ls_allDipeNames)]
    # print((ls_allDipeNames))
    #将list转为dataframe
    df_allDipVals = pd.DataFrame([ls_allDipVals],columns=ls_allDipeNames)
    return df_allDipVals

# 函数：输入dataframe类型数据df, 计算每一列的均值,标准差
def f_get_3_elements(df):
    ls_mean = df.mean()
    ls_std = df.std()
    ls_df = f_get_s_t_val(df)
    # #将上述三个向量组合成大的list
    # ls_mean.extend(ls_std)
    # ls_mean.extend(ls_df)
    return ls_mean,ls_std,ls_df

def f_gene_rAAList_rDipList(ls_rAAs):
    ls_20AAs = list('ARNDCQEGHILKMFPSTWYV')
    #sort the key AAs according to the ARND... order
    ls_rAA_ordered = [s_1AA for i,s_1AA in enumerate(ls_20AAs) if s_1AA in ls_rAAs]
    #generate the ordered ruduced-dipeptides
    ls_rDip_ordered = []
    for i,s_AA_pre in enumerate(ls_rAA_ordered):
        for j,s_AA_suf in enumerate(ls_rAA_ordered):
            s_rDipep = ''.join([s_AA_pre,s_AA_suf])
            ls_rDip_ordered.append(s_rDipep)
    #return
    return ls_rAA_ordered,ls_rDip_ordered

def f_lsMean(ls_var):
    f_sum = 0
    for item in ls_var:
        f_sum += item
    return f_sum/(len(ls_var))
    

def process_pssm_file(s_pssmFile,s_alpha):
    try:
        with open(s_pssmFile, 'r') as f:
            s_pssmGoodLines = []
            for s_currentLine in f.readlines():
                # 去掉行尾的换行符
                s_currentLine = s_currentLine.strip()
                # 如果当前行为空则跳过
                if len(s_currentLine) == 0:
                    continue
                # 如果当前行以#开头则跳过
                if s_currentLine[0] == '#':
                    continue
                # 如果当前行数量不足20则跳过
                ls_curLineElems_noSpace = f_getList_noSpace(s_currentLine)
                if len(ls_curLineElems_noSpace) <=22:
                    continue
                s_pssmGoodLines.append(ls_curLineElems_noSpace)
    except:
        raise ErrorCoding('The file cannot be created, please check...')
    # 检验得到的数据是否符合要求
    if (f_varfPSSM_line1(s_pssmGoodLines) and 
        f_varfPSSM_otherLines(s_pssmGoodLines)):
        pass
    else:
        raise ErrorCoding('The data in the PSSM file is not correct, please check...')

    #处理第一行,各列名称
    ls_dfCols = ['ind','AA']
    ls_dfCols.extend([str(val) for i,val in enumerate(s_pssmGoodLines[0][:20])])
    #将s_pssmGoodLines只取前20列
    ls_pssm_pureData_str = [item[:22] for i,item in enumerate(s_pssmGoodLines) if i != 0]
    for i,item in enumerate(ls_pssm_pureData_str):
        ls_pssm_pureData_str[i] = [int(val) if val.isdigit() else val for val in item ]
    #当前约化字典对应的dict,一对多形式
    # print(ls_pssm_pureData_str[5])
    #将s_pssmGoodLines转化为dataframe

    #带有前两列的PSSM矩阵
    df_pssm = pd.DataFrame(ls_pssm_pureData_str, columns=ls_dfCols)
    # print(df_pssm.head())

    #获取PSSM矩阵中的序列字符串
    s_protSeq = ''.join(df_pssm['AA'].tolist())
    # print(s_protSeq)

    # 根据字符串长度将其划分为N段
    # i_protLen = len(s_protSeq)
    ls_splitIndex = f_get7Segments(s_protSeq)
    # print(ls_splitIndex)
    # print(df_pssm.shape)

    #纯粹的去掉前两列的PSSM数据特征
    df_pssm_pureData = df_pssm.iloc[:,2:]
    # print(df_pssm_pureData.head())

    #将所有数据应用Mish激活函数处理
    df_pssm_pureData = df_pssm_pureData.astype('int')
    df_pssm_active = df_pssm_pureData.applymap(mish)


    #对应于第一个分段的PSSM矩阵
    subMat_Pssm = df_pssm_active.iloc[ls_splitIndex[0][0]:ls_splitIndex[0][1]+1,:]
    ls_3_elems_1subMat = f_get_3_elements(subMat_Pssm)
    ser_1st_compMean = ls_3_elems_1subMat[0]
    ser_2nd_compStd = ls_3_elems_1subMat[1]
    df_3rd_PssmMat = ls_3_elems_1subMat[2]
    # print(ls_3_elems_1subMat)
    #二肽AR的值
    # print((ls_3_elems_1subMat[2]['AR'].values[0]))

    #根据不同类型的约化获取子分组的相关矩阵
    d_1AAdict,d_dipepDict = f_getAADict_dipDict(s_alpha)
    # print(d_dipepDict)
    ls_rAA_keys = d_1AAdict.keys()
    # ls_rDip_keys = d_dipepDict.keys()
    #根据约化方案产生对应的排序好的AAs, Dipeps
    ls_N_rAAs_ord, ls_N_rDips_ord = f_gene_rAAList_rDipList(ls_rAA_keys)
    # print(ls_N_rDips_ord)
    #分别读取各个子约化方案汇总信息
    ls_rFeat_1stGrp = []
    ls_rFeat_2ndGrp = []
    for i,s_r_1AA in enumerate(ls_N_rAAs_ord):
        #得到该约化字符对应的多个成员
        ls_origAAs_1_rAA = d_1AAdict[s_r_1AA]
        #获取第一组前N个特征
        f_rFeat_1stGrp = ser_1st_compMean[ls_origAAs_1_rAA].mean()
        # 第二个特征
        f_rFeat_2ndGrp = ser_2nd_compStd[ls_origAAs_1_rAA].mean()

        #
        ls_rFeat_1stGrp.append(f_rFeat_1stGrp)
        ls_rFeat_2ndGrp.append(f_rFeat_2ndGrp)
    ls_rFeat_3rdGrp = []
    for j,s_r_dip in enumerate(ls_N_rDips_ord):
        #得到该约化二肽对应的多个成员
        ls_origDips_1_rDip = d_dipepDict[s_r_dip]
        # 第三个特征
        ls_3grp_feats = [df_3rd_PssmMat.loc[:,item].values[0] for item in ls_origDips_1_rDip]
        # f_DipMean = df_3rd_PssmMat.loc[:,ls_origDips_1_rDip].mean().values[0]
        f_DipMean = f_lsMean(ls_3grp_feats)
        ls_rFeat_3rdGrp.append(f_DipMean)
    #组合特征
    ls_3GrpFeats = []
    ls_3GrpFeats.extend(ls_rFeat_1stGrp)
    ls_3GrpFeats.extend(ls_rFeat_2ndGrp)
    ls_3GrpFeats.extend(ls_rFeat_3rdGrp)
    ls_colnames = [''.join(['r',s_1_rAA,'_mean']) for i,s_1_rAA in enumerate(ls_N_rAAs_ord)]
    ls_colName_2nd = [''.join(['r',s_1_rAA,'_std']) for i,s_1_rAA in enumerate(ls_N_rAAs_ord)]
    ls_colName_3rd = [''.join(['r',s_1_rDip]) for i,s_1_rDip in enumerate(ls_N_rDips_ord)]
    ls_colnames.extend(ls_colName_2nd)
    ls_colnames.extend(ls_colName_3rd)
    #创建dataframe
    df_features = pd.DataFrame([ls_3GrpFeats], columns=ls_colnames)
    # return df_3rd_PssmMat,df_features
    return df_features

# s_pssmFile = '/Users/sealight/Documents/TsuWork/code/allprojectcode/workInUestc/6iProp/addFiles/p3.pssm'
# df_3rd_PssmMat, df_features = process_pssm_file(s_pssmFile,'DE#SF')
# print(df_3rd_PssmMat['DS'])
# print(df_3rd_PssmMat['DF'])
# print(df_3rd_PssmMat['ES'])
# print(df_3rd_PssmMat['EF'])
# print(df_features['rDS'])

def ScPssm(s_pssmPth, s_alphabet):
    return process_pssm_file(s_pssmPth, s_alphabet)

def ScPssmSave(s_pssmPth, s_alphabet,s_csvPath):
    df_scPssm = process_pssm_file(s_pssmPth, s_alphabet)
    df_scPssm.to_csv(s_csvPath,index=False)
    

def main():
    parser = argparse.ArgumentParser(description="Calculate the SC-PSSM feature")
    parser.add_argument('-p', '--pssmPath', help="The path of the PSSM file, other file types are not supported at present", required=True)
    parser.add_argument('-a', '--alphabet', help='The given alphabet for amino acid recoding', required=True)
    parser.add_argument('-o', '--outfile', help='The name of output picture: .csv type', required=True)
    args = parser.parse_args()
    
    ScPssmSave(args.pssmPath, args.alphabet, args.outfile)

if __name__ == '__main__':
    main()