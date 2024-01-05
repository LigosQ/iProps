#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import pickle
from math import pow
import time
from files.util import frequency
from files.util import get_data
from files.util import check_args, read_k
from files.kmer import make_kmer_list
from files.fun_dfData2Csv import *
from files import globSet
try:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
except:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT
class ErrorUser(Exception):
    pass
def serCurPth():
    global current_path
    current_path = os.path.dirname(__file__)
    return current_path
"""Prepare for PseKNC."""
class AAIndex():
    def __init__(self, head, index_dict):
        self.head = head
        self.index_dict = index_dict
    def __str__(self):
        return "%s\n%s" % (self.head, self.index_dict)
def pseknc(input_data, k, w, lamada, phyche_list, alphabet, extra_index_file=None, all_prop=False, theta_type=1):
    """This is a complete process in PseKNC.
    :param k: int, the value of k-tuple.
    :param phyche_list: list, the input physicochemical properties list.
    :param extra_index_file: a file path includes the user-defined phyche_index.
    :param all_prop: bool, choose all physicochemical properties or not.
    """
    phyche_list = get_phyche_list(k, phyche_list,
                                  extra_index_file=extra_index_file, alphabet=alphabet, all_prop=all_prop)
    if alphabet == "ACDEFGHIKLMNPQRSTVWY":
        phyche_vals = get_aaindex(phyche_list)
        if extra_index_file is not None:
            phyche_vals.extend(extend_aaindex(extra_index_file))
    seq_list = get_data(input_data, alphabet)
    return make_pseknc_vector(seq_list, phyche_vals, k, w, lamada, alphabet, theta_type)
def ipseknc(input_data, k, w, lamada, phyche_list, alphabet, extra_index_file=None, all_prop=False):
    """This is a complete process in iPseKNC, k is kmer, but the index is just for dinucleotide.
    :param k: int, the value of k-tuple.
    :param phyche_list: list, the input physicochemical properties list.
    :param extra_index_file: a file path includes the user-defined phyche_index.
    :param all_prop: bool, choose all physicochemical properties or not.
    """
    phyche_list = get_phyche_list(k=2, phyche_list=phyche_list,
                                  extra_index_file=extra_index_file, alphabet=alphabet, all_prop=all_prop)
    if extra_index_file is not None:
        extra_phyche_index = get_extra_index(extra_index_file)
        from util import normalize_index
        phyche_vals = get_phyche_value(k=2, phyche_list=phyche_list, alphabet=alphabet,
                                       extra_phyche_index=normalize_index(extra_phyche_index, alphabet,
                                                                          is_convert_dict=True))
    else:
        phyche_vals = get_phyche_value(k=2, phyche_list=phyche_list, alphabet=alphabet)
    seq_list = get_data(input_data, alphabet)
    return make_pseknc_vector(seq_list, phyche_vals, k, w, lamada, alphabet, theta_type=3)
