# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:44:49 2021

@author: tafch
"""
import sys
import math

class ErrorUser(Exception):
    pass

def main(argv):
    #判断输入参数的个数
    numOfArgv = len(argv)
    #如果为4个则为正确，否则为错误
    if numOfArgv == 4:
        pass
    else:
        raise ErrorUser('The number of parameters should be 4, please check...')
    #到此排除了不等于4个的情况，接下来进行计算
    tp = float(argv[0])
    fp = float(argv[1])
    fn = float(argv[2])
    tn = float(argv[3])
    #计算四个准确率数值
    sn = tp/(tp+fn)
    sp = tn/(tn+fp)    
    acc = (tp+tn)/(tp+fp+fn+tn)    
    mcc = (tp*tn-fp*fn)/math.sqrt((tp+fn)*(tn+fn)*(tp+fp)*(tn+fp))
    #输出值
    print('SN:'+str(sn))
    print('SP:'+str(sp))
    print('ACC:'+str(acc))
    print('MCC:'+str(mcc))
    #返回值
    return sn,sp,acc,mcc


if __name__ == "__main__":
    #带入函数
    main(sys.argv[1:])

