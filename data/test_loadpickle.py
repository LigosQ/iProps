#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 21:01:56 2023

@author: sealight
"""
import pickle

class ErrorCoding(Exception):
    pass

# with open('./usergiven.data', 'rb') as f:
#     data = pickle.load(f)

# print(data)

# s_seqs = '''EQ#FY#HIKL
# DN#EKQR#FWY#HS#IV#LM
# DEKST#LMTV
# CH#EKQR#FWY#IV#LM#NS
# DEKPRS#LMTV
# DN#EKQR#FWY#ILMV
# DEHKNQR#FILMVWY#ST
# DEKPQST#LMTV#NR
# EKQR#FWY#ILV
# DEKPST#FLMTV
#  '''

# try:
#     with open('./groupSchms_Afp10.pkl','wb') as f:
#         pickle.dump(s_seqs, f, True)
# except:
#     raise 
def f_sortStr(s_alpha):
    ls_alpha = list(s_alpha)
    ls_alpha.sort()
    return ''.join(ls_alpha)
    
p_pklFile = './groupSchms_mini9.pkl'
p_pklFile = './paras.data'
p_pklFile = './redSchm3Len.pkl'
try:
    with open(p_pklFile, 'rb') as f:
        s_grpSchms = pickle.load(f)
except:
    raise

print(s_grpSchms)

ls_schmName_len3 = ['redSchm_2', 'redSchm_33', 'redSchm_44', 'redSchm_80', 'redSchm_105', 'redSchm_126', 
    'redSchm_149', 'redSchm_166', 'redSchm_182', 'redSchm_183', 'redSchm_189', 'redSchm_192', 
    'redSchm_194', 'redSchm_196', 'redSchm_199', 'redSchm_216', 'redSchm_234', 'redSchm_248', 
    'redSchm_262', 'redSchm_292', 'redSchm_317', 'redSchm_382', 'redSchm_400', 'redSchm_426', 
    'redSchm_442', 'redSchm_460', 'redSchm_478', 'redSchm_498', 'redSchm_499', 'redSchm_503', 
    'redSchm_520', 'redSchm_529', 'redSchm_546', 
]

d_3grpDivSchm = dict()
for i,s_schmName in enumerate(ls_schmName_len3):
    ls_curSchm = []
    ls_curSchm.append(s_grpSchms['group1'][s_schmName].strip())
    ls_curSchm.append(s_grpSchms['group2'][s_schmName].strip())
    ls_curSchm.append(s_grpSchms['group3'][s_schmName].strip())
    s_curSchmStr = ','.join(ls_curSchm)
    d_3grpDivSchm[s_schmName] = s_curSchmStr
print(d_3grpDivSchm)

# def f_tranTxt2Dict(s_alphaTxt):
#     import pickle
#     #get the file id
#     d_allSchm = dict()
#     #counter
#     i_schmNo = 0
#     #open files
#     try:
#         with open(s_alphaTxt,'rb') as fid_schmPkl:
#             s_allSchmLines = pickle.load(fid_schmPkl)
#     except:
#         raise ErrorCoding('Error: the code cannot open the group scheme pkl file.')
#     #divide the whole string to a list variable
#     ls_allGrpSchmStr = s_allSchmLines.split('\n')
#     #iteration for each group scheme
#     for i,s_schmStr_i in enumerate(ls_allGrpSchmStr):
#         i_schmNo += 1
#         #准备空的dict保存当前的约化方案
#         d_schm_i = dict()
#         ##remove the useless symbols
#         s_line_strip = s_schmStr_i.strip()
#         #根据符号#将当前编码划分为list
#         ls_subSchm = s_line_strip.split('#')
#         #检查是否有空格字符串，有的话表示需要不约化的场景
#         if ls_subSchm[0]=='':
#             #generate the list of original self-self dictionary
#             ls_origAmAcid = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
#             #new a dictionary by its construte function
#             #generate the element of dict likes 'A':'A', 'B':'B'(initial state)
#             d_origAmAcid_2RedStr = dict(zip(ls_origAmAcid,ls_origAmAcid))
#             d_schm_i = d_origAmAcid_2RedStr
#         else:
#             #iteration for all elements in the above list
#             for s_item in ls_subSchm:
#                 #继续使用-将当前schm进行划分
#                 #保存对应的约化方案
#                 d_schm_i[s_item[0]] = s_item
#         #将当前所有的方案信息保存到dict中
#         d_allSchm[str(i_schmNo)] = d_schm_i
#     #iteration done
#     #return value 
#     return d_allSchm

# # d_allSchmsDict = f_tranTxt2Dict('./groupSchms_mini9.pkl')

# s_3groupPkl = '/Users/sealight/Documents/TsuWork/code/allprojectcode/workInUestc/6iProp/data/redSchm3Len.pkl'
# try:
#     with open(s_3groupPkl,'rb') as fid:
#         s3grpStr = pickle.load(fid)
# except:
#     raise
    
# print(s3grpStr)