def get_phyche_list(k, phyche_list, extra_index_file, alphabet, all_prop=False):
    """Get phyche_list and check it.
    :param k: int, the value of k-tuple.
    :param phyche_list: list, the input physicochemical properties list.
    :param all_prop: bool, choose all physicochemical properties or not.
    """
    if phyche_list is None or len(phyche_list) == 0:
        if extra_index_file is None and all_prop is False:
            error_info = 'Error, The phyche_list, extra_index_file and all_prop can\'t be all False.'
            raise ValueError(error_info)
    all_prop_list = []
    pro_list = ['Hydrophobicity', 'Hydrophilicity', 'Mass',
                'ANDN920101', 'ARGP820101', 'ARGP820102', 'ARGP820103', 'BEGF750101', 'BEGF750102', 'BEGF750103',
                'BHAR880101', 'BIGC670101', 'BIOV880101', 'BIOV880102', 'BROC820101', 'BROC820102', 'BULH740101',
                'BULH740102', 'BUNA790101', 'BUNA790102', 'BUNA790103', 'BURA740101', 'BURA740102', 'CHAM810101',
                'CHAM820101', 'CHAM820102', 'CHAM830101', 'CHAM830102', 'CHAM830103', 'CHAM830104', 'CHAM830105',
                'CHAM830106', 'CHAM830107', 'CHAM830108', 'CHOC750101', 'CHOC760101', 'CHOC760102', 'CHOC760103',
                'CHOC760104', 'CHOP780101', 'CHOP780201', 'CHOP780202', 'CHOP780203', 'CHOP780204', 'CHOP780205',
                'CHOP780206', 'CHOP780207', 'CHOP780208', 'CHOP780209', 'CHOP780210', 'CHOP780211', 'CHOP780212',
                'CHOP780213', 'CHOP780214', 'CHOP780215', 'CHOP780216', 'CIDH920101', 'CIDH920102', 'CIDH920103',
                'CIDH920104', 'CIDH920105', 'COHE430101', 'CRAJ730101', 'CRAJ730102', 'CRAJ730103', 'DAWD720101',
                'DAYM780101', 'DAYM780201', 'DESM900101', 'DESM900102', 'EISD840101', 'EISD860101', 'EISD860102',
                'EISD860103', 'FASG760101', 'FASG760102', 'FASG760103', 'FASG760104', 'FASG760105', 'FAUJ830101',
                'FAUJ880101', 'FAUJ880102', 'FAUJ880103', 'FAUJ880104', 'FAUJ880105', 'FAUJ880106', 'FAUJ880107',
                'FAUJ880108', 'FAUJ880109', 'FAUJ880110', 'FAUJ880111', 'FAUJ880112', 'FAUJ880113', 'FINA770101',
                'FINA910101', 'FINA910102', 'FINA910103', 'FINA910104', 'GARJ730101', 'GEIM800101', 'GEIM800102',
                'GEIM800103', 'GEIM800104', 'GEIM800105', 'GEIM800106', 'GEIM800107', 'GEIM800108', 'GEIM800109',
                'GEIM800110', 'GEIM800111', 'GOLD730101', 'GOLD730102', 'GRAR740101', 'GRAR740102', 'GRAR740103',
                'GUYH850101', 'HOPA770101', 'HOPT810101', 'HUTJ700101', 'HUTJ700102', 'HUTJ700103', 'ISOY800101',
                'ISOY800102', 'ISOY800103', 'ISOY800104', 'ISOY800105', 'ISOY800106', 'ISOY800107', 'ISOY800108',
                'JANJ780101', 'JANJ780102', 'JANJ780103', 'JANJ790101', 'JANJ790102', 'JOND750101', 'JOND750102',
                'JOND920101', 'JOND920102', 'JUKT750101', 'JUNJ780101', 'KANM800101', 'KANM800102', 'KANM800103',
                'KANM800104', 'KARP850101', 'KARP850102', 'KARP850103', 'KHAG800101', 'KLEP840101', 'KRIW710101',
                'KRIW790101', 'KRIW790102', 'KRIW790103', 'KYTJ820101', 'LAWE840101', 'LEVM760101', 'LEVM760102',
                'LEVM760103', 'LEVM760104', 'LEVM760105', 'LEVM760106', 'LEVM760107', 'LEVM780101', 'LEVM780102',
                'LEVM780103', 'LEVM780104', 'LEVM780105', 'LEVM780106', 'LEWP710101', 'LIFS790101', 'LIFS790102',
                'LIFS790103', 'MANP780101', 'MAXF760101', 'MAXF760102', 'MAXF760103', 'MAXF760104', 'MAXF760105',
                'MAXF760106', 'MCMT640101', 'MEEJ800101', 'MEEJ800102', 'MEEJ810101', 'MEEJ810102', 'MEIH800101',
                'MEIH800102', 'MEIH800103', 'MIYS850101', 'NAGK730101', 'NAGK730102', 'NAGK730103', 'NAKH900101',
                'NAKH900102', 'NAKH900103', 'NAKH900104', 'NAKH900105', 'NAKH900106', 'NAKH900107', 'NAKH900108',
                'NAKH900109', 'NAKH900110', 'NAKH900111', 'NAKH900112', 'NAKH900113', 'NAKH920101', 'NAKH920102',
                'NAKH920103', 'NAKH920104', 'NAKH920105', 'NAKH920106', 'NAKH920107', 'NAKH920108', 'NISK800101',
                'NISK860101', 'NOZY710101', 'OOBM770101', 'OOBM770102', 'OOBM770103', 'OOBM770104', 'OOBM770105',
                'OOBM850101', 'OOBM850102', 'OOBM850103', 'OOBM850104', 'OOBM850105', 'PALJ810101', 'PALJ810102',
                'PALJ810103', 'PALJ810104', 'PALJ810105', 'PALJ810106', 'PALJ810107', 'PALJ810108', 'PALJ810109',
                'PALJ810110', 'PALJ810111', 'PALJ810112', 'PALJ810113', 'PALJ810114', 'PALJ810115', 'PALJ810116',
                'PARJ860101', 'PLIV810101', 'PONP800101', 'PONP800102', 'PONP800103', 'PONP800104', 'PONP800105',
                'PONP800106', 'PONP800107', 'PONP800108', 'PRAM820101', 'PRAM820102', 'PRAM820103', 'PRAM900101',
                'PRAM900102', 'PRAM900103', 'PRAM900104', 'PTIO830101', 'PTIO830102', 'QIAN880101', 'QIAN880102',
                'QIAN880103', 'QIAN880104', 'QIAN880105', 'QIAN880106', 'QIAN880107', 'QIAN880108', 'QIAN880109',
                'QIAN880110', 'QIAN880111', 'QIAN880112', 'QIAN880113', 'QIAN880114', 'QIAN880115', 'QIAN880116',
                'QIAN880117', 'QIAN880118', 'QIAN880119', 'QIAN880120', 'QIAN880121', 'QIAN880122', 'QIAN880123',
                'QIAN880124', 'QIAN880125', 'QIAN880126', 'QIAN880127', 'QIAN880128', 'QIAN880129', 'QIAN880130',
                'QIAN880131', 'QIAN880132', 'QIAN880133', 'QIAN880134', 'QIAN880135', 'QIAN880136', 'QIAN880137',
                'QIAN880138', 'QIAN880139', 'RACS770101', 'RACS770102', 'RACS770103', 'RACS820101', 'RACS820102',
                'RACS820103', 'RACS820104', 'RACS820105', 'RACS820106', 'RACS820107', 'RACS820108', 'RACS820109',
                'RACS820110', 'RACS820111', 'RACS820112', 'RACS820113', 'RACS820114', 'RADA880101', 'RADA880102',
                'RADA880103', 'RADA880104', 'RADA880105', 'RADA880106', 'RADA880107', 'RADA880108', 'RICJ880101',
                'RICJ880102', 'RICJ880103', 'RICJ880104', 'RICJ880105', 'RICJ880106', 'RICJ880107', 'RICJ880108',
                'RICJ880109', 'RICJ880110', 'RICJ880111', 'RICJ880112', 'RICJ880113', 'RICJ880114', 'RICJ880115',
                'RICJ880116', 'RICJ880117', 'ROBB760101', 'ROBB760102', 'ROBB760103', 'ROBB760104', 'ROBB760105',
                'ROBB760106', 'ROBB760107', 'ROBB760108', 'ROBB760109', 'ROBB760110', 'ROBB760111', 'ROBB760112',
                'ROBB760113', 'ROBB790101', 'ROSG850101', 'ROSG850102', 'ROSM880101', 'ROSM880102', 'ROSM880103',
                'SIMZ760101', 'SNEP660101', 'SNEP660102', 'SNEP660103', 'SNEP660104', 'SUEM840101', 'SUEM840102',
                'SWER830101', 'TANS770101', 'TANS770102', 'TANS770103', 'TANS770104', 'TANS770105', 'TANS770106',
                'TANS770107', 'TANS770108', 'TANS770109', 'TANS770110', 'VASM830101', 'VASM830102', 'VASM830103',
                'VELV850101', 'VENT840101', 'VHEG790101', 'WARP780101', 'WEBA780101', 'WERD780101', 'WERD780102',
                'WERD780103', 'WERD780104', 'WOEC730101', 'WOLR810101', 'WOLS870101', 'WOLS870102', 'WOLS870103',
                'YUTK870101', 'YUTK870102', 'YUTK870103', 'YUTK870104', 'ZASB820101', 'ZIMJ680101', 'ZIMJ680102',
                'ZIMJ680103', 'ZIMJ680104', 'ZIMJ680105', 'AURR980101', 'AURR980102', 'AURR980103', 'AURR980104',
                'AURR980105', 'AURR980106', 'AURR980107', 'AURR980108', 'AURR980109', 'AURR980110', 'AURR980111',
                'AURR980112', 'AURR980113', 'AURR980114', 'AURR980115', 'AURR980116', 'AURR980117', 'AURR980118',
                'AURR980119', 'AURR980120', 'ONEK900101', 'ONEK900102', 'VINM940101', 'VINM940102', 'VINM940103',
                'VINM940104', 'MUNV940101', 'MUNV940102', 'MUNV940103', 'MUNV940104', 'MUNV940105', 'WIMW960101',
                'KIMC930101', 'MONM990101', 'BLAM930101', 'PARS000101', 'PARS000102', 'KUMS000101', 'KUMS000102',
                'KUMS000103', 'KUMS000104', 'TAKK010101', 'FODM020101', 'NADH010101', 'NADH010102', 'NADH010103',
                'NADH010104', 'NADH010105', 'NADH010106', 'NADH010107', 'MONM990201', 'KOEP990101', 'KOEP990102',
                'CEDJ970101', 'CEDJ970102', 'CEDJ970103', 'CEDJ970104', 'CEDJ970105', 'FUKS010101', 'FUKS010102',
                'FUKS010103', 'FUKS010104', 'FUKS010105', 'FUKS010106', 'FUKS010107', 'FUKS010108', 'FUKS010109',
                'FUKS010110', 'FUKS010111', 'FUKS010112', 'AVBF000101', 'AVBF000102', 'AVBF000103', 'AVBF000104',
                'AVBF000105', 'AVBF000106', 'AVBF000107', 'AVBF000108', 'AVBF000109', 'YANJ020101', 'MITS020101',
                'TSAJ990101', 'TSAJ990102', 'COSI940101', 'PONP930101', 'WILM950101', 'WILM950102', 'WILM950103',
                'WILM950104', 'KUHL950101', 'GUOD860101', 'JURD980101', 'BASU050101', 'BASU050102', 'BASU050103',
                'SUYM030101', 'PUNT030101', 'PUNT030102', 'GEOR030101', 'GEOR030102', 'GEOR030103', 'GEOR030104',
                'GEOR030105', 'GEOR030106', 'GEOR030107', 'GEOR030108', 'GEOR030109', 'ZHOH040101', 'ZHOH040102',
                'ZHOH040103', 'BAEK050101', 'HARY940101', 'PONJ960101', 'DIGM050101', 'WOLR790101', 'OLSK800101',
                'KIDA850101', 'GUYH850102', 'GUYH850103', 'GUYH850104', 'GUYH850105', 'ROSM880104', 'ROSM880105',
                'JACR890101', 'COWR900101', 'BLAS910101', 'CASG920101', 'CORJ870101', 'CORJ870102', 'CORJ870103',
                'CORJ870104', 'CORJ870105', 'CORJ870106', 'CORJ870107', 'CORJ870108', 'MIYS990101', 'MIYS990102',
                'MIYS990103', 'MIYS990104', 'MIYS990105', 'ENGD860101', 'FASG890101']
    try:
        if alphabet == "ACDEFGHIKLMNPQRSTVWY":
            all_prop_list = pro_list
        else:
            error_info = "Error, the alphabet must be dna, rna or protein."
            raise ValueError(error_info)
    except:
        raise
    try:
        if all_prop is True:
            phyche_list = all_prop_list
        else:
            for e in phyche_list:
                if e not in all_prop_list:
                    error_info = 'Sorry, the physicochemical properties ' + e + ' is not exit.'
                    raise NameError(error_info)
    except:
        raise
    return phyche_list
