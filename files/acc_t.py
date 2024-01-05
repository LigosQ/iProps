#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from files.util import get_data, check_args, read_k
from files.pse_t import get_phyche_list, get_extra_index, get_phyche_value, get_aaindex, extend_aaindex, AAIndex
from files.fun_dfData2Csv import *
from files import globSet
def acc(input_data, k, lag, phyche_list, alphabet, extra_index_file=None, all_prop=False, theta_type=1):
    """This is a complete acc in PseKNC.
    :param k: int, the value of k-tuple.
    :param phyche_list: list, the input physicochemical properties list.
    :param extra_index_file: a file path includes the user-defined phyche_index.
    :param all_prop: bool, choose all physicochemical properties or not.
    :param theta_type: the value 1, 2 and 3 for ac, cc or acc.
    """
    phyche_list = get_phyche_list(k, phyche_list,
                                  extra_index_file=extra_index_file, alphabet=alphabet, all_prop=all_prop)
    phyche_vals = get_aaindex(phyche_list)
    if extra_index_file is not None:
        phyche_vals.extend(extend_aaindex(extra_index_file))
    seqs = get_data(input_data, alphabet)
    if alphabet == "ACDEFGHIKLMNPQRSTVWY":
        phyche_keys = phyche_vals[0].index_dict.keys()
        phyche_vals = [e.index_dict.values() for e in phyche_vals]
        new_phyche_vals = zip(*[e for e in phyche_vals])
        phyche_vals = {key: list(val) for key, val in zip(phyche_keys, new_phyche_vals)}
    if theta_type == 1:
        return make_ac_vec(seqs, lag, phyche_vals, k)
    elif theta_type == 2:
        return make_cc_vec(seqs, lag, phyche_vals, k)
    elif theta_type == 3:
        return make_acc_vec(seqs, lag, phyche_vals, k)
def make_ac_vec(sequence_list, lag, phyche_value, k):
    phyche_values = list(phyche_value.values())
    len_phyche_value = len(phyche_values[0])
    vec_ac = []
    for sequence in sequence_list:
        len_seq = len(sequence)
        each_vec = []
        for temp_lag in range(1, lag + 1):
            for j in range(len_phyche_value):
                ave_phyche_value = 0.0
                for i in range(len_seq - temp_lag - k + 1):
                    nucleotide = sequence[i: i + k]
                    ave_phyche_value += float(phyche_value[nucleotide][j])
                ave_phyche_value /= len_seq
                temp_sum = 0.0
                for i in range(len_seq - temp_lag - k + 1):
                    nucleotide1 = sequence[i: i + k]
                    nucleotide2 = sequence[i + temp_lag: i + temp_lag + k]
                    temp_sum += (float(phyche_value[nucleotide1][j]) - ave_phyche_value) * (
                        float(phyche_value[nucleotide2][j]))
                each_vec.append(round(temp_sum / (len_seq - temp_lag - k + 1), 8))
        vec_ac.append(each_vec)
    return vec_ac
def make_cc_vec(sequence_list, lag, phyche_value, k):
    phyche_values = list(phyche_value.values())
    len_phyche_value = len(phyche_values[0])
    vec_cc = []
    for sequence in sequence_list:
        len_seq = len(sequence)
        each_vec = []
        for temp_lag in range(1, lag + 1):
            for i1 in range(len_phyche_value):
                for i2 in range(len_phyche_value):
                    if i1 != i2:
                        ave_phyche_value1 = 0.0
                        ave_phyche_value2 = 0.0
                        for j in range(len_seq - temp_lag - k + 1):
                            nucleotide = sequence[j: j + k]
                            ave_phyche_value1 += float(phyche_value[nucleotide][i1])
                            ave_phyche_value2 += float(phyche_value[nucleotide][i2])
                        ave_phyche_value1 /= len_seq
                        ave_phyche_value2 /= len_seq
                        temp_sum = 0.0
                        for j in range(len_seq - temp_lag - k + 1):
                            nucleotide1 = sequence[j: j + k]
                            nucleotide2 = sequence[j + temp_lag: j + temp_lag + k]
                            temp_sum += (float(phyche_value[nucleotide1][i1]) - ave_phyche_value1) * \
                                        (float(phyche_value[nucleotide2][i2]) - ave_phyche_value2)
                        each_vec.append(round(temp_sum / (len_seq - temp_lag - k + 1), 8))
        vec_cc.append(each_vec)
    return vec_cc
def make_acc_vec(seqs, lag, phyche_values, k):
    from functools import reduce
    zipped = list(zip(make_ac_vec(seqs, lag, phyche_values, k), make_cc_vec(seqs, lag, phyche_values, k)))
    return [reduce(lambda x, y: x + y, e) for e in zipped]
def calcAcc_MainFun_forEmbed(fastapth,outputfile,method,alphabet='Protein',lag=2,
                             indexfile=None,userIndfile=None,args_a=False,
                             outFormat='csv', classLab=1):
    lag=None
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    with open(fastapth) as f:
        finishStatus = False
        k = read_k(alphabet, method, 0)
        if indexfile is not None:
            from pse import read_index
            ind_list = read_index(indexfile)
        else:
            ind_list = []
        default_e = []
        alphabet = "ACDEFGHIKLMNPQRSTVWY"
        default_e = ['Hydrophobicity', 'Hydrophilicity', 'Mass']
        theta_type = 1
        if method in ['DAC', 'TAC', 'AC']:
            theta_type = 1
            lag = d_allParas['AC']
        elif method in ['DCC', 'TCC', 'CC']:
            theta_type = 2
            lag = d_allParas['CC']
        elif method in ['DACC', 'TACC', 'ACC']:
            theta_type = 3
            lag = d_allParas['ACC']
        else:
            print("Method error!")
        if userIndfile is None and len(ind_list) == 0 and args_a is False:
            res = acc(f, k, lag, default_e, alphabet,
                      extra_index_file=userIndfile, all_prop=args_a, theta_type=theta_type)
        else:
            res = acc(f, k, lag, ind_list, alphabet,
                      extra_index_file=userIndfile, all_prop=args_a, theta_type=theta_type)
    if outFormat == 'tab':
        from util import write_tab
        write_tab(res, outputfile)
    elif outFormat == 'svm':
        from util import write_libsvm
        write_libsvm(res, [classLab] * len(res), outputfile)
    elif outFormat == 'csv':
        if len(res)==0:
            raise ErrorUser('Error! The length of the obtained feature is None')
        else:
            numProp = len(res[0])
            colNam_prop = [method+'_prop_'+str(i) for i in range(numProp)]
            colNam_prop.append('class')
            classColList = [1 for i in range(len(res))]
            import numpy as np
            classColArray = np.array(classColList)
            npMat = np.array(res)
            npMat_Added = np.vstack((npMat.T, classColArray.T)).T
            import pandas as pd
            df_full = pd.DataFrame(npMat_Added,columns=colNam_prop)
            return df_full,True
    else:
        return 0,False
