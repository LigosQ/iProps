#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 22:12:28 2023

@author: sealight
"""
import pandas as pd
import numpy as np
import argparse
import json
# import pysnooper

#Define a class: Error Type
class ErrorCoding(Exception):
    pass

def f_findTypeColName(ls_allColNames):
    #iteration
    for s_1colName in ls_allColNames:
        s_1colName_lower = s_1colName.lower()
        if (s_1colName_lower=='class') or (s_1colName_lower=='target'):
            return s_1colName
        else:
            pass
    #Iteration done. Results: Not find the class or target column name.
    #return None
    return None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def f_isTypeLabContainNum(ls_typeColVals):
    for item in ls_typeColVals:
        if is_number(item):
            #True: is a number
            return True
        else:
            #not a number
            pass
    #iteration done
    #return value
    return False

# def f_isAllIntType_inClsCol(ls_classColVals):
#     for item in ls_classColVals:
#         if is_number()
#         if isinstance(item, int):
#             pass
#         else:
#             return False
        
        
        
# @pysnooper.snoop()
def fun_chgCsv2Arff(infilePth,outfilePth):
    ##read the input file data
    df_csvData = pd.read_csv(infilePth)
    #open the output file
    fid_w = open(outfilePth,'w')
    #get the original all column name list 
    ls_origColNames = df_csvData.columns.values.tolist()
    #get the name of the class/type column
    s_origLabelOfTypeCol = f_findTypeColName(ls_origColNames)
    #get the dataframe removed the class/type column
    df_csvData_noClsCol = df_csvData.drop(columns=[s_origLabelOfTypeCol])
    #get the class/type column value
    if s_origLabelOfTypeCol is None:
        raise ErrorCoding('The current version only support "class" or "target" to label the data type')
    else:
        ls_valInClassCol = df_csvData[s_origLabelOfTypeCol]
    #change the list to set
    set_classCol = set(ls_valInClassCol)
    #get the number of label words
    i_labelWordNum = len(set_classCol)
    #check whether the class types is string types
    # b_isTypeColContainNum = f_isTypeLabContainNum(list(set_classCol))
    # b_needAlterTypeStr = b_isTypeColContainNum
    # #build the alternative type string dict
    # if b_needAlterTypeStr:
    #     if i_labelWordNum==2:
    #         if set_classCol=={0,1}:
    #             ls_alterStrTypes = ['Positive','Negative']
    #             d_alterStr_types = dict()
    #             d_alterStr_types['0']='Negative'
    #             d_alterStr_types['1']='Positive'
    #         else:
    #             raise ErrorCoding('Binary classification only supports {0,1} as category identification, please check the category column')
    #     elif i_labelWordNum>=3:
    #         ls_uniqueTypeVals = sorted(list(set_classCol))
    #         # ls_uniqueTypeVals_str = [str(ls_uniqueTypeVals[i]) for i in range(len(ls_uniqueTypeVals))]
    #         ls_alterStrTypes = [''.join(['Type',str(i)]) for i in range(i_labelWordNum)]
    #         d_alterStr_types = dict()
    #         for i in range(i_labelWordNum):
    #             d_alterStr_types[str(ls_uniqueTypeVals[i])] = ls_alterStrTypes[i]
    #         #
    #         # print(d_alterStr_types)
    #     else:
    #         raise ErrorCoding('There is only one type in the class column, the subsequent algorithm does not support the case of only one category')
    # else:
    #     d_alterStr_types = dict()
    #     ls_alterStrTypes = list(set_classCol)
    #     d_alterStr_types = dict(zip(ls_alterStrTypes,ls_alterStrTypes))
    ls_uniqStrTypes = list(set_classCol)
    ls_uniqType_str = [str(ls_uniqStrTypes[i]) for i in range(i_labelWordNum)]
    ls_alterStrTypes = [''.join(['Type_', str(ls_uniqStrTypes[i])]) for i in range(i_labelWordNum)]
    d_alterStr_types = dict(zip(ls_uniqType_str,ls_alterStrTypes))
    s_jsonFileName = 'classSubstPairs.json'
    # jsonInfo_substPair = json.dumps(d_alterStr_types)
    with open(s_jsonFileName, 'w') as fid:
        json.dump(d_alterStr_types, fid)  # 会在目录下生成一个1.json的文件，文件内容是dict数据转成的json数据
    #the type string in the arff file
    s_tempTypeStr = ','.join(ls_alterStrTypes)
    s_typeLabInHeader = ''.join(['{',s_tempTypeStr ,'}'])
    #write data
    #Writting the first line
    fid_w.write('@Relation Data_feature\n')
    #iteration write the column names
    ls_colNames_noCls = df_csvData_noClsCol.columns.values.tolist()
    for i in range(len(ls_colNames_noCls)):
        s_curColName = ls_colNames_noCls[i]
        fid_w.write('@attribute '+s_curColName+' real\n')
    #all feature column names have been writen
    #write the class/type column label of  arff file
    fid_w.write(''.join(['@attribute class',s_typeLabInHeader,'\n']))
    #write the data to the file
    fid_w.write('@data\n')
    #iteration for writing the data in each row to the arff file
    i_roundNum = 6
    for i_row in range(df_csvData_noClsCol.shape[0]):
        ser_data_row_i = df_csvData_noClsCol.iloc[i_row].round(i_roundNum)
        #change data to the number
        s_serData2Str = [str(ser_data_row_i[i]) for i in range(len(ser_data_row_i))]
        s_data_row_i = ','.join(s_serData2Str)
        #adding the type/class label
        s_final_row_i = ''.join([s_data_row_i,',', d_alterStr_types[str(ls_valInClassCol[i_row])], '\n'])
        #wring to the file
        fid_w.write(s_final_row_i)
    #done
    #close the file
    fid_w.close()

def main():
    parser = argparse.ArgumentParser(description="Transfrom the csv file to arff format")
    parser.add_argument('-i', '--infile', help="The input file should be csv format, other file types are not supported at present", required=True)
    parser.add_argument('-o', '--outfile', help='The name of output picture: .arff type', required=True)
    args = parser.parse_args()
    
    #using the function to operate
    fun_chgCsv2Arff(args.infile, args.outfile)

if __name__ == "__main__":
    main()
    
# s_in = 'abnorm_add3types.csv'
# s_o = 'abnorm_add3types.arff'
# fun_chgCsv2Arff(s_in, s_o)