def get_extra_index(filename):
    """Get the extend indices from index file, only work for DNA and RNA."""
    extra_index_vals = []
    with open(filename) as f:
        lines = f.readlines()
        for ind, line in enumerate(lines):
            if line[0] == '>':
                vals = lines[ind + 2].rstrip().split('\t')
                vals = [float(val) for val in vals]
                extra_index_vals.append(vals)
    return extra_index_vals
def get_aaindex(index_list):
    """Get the aaindex from data/aaindex.data.
    :param index_list: the index we want to get.
    :return: a list of AAIndex obj.
    """
    new_aaindex = []
    # current_path = serCurPth()
    # with open(current_path+'/data/aaindex.data', 'rb') as f:
    #     aaindex = pickle.load(f)
    #     for index_vals in aaindex:
    #         if index_vals.head in index_list:
    #             new_aaindex.append(index_vals)
    p_aaindexPth = f_geneAbsPath_frmROOT('data','aaindex.data')
    with open(p_aaindexPth, 'rb') as f:
        aaindex = pickle.load(f)
        for index_vals in aaindex:
            if index_vals.head in index_list:
                new_aaindex.append(index_vals)
    return new_aaindex
def extend_aaindex(filename):
    """Extend the user-defined AAIndex from user's file.
    :return: a list of AAIndex obj.
    """
    from scrip.extract_aaindex import extra_aaindex, norm_index_vals
    aaindex = extra_aaindex(filename)
    for ind, e in enumerate(aaindex):
        aaindex[ind] = AAIndex(e.head, norm_index_vals(e.index_dict))
    return aaindex
def get_ext_ind_pro(filename):
    """Get the extend indices from index file, only work for protein."""
    inds = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    aaindex = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line[0] == '>':
                temp_name = line[1:].rstrip()
                vals = lines[i + 2].rstrip().split('\t')
                ind_val = {ind: float(val) for ind, val in zip(inds, vals)}
                aaindex.append(AAIndex(temp_name, ind_val))
    return aaindex
def get_phyche_value(k, phyche_list, alphabet, extra_phyche_index=None):
    """Generate DNA or RNA phyche_value.
    :param k: int, the value of k-tuple.
    :param phyche_list: physicochemical properties list.
    :param extra_phyche_index: dict, the key is the olinucleotide (string),
                                     the value is its physicochemical property value (list).
                               It means the user-defined physicochemical indices.
    """
    if extra_phyche_index is None:
        extra_phyche_index = {}
    phyche_value = extend_phyche_index(get_phyche_index(k, phyche_list, alphabet), extra_phyche_index)
    return phyche_value
def get_phyche_index(k, phyche_list, alphabet):
    """get phyche_value according phyche_list."""
    phyche_value = {}
    if 0 == len(phyche_list):
        for nucleotide in make_kmer_list(k, alphabet):
            phyche_value[nucleotide] = []
        return phyche_value
    nucleotide_phyche_value = get_phyche_factor_dic(k, alphabet)
    for nucleotide in make_kmer_list(k, alphabet):
        if nucleotide not in phyche_value:
            phyche_value[nucleotide] = []
        for e in nucleotide_phyche_value[nucleotide]:
            if e[0] in phyche_list:
                phyche_value[nucleotide].append(e[1])
    return phyche_value
"""Calculate PseKNC."""
def parallel_cor_function(nucleotide1, nucleotide2, phyche_index):
    """Get the cFactor.(Type1)"""
    temp_sum = 0.0
    phyche_index_values = list(phyche_index.values())
    len_phyche_index = len(phyche_index_values[0])
    for u in range(len_phyche_index):
        temp_sum += pow(float(phyche_index[nucleotide1][u]) - float(phyche_index[nucleotide2][u]), 2)
    return temp_sum / len_phyche_index
def series_cor_function(nucleotide1, nucleotide2, big_lamada, phyche_value):
    """Get the series correlation Factor(Type 2)."""
    return float(phyche_value[nucleotide1][big_lamada]) * float(phyche_value[nucleotide2][big_lamada])
def pro_cor_fun1(ri, rj, aaindex_list):
    _sum = 0.0
    len_index = len(aaindex_list)
    for aaindex in aaindex_list:
        _sum += pow(aaindex.index_dict[ri] - aaindex.index_dict[rj], 2)
    return _sum / len_index
def pro_cor_fun2(ri, rj, aaindex):
    return aaindex.index_dict[ri] * aaindex.index_dict[rj]
def get_parallel_factor(k, lamada, sequence, phyche_value, alphabet):
    """Get the corresponding factor theta list."""
    theta = []
    l = len(sequence)
    for i in range(1, lamada + 1):
        temp_sum = 0.0
        for j in range(0, l - k - i + 1):
            nucleotide1 = sequence[j: j + k]
            nucleotide2 = sequence[j + i: j + i + k]
            if alphabet == "ACGT" or alphabet == "ACGU":
                temp_sum += parallel_cor_function(nucleotide1, nucleotide2, phyche_value)
            elif alphabet == "ACDEFGHIKLMNPQRSTVWY":
                temp_sum += pro_cor_fun1(nucleotide1, nucleotide2, phyche_value)
        theta.append(temp_sum / (l - k - i + 1))
    return theta
def get_series_factor(k, lamada, sequence, phyche_value, alphabet):
    """Get the corresponding series factor theta list."""
    theta = []
    l_seq = len(sequence)
    if alphabet == "ACGT" or alphabet == "ACGU":
        temp_values = list(phyche_value.values())
        max_big_lamada = len(temp_values[0])
    elif alphabet == "ACDEFGHIKLMNPQRSTVWY":
        max_big_lamada = len(phyche_value)
    for small_lamada in range(1, lamada + 1):
        for big_lamada in range(max_big_lamada):
            temp_sum = 0.0
            for i in range(0, l_seq - k - small_lamada + 1):
                nucleotide1 = sequence[i: i + k]
                nucleotide2 = sequence[i + small_lamada: i + small_lamada + k]
                if alphabet == "ACGT" or alphabet == "ACGU":
                    temp_sum += series_cor_function(nucleotide1, nucleotide2, big_lamada, phyche_value)
                elif alphabet == "ACDEFGHIKLMNPQRSTVWY":
                    temp_sum += pro_cor_fun2(nucleotide1, nucleotide2, phyche_value[big_lamada])
            theta.append(temp_sum / (l_seq - k - small_lamada + 1))
    return theta
def make_pseknc_vector(sequence_list, phyche_value, k=2, w=0.05, lamada=1, alphabet="ACGT", theta_type=1):
    """Generate the pseknc vector."""
    kmer = make_kmer_list(k, alphabet)
    vector = []
    for sequence in sequence_list:
        if len(sequence) < k or lamada + k > len(sequence):
            error_info = "Sorry, the sequence length must be larger than " + str(lamada + k)
            sys.stderr.write(error_info)
            sys.exit(0)
        fre_list = [frequency(sequence, str(key)) for key in kmer]
        fre_sum = float(sum(fre_list))
        fre_list = [e / fre_sum for e in fre_list]
        if 1 == theta_type:
            theta_list = get_parallel_factor(k, lamada, sequence, phyche_value, alphabet)
        elif 2 == theta_type:
            theta_list = get_series_factor(k, lamada, sequence, phyche_value, alphabet)
        elif 3 == theta_type:
            theta_list = get_parallel_factor(k=2, lamada=lamada, sequence=sequence,
                                             phyche_value=phyche_value, alphabet=alphabet)
        theta_sum = sum(theta_list)
        denominator = 1 + w * theta_sum
        temp_vec = [round(f / denominator, 8) for f in fre_list]
        for theta in theta_list:
            temp_vec.append(round(w * theta / denominator, 8))
        vector.append(temp_vec)
    return vector
def read_index(index_file):
    with open(index_file) as f_ind:
        lines = f_ind.readlines()
        ind_list = [index.rstrip() for index in lines]
        return ind_list
def myfun_calcPseProp(fastafile,outfile,method,weight,vlambda,lable=1):
    args_K = 1
    args_e = None
    args_a = None
    try:
        d_allParas
    except:
        d_allParas = globSet.getGlobParas()
    else:
        if len(d_allParas)==1:
            d_allParas = globSet.getGlobParas()
    with open(fastafile) as f:
        ind_list = []
        default_e = []
        Alphabet = "ACDEFGHIKLMNPQRSTVWY"
        default_e = ['Hydrophobicity', 'Hydrophilicity', 'Mass']
        theta_type = 1
        if method in ['PseDNC', 'PC-PseDNC-General', 'PC-PseTNC-General', 'PC-PseAAC', 'PC-PseAAC-General']:
            theta_type = 1
        elif method in ['SC-PseDNC-General', 'SC-PseTNC-General', 'SC-PseAAC', 'SC-PseAAC-General']:
            theta_type = 2
        elif method == 'PseKNC':
            theta_type = 3
        else:
            print("Method error!")
        if args_e is None and len(ind_list) == 0 and args_a is False:
            res = pseknc(f, args_K, weight, vlambda, default_e, Alphabet,
                             extra_index_file=args_e, all_prop=args_a, theta_type=theta_type)
        else:
            res = pseknc(f, args_K, weight, vlambda, ind_list, Alphabet,
                             extra_index_file=args_e, all_prop=args_a, theta_type=theta_type)
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
        writeDf2csv(df_full,outfile)
    return True
