#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:55:18 2022

@author: sealight
"""
import flet as ft
import random
import time
import sys, os,zipfile
sys.path.append("files")
from threading import Timer
from files.f_checkValidation import f_checkParas
from files.fun_multiProcess import *
from files.getDoneTaskNum import f_getDoneTaskNum
from files.FS_process import *
from files import globSet
import warnings

global s_selectedProps

class ErrorCoding(Exception):
    pass

def main(page: ft.Page):
    #
    warnings.filterwarnings('ignore')
    page.title='iProp Ver 0.7'
    page.bgcolor="#f2f2f3"#f2f2f3
    page.window_width=930
    page.window_height=870
    theme = ft.Theme()
    theme.page_transitions.android = "openUpwards"
    theme.page_transitions.ios = "cupertino"
    theme.page_transitions.macos = "fadeUpwards"
    theme.page_transitions.linux = "zoom"
    theme.page_transitions.windows = "zoom"
    page.theme = theme
    page.scroll = "adaptive"
    page.session.set('i_lenCsv', 0)
    globSet._init()
    global d_allParas
    d_allParas = globSet.getGlobParas()

    def initRootPth():
        curWorkPth_abs = os.getcwd()
        curWorkPth_abs = str(curWorkPth_abs)
        s_osInfo = platform.platform().lower()
        globSet.set_rootPth(curWorkPth_abs)
        globSet.set_pcPlatformInfo(s_osInfo)
    #
    initRootPth()
    
    d_dispStatusIn4 = {
        'Tsne'
        }
    
    
    #1. pick files dialog
    def pick_posflies_result(e: ft.FilePickerResultEvent):
        #
        selected_posfiles.value=(
            ",".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_posfiles.update()
        #s_posName=e.files[0].path
        page.session.set("posFullPth", e.files[0].path)
        
    pick_posfiles_dialog = ft.FilePicker(on_result=pick_posflies_result)
    selected_posfiles = ft.Text()
    
    #1. Negative files
    def pick_negflies_result(e: ft.FilePickerResultEvent):
        #
        selected_negfiles.value=(
            ",".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_negfiles.update()
        page.session.set("negFullPth", e.files[0].path)
        
    pick_negfiles_dialog = ft.FilePicker(on_result=pick_negflies_result)
    selected_negfiles = ft.Text()
    
    # hide all dialogs in overlay
    page.overlay.extend([pick_posfiles_dialog,pick_negfiles_dialog])
    
    #1
    def f_getResampMethd(e):
        s_resampMethod = dd_resamp.value
        page.session.set("s_resampMethd", s_resampMethod)
    
    #1 the resampling method
    dd_resamp = ft.Dropdown(
        width=220,
        options=[
            ft.dropdown.Option("Under sampling"),
            ft.dropdown.Option("Over sampling"),
            ft.dropdown.Option("Under+Over sampling"),
            ft.dropdown.Option("None. Using oirginal data.")
         ],
        on_change=f_getResampMethd,
     )
    
    #1
    def f_getClassifier(e):
        s_classifier = rad_clasfier.value
        page.session.set("s_classifier", s_classifier)
    def f_setFeatEvalClfer(e):
        s_classifier = rad_clasfier.value
        page.session.set("s_classifier", s_classifier)
    def f_getFeatNumberInComb(e):
        s_featNumInComb = rad_featNum.value
        # print(s_featNumInComb)
        if s_featNumInComb in ['1','2','3','4']:
            page.session.set("s_featNumber", int(s_featNumInComb))
        else:
            print('The feature number in feat-combination is wrong, its value is set to be one currently.')
            page.session.set("s_featNumber", 1)
    #0
    logoElem = ft.Image(
        src_base64="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",
        width=171,
        height=72,
        fit="contain",
        repeat="noRepeat",
    )
    logoRow = ft.Row([logoElem],alignment=ft.MainAxisAlignment.CENTER)
    #0
    # The introduction for iProp-p
    dv_intro = ft.Text((
    'iProp-p is an automatic evaluation software for numerical characterization of a given protein sequence.\r\n'
    'In this version, iProp-p implements the processing of unbalanced data, the setting of different evaluation classifiers and'
    'the calculation of different protein numerical features. In particular, for ORAAC features, the code automatically '
    'calculates and evaluates the classification performance of more than 600 approximate schemes and then obtains the '
    'optimal approximate numerical features.\r\n'
    'Other properties include 188D, ACC, AC, CC, Moran,Geary, Nmbroto, Socnumber, Qsorder, SC-PseAAC-General, SC-PseAAC et al.'
    'The details of these properties can be found in the user\'s manual or the help section of the software.\r\n'
    'The functions of several components in the left column of this software are as follows:\r\n'
    '1. Start: set positive and negative sample sequence files, set parameters such as sampling method and numerical feature type;\r\n'
    '2. Progress: Get the calculation progress of the software;\r\n'
    '3. Results: View the related numerical files obtained by the software;\r\n'
    '4. Visulization: visualization of the obtained results;\r\n'
    '5. Feat-selection: Feature selection to simplify the model;\r\n'
    '6. Performace: Show the identification ability.\r\n'
    '7. ExtractFiles: Getting results, pictures, etc. related to this calculation task.\r\n'
    '8. Help: Get help information.'
    ))
    dv_horDivier = ft.Container(width=600,height=2, bgcolor="#cccccc")#5d6471
    dv_cite = ft.Text((
    'Cite our paper:\r\n'
    'Feng Changli, Wu Jin, Wei Haiyan, Xu Lei, Zou Quan. CRCF: A Method of Identifying Secretory Proteins of Malaria Parasites. '
    'IEEE/ACM Trans Comput Biol Bioinform. 2022 Jul-Aug;19(4):2149-2157. doi: 10.1109/TCBB.2021.3085589. '
    'Epub 2022 Aug 8. PMID: 34061749.'
    ),color="#000000",size=15)
    sec_intro = ft.Column(
        width=800,
        height=750,
        controls=[
            logoRow,
            dv_intro,
            dv_horDivier,
            dv_cite,
        ],        
    )
    
    #1 the property of proteins
    cb_raac=ft.Checkbox(label="ORDip", value=False,fill_color={"selected":"#4FCDC5"})
    cb_188d=ft.Checkbox(label="188D", value=False,fill_color={"selected":"#4FCDC5"})
    cb_ACC=ft.Checkbox(label="ACC",value=False,fill_color={"selected":"#4FCDC5"})
    
    cb_CC=ft.Checkbox(label="CC",value=False,fill_color={"selected":"#4FCDC5"})
    cb_AC=ft.Checkbox(label="AC",value=False,fill_color={"selected":"#4FCDC5"})
    cb_Moran=ft.Checkbox(label="Moran",value=False,fill_color={"selected":"#4FCDC5"})
    
    cb_Geary=ft.Checkbox(label="Geary",value=False,fill_color={"selected":"#4FCDC5"})
    cb_nmbroto=ft.Checkbox(label="Nmbroto",value=False,fill_color={"selected":"#4FCDC5"})
    cb_Socnumber=ft.Checkbox(label="Socnumber",value=False,fill_color={"selected":"#4FCDC5"})
    
    cb_Qsorder=ft.Checkbox(label="Qsorder",value=False,fill_color={"selected":"#4FCDC5"})
    cb_PseAAC_General=ft.Checkbox(label="SCPseAAC-G",value=False,fill_color={"selected":"#4FCDC5"})
    cb_SC_PseAAC=ft.Checkbox(label="SC-PseAAC",value=False,fill_color={"selected":"#4FCDC5"})
    
    cb_CKSAAGP=ft.Checkbox(label="CKSAAGP",value=False,fill_color={"selected":"#4FCDC5"})
    # cb_CKSAAGP=ft.TextField(label="CKSAAGP",value="(1~568)",keyboard_type=ft.KeyboardType.NUMBER,max_length=3)
    cb_CKSAAP=ft.Checkbox(label="CKSAAP",value=False,fill_color={"selected":"#4FCDC5"})
    cb_PAAC=ft.Checkbox(label="PAAC",value=False,fill_color={"selected":"#4FCDC5"})
    
    cb_CTDC=ft.Checkbox(label="CTDC",value=False,fill_color={"selected":"#4FCDC5"}) 
    cb_CTDD=ft.Checkbox(label="CTDD",value=False,fill_color={"selected":"#4FCDC5"})
    cb_CTDT=ft.Checkbox(label="CTDT",value=False,fill_color={"selected":"#4FCDC5"})

    cb_DDE=ft.Checkbox(label="DDE",value=False,fill_color={"selected":"#4FCDC5"})
    cb_trip=ft.Checkbox(label="rTrip",value=False, fill_color={"selected":"#4FCDC5"})
    
    cb_usrCsv=ft.Checkbox(label="UserFeature",value=False, fill_color={"selected":"#4FCDC5"})
    # cb_usrCsv.disabled = True
    
    cb_ASDC = ft.Checkbox(label="ASDC",value=False,fill_color={"selected":"#4FCDC5"})
    cb_EAAC = ft.Checkbox(label="EAAC",value=False,fill_color={"selected":"#4FCDC5"})
    cb_APAAC = ft.Checkbox(label="APAAC",value=False,fill_color={"selected":"#4FCDC5"})
    
    # cb_nmbroto.disabled = True
    
    # rad_clasfier = ft.RadioGroup(
    #     content=ft.Row(
    #         [
    #             ft.Radio(value="Random Forest", label="RF",fill_color={"selected":"#4FCDC5"}),
    #             ft.Radio(value="RBF SVM", label="SVM",fill_color={"selected":"#4FCDC5"}),
    #             ft.Radio(value="Gaussian Process", label="Gaussian",fill_color={"selected":"#4FCDC5"}),
    #             ft.Radio(value="Naive Bayes", label="Bayes",fill_color={"selected":"#4FCDC5"}),
    #             ft.Radio(value="xgboost", label="Xgboost",fill_color={"selected":"#4FCDC5"}),
    #         ],
    #     ),
    #     on_change=f_getClassifier,
    # )
    rad_clasfier = ft.Dropdown(
        width=220,
        options=[
            ft.dropdown.Option("Nearest Neighbors"),
            ft.dropdown.Option("SVM(linear)"),
            ft.dropdown.Option("RBF SVM"),
            ft.dropdown.Option("Gaussian Process"),
            ft.dropdown.Option("Decision Tree"),
            ft.dropdown.Option("Random Forest"),
            ft.dropdown.Option("Neural Net"),
            ft.dropdown.Option("AdaBoost"),
            ft.dropdown.Option("Naive Bayes"),
            ft.dropdown.Option("QDA"),
            ft.dropdown.Option("xgboost"),
            ft.dropdown.Option("lightGBM"),
            ft.dropdown.Option('Gradient Boosting Classifier'),
            ft.dropdown.Option('SVC'),
            ft.dropdown.Option('ExtraTreesClassifier'),
            ft.dropdown.Option('SGDClassifier'),
            ft.dropdown.Option('BernoulliNB'),
            ft.dropdown.Option('Perceptron'),
            ft.dropdown.Option('PassiveAggressiveClassifier'),
            ft.dropdown.Option('BaggingClassifier'),
            ft.dropdown.Option('CalibratedClassifierCV'),
            ft.dropdown.Option('ExtraTreeClassifier'),
            ft.dropdown.Option('LinearDiscriminantAnalysis'),
            ft.dropdown.Option('LabelSpreading'),
            ft.dropdown.Option('LabelPropagation'),
            ft.dropdown.Option('DummyClassifier')
            ],
        on_change=f_setFeatEvalClfer,
        )
    rad_featNum = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="1", label="1",fill_color={"selected":"#4FCDC5"}),
                ft.Radio(value="2", label="2",fill_color={"selected":"#4FCDC5"}),
                ft.Radio(value="3", label="3",fill_color={"selected":"#4FCDC5"}),
                ft.Radio(value="4", label="4",fill_color={"selected":"#4FCDC5"}),
            ],
        ),
        on_change=f_getFeatNumberInComb,
    )
    
    #1->end function: get the selected proeprties
    def f_getSelctedProps(e):
        #all The
        ls_propsNames = ["optiRaac","188d","ACC","CC","AC","Moran","Geary","nmbroto",
                         "Socnumber","Qsorder","SC-PseAAC-General","SC-PseAAC",
                         "CKSAAGP","CKSAAP","PAAC","CTDC","CTDD","CTDT","DDE",
                         "rTripComp",'userGivenFeat','ASDC','EAAC','APAAC']
        #user selection status: boolean variable
        ls_radioOptionsVals = [cb_raac.value,cb_188d.value,cb_ACC.value,cb_CC.value,cb_AC.value,
                           cb_Moran.value,cb_Geary.value,cb_nmbroto.value,cb_Socnumber.value,
                           cb_Qsorder.value,cb_PseAAC_General.value,cb_SC_PseAAC.value,
                           cb_CKSAAGP.value,cb_CKSAAP.value,cb_PAAC.value,
                           cb_CTDC.value,cb_CTDD.value,cb_CTDT.value,cb_DDE.value,
                           cb_trip.value,cb_usrCsv.value,cb_ASDC.value,cb_EAAC.value,
                           cb_APAAC.value]
        #fast list generator
        ls_selectedPropsStr = []
        for i in range(len(ls_radioOptionsVals)):
            if ls_radioOptionsVals[i]:
                ls_selectedPropsStr.append(ls_propsNames[i])
            else:
                pass
        #change to a string format
        s_selectedProps = ','.join(ls_selectedPropsStr)
        return s_selectedProps
    
    #1 function: generate a id with 6 number or alphabets
    def f_geneTimeId():
        s_time = time.strftime("%m%d%H%M%S",time.localtime())
        return s_time         
        
    
    #1 spliter
    obj_empty20 = ft.Container(width=26)
    
    #1.显示问题的提示框
    text_problems = ft.Text("")
    
    #1.左侧的提示框
    obj_infoScreen_left = ft.Container(
        width=270,
        padding=3,
        height=270,
        content=text_problems,
        alignment=ft.alignment.top_left,
        bgcolor="#f2f2f3",
        visible=True,
    )
    
    #1.右侧的蛋白质特征列表
    obj_Props9_r = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_CC,
                    ft.Container(width=49),
                    cb_AC,
                    ft.Container(width=36),
                    cb_Moran,  
                 ]
             ),
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_nmbroto,
                    ft.Container(width=10),
                    cb_Geary,
                    ft.Container(width=15),
                    cb_Socnumber,
                 ]
             ),
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_Qsorder,
                    ft.Container(width=14),
                    cb_PseAAC_General,
                    ft.Container(width=0),
                    cb_usrCsv,
                 ]
             ),
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_PAAC,
                    ft.Container(width=32),
                    cb_CTDC,
                    ft.Container(width=16),
                    cb_CTDD,
                 ]
             ),
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_CTDT,
                    ft.Container(width=31),
                    cb_DDE,
                    ft.Container(width=26),
                    cb_SC_PseAAC,
                 ]
             ),
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_CKSAAGP,
                    ft.Container(width=2),
                    cb_CKSAAP,
                    ft.Container(width=0),
                    cb_trip,
                 ]
             ),
            ft.Row(
                [
                    ft.Container(width=10),
                    cb_ASDC,
                    ft.Container(width=31),
                    cb_EAAC,
                    ft.Container(width=17),
                    cb_APAAC,
                 ]
             ),
        ],
    )
        
    #1. function: obtain user input and start calculation
    def f_calcProps(e):
        para_id = f_geneTimeId()
        try:
            if isinstance(para_id, str) and (not((para_id=='') or (para_id is None))):
                page.session.set('taskID', para_id)
            else:
                if (para_id is None):
                    raise ErrorCoding("taskID is None.")
                elif para_id=='':
                    raise ErrorCoding("taskID is a empty string.")
                else:
                    raise ErrorCoding("taskID is a unknown type.")
        except:
            raise ErrorCoding("An error occurred while setting up taskID。")
        
        #obtain 5 paremeter values
        para_pos = page.session.get("posFullPth")
        para_neg = page.session.get("negFullPth")
        para_sample = page.session.get("s_resampMethd")
        para_clfier = page.session.get("s_classifier")
        para_featNum = page.session.get("s_featNumber")
        para_props = f_getSelctedProps(e)
        globSet.setGlobID(para_id)
        para_userCsvPth = globSet.getGlobParas()['userCsv']
        s_paraProblems = f_checkParas(para_pos,para_neg,para_sample,para_clfier,
                                      para_props,para_featNum,para_userCsvPth)
        if s_paraProblems == '':
            globSet.setFeatNumInPairs(para_featNum)
            obj_infoScreen_left.bgcolor="#f2f2f3"
            text_problems.value = ""
            btnSubmit.disabled = True
            page.update()
            b_isContinue = True
        else:
            obj_infoScreen_left.bgcolor="#D5E3FE"
            text_problems.value = s_paraProblems
            btnSubmit.disabled = False
            page.update()
            b_isContinue = False
        d_rsamp = {
            'Under sampling':'delete',
            'Over sampling': 'add',
            'Under+Over sampling':'both',
            'None. Using oirginal data.':'orig'
            }
        #'
        if b_isContinue:
            print('1. Program initialization completed\n')
            print('='*50)
            print('2. Calculation task start...')
            f_visDivBlock(1)
            page.session.set('featCalcStatus', False)
            globSet.setFeatNumInPairs(int(para_featNum))
            d_allPropAcc, ls_finishProps = f_procPara_then_calc(para_pos,para_neg,
                                                                d_rsamp[para_sample],
                                                                para_clfier,para_props,
                                                                para_id,para_featNum)
            page.session.set('finishProps', ls_finishProps)
            page.session.set('featCalcStatus', True)
            #print information
            print('3. All results have been generated.')
            f_visDivBlock(2)
            fCheckProcess()
            page.update()
    #1    
    btnSubmit = ft.ElevatedButton(
        "Calculation",
        icon=ft.icons.ARROW_CIRCLE_RIGHT,
        bgcolor='#FAF4DD',
        on_click=f_calcProps,
    )
    #1
    divParas = ft.Column(
        width=800,
        height=830,
        controls=[
            logoRow,
            ft.Row(
                 [
                     ft.Text("Choose your positive files(*.fasta，required): "),
                     ft.Container(width=10),
                     ft.ElevatedButton(
                         "Positive flies",
                         height=30,
                         icon=ft.icons.UPLOAD_FILE,
                         on_click=lambda _:pick_posfiles_dialog.pick_files(allow_multiple=False),
                     ),
                     selected_posfiles,
                 ]
             ),
            ft.Row(
                 [
                     ft.Text("Choose your negative files(*.fasta，required): "),
                     ft.Container(width=10),
                     ft.ElevatedButton(
                         "Negative flies",
                         height=30,
                         icon=ft.icons.UPLOAD_FILE,
                         on_click=lambda _:pick_negfiles_dialog.pick_files(allow_multiple=False),
                     ),
                     selected_negfiles,
                 ]
             ),
            ft.Row(
                [
                    ft.Text("Choose your resampling method(required)： "),
                    ft.Container(width=10),
                    dd_resamp,
                ]
             ),
            ft.Row(
                [
                    ft.Text("Choose the embedded classifier(required)： "),
                    ft.Container(width=10),
                    rad_clasfier,
                ]
             ),
            ft.Row(
                [
                    ft.Text("Choose the number of features in combination(required)： "),
                    ft.Container(width=10),
                    rad_featNum,
                ]
             ),
            ft.Row(
                [
                    ft.Text("Choose the protein property(required): "),
                    ft.Container(width=10),
                    cb_raac,
                    obj_empty20,
                    cb_188d,
                    ft.Container(width=20),
                    cb_ACC,
                 ]
             ),
            ft.Row(
                [
                    obj_infoScreen_left,
                    obj_Props9_r,
                ],
            ),
            ft.Container(width=900, height=3,bgcolor="#cccccc"),
            ft.Row(
                [
                    ft.Container(width=250),
                    btnSubmit,
                ],
            ),
        ],
    )
    sec_intro.visible=True
    divParas.visible=False
    pb = ft.ProgressBar(width=600)
    txtDiv_process = ft.Text("Waiting....No computation has been performed yet.",overflow='visible')
    title_process = ft.Text("task progress...")
    divProgress=ft.Column(
        width=800,
        height=750,
        controls=[
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text("The progress of calculation",color='#FFFFFF',size=23),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor='#88d9d0',
                        width=650,
                        height=80,
                        border_radius=10,
                    ),
                ],
            ),
            ft.Column([title_process, pb]),
            txtDiv_process,
        ],
    )
    divProgress.visible=False
    #2
    def fCheckProcess():
        ls_allTask, ls_doneTask = f_getDoneTaskNum()
        if len(ls_allTask)==0:
            pb.value = 0
        else:
            pb.value = len(ls_doneTask)/len(ls_allTask)
            if len(ls_doneTask)>=24:
                ls_dispTask = ls_doneTask[-24:]
            else:
                ls_dispTask = ls_doneTask
            txtDiv_process.value='\n'.join(ls_dispTask)
            page.update()
        # page.update()
        f_checkResultFiles()
        f_checkVisulStatus()
        f_checkFsState_dispInfo()
        f_checkPerformance()
        #
        page.update()
    #3. results    
    #function query the result csv periodically
    def f_checkResultFiles():
        #get the task id
        s_taskID = page.session.get('taskID')
        d_validPropNames = globSet.get_finalProps()
        #the delimer line
        ls_delimiter = ['----------------','----------------------------',\
                        '------------------------','------------------------------------']
        # list: the display string list
        ls_dispText = []
        
        #iteration each propName
        if (d_validPropNames==0):
            pass
        else:
            for s_propName in list(d_validPropNames.keys()):
                s_propCsvFName = ''.join([s_propName,'_',s_taskID,'.csv'])
                #gene the smart path
                p_propCsvPth = geneSmartPth('results',s_propCsvFName)
                i_randInd_forDelim = random.randint(0,3)
                s_delimiterStr = ls_delimiter[i_randInd_forDelim]
                s_curPropInfo = ''.join([s_propName,'\t\t------>\t\t',p_propCsvPth,'\n',s_delimiterStr,'\n'])
                ls_dispText.append(s_curPropInfo)

            i_lenDispdCsv = page.session.get('i_lenCsv')
            
            if len(ls_dispText)>i_lenDispdCsv:
                #
                ls_addedCsvInfo = ls_dispText[i_lenDispdCsv:]
                page.session.set('i_lenCsv', len(ls_dispText))
                #
                for s_curPropCsv in ls_addedCsvInfo:
                    #
                    divResults.controls.append(ft.Text(s_curPropCsv))
                    page.update()
    #4. visulization               
    def f_visDivBlock(i_dispDivIndex):
        #
        ls_visibStatus = [True if i==i_dispDivIndex else False for i in range(9)]
        
        #
        sec_intro.visible=False
        divParas.visible=ls_visibStatus[0]
        divProgress.visible=ls_visibStatus[1]
        divResults.visible =ls_visibStatus[2]
        divVisul.visible = ls_visibStatus[3]
        divFS.visible = ls_visibStatus[4]
        divPerform.visible = ls_visibStatus[5]
        divSave.visible = ls_visibStatus[6]
        divHelp.visible = ls_visibStatus[7]
        page.update()
    #function: check the visulization status
    def f_checkVisulStatus():
        #if two images have been displayed
        while not page.session.get('featCalcStatus'):
            return
        #4.1 Accuracy sort list plot
        if globSet.get_task_isDone('accSortList_disped'):
            #displayed
            pass
        else:
            print('='*50)
            print('\n 4. The visulization start...')
            b_accSortLs_progDone = globSet.get_task_isDone('accSortList_progPloted')
            if b_accSortLs_progDone is None:
                pass
            elif (b_accSortLs_progDone==True): 
                elemAccSortList_txt.visible = True
                p_sortList_pngPth = globSet.get_finalTaskResults('sortListPng')
                elemAccSortList_fig.src = p_sortList_pngPth
                elemAccSortList_fig.tooltip = globSet.get_finalTaskResults('accTopN-pdfFile')
                elemAccSortList_fig.visible = True
                page.update()
                print('4.1 Accuracies sort process done...')
                print('4.1 You can find the sort list figure in the "Visulization" section of the software.')
                # print('\n')
                globSet.set_task_done('accSortList_disped')
                page.update()
            else:
                pass
        #4.2 tsne 2D scatter
        if globSet.get_bothTsneUmapDisp_status('tsne'):
            #displayed
            pass
        else:
            #get the plot task status
            b_plotTaskStatus = globSet.get_plotTaskStatus()
            #check if it is None
            if b_plotTaskStatus==False:
                pass
            elif (b_plotTaskStatus==True):
                elem_visual_totalInfo.value = '2. The scatter figure of the TSNE algorithm is as follows: '
                p_tsne_jpgPth = globSet.get_finalTaskResults('tsne-pngFile')
                elem_vis_fig_tsne.src = p_tsne_jpgPth
                elem_vis_fig_tsne.tooltip = globSet.get_finalTaskResults('tsne-pdfFile')
                page.update()
                globSet.set_bothTsneUmapDisp_done('tsne')
                print('4.2 TSNE process Done...')
                print('4.2 You can find the TSNE figure in the "Visulization" section of the software.')
                # print('\n')
                page.update()
            else:
                pass
        #4.3 violin-tsne
        if globSet.get_violPlot_status('tsne_violin_disped'):
            #displayed
            pass
        else:
            #get the umap task stauts
            b_tsneTask_status = globSet.get_violPlot_status('tsne_violin_progPloted')
            #process if the task has been done
            if b_tsneTask_status is None:
                pass
            elif (b_tsneTask_status==True): 
                elemViolinTsne_txt.visible = True
                p_tsne_pngPth = globSet.get_finalTaskResults('tsne_png_violon')
                elemViolinTsne_fig.src = p_tsne_pngPth
                elemViolinTsne_fig.tooltip = globSet.get_finalTaskResults('tsne_pdf_violon')
                elemViolinTsne_fig.visible = True
                # print(''.join(['the glob violin-tsne png path: ',p_tsne_pngPth]))
                page.update()
                print('4.3 TSNE violin process done...')
                print('4.3 You can find the violin figure in the "Visulization" section of the software.')
                # print('\n')
                globSet.set_violPlot_status_done('tsne_violin_disped')
                page.update()
            else:
                pass
        
        #4.4 umap 2D scatter
        if globSet.get_bothTsneUmapDisp_status('umap'):
            #displayed
            pass
        else:
            #get the umap task stauts
            b_umapTask_status = globSet.get_umapTask_status()
            #process if the task has been done
            if b_umapTask_status is None:
                pass
            elif (b_umapTask_status==True): 
                elem_vis_title_umap.value = '4. The scatter figure of the UMAP algorithm is as follows: '
                elem_vis_title_umap.visible = True
                p_uMAP_jpgPth = globSet.get_finalTaskResults('umap-pngFile')
                elem_vis_fig_umap.src = p_uMAP_jpgPth
                elem_vis_fig_umap.tooltip = globSet.get_finalTaskResults('umap-pdfFile')
                elem_vis_fig_umap.visible = True
                page.update()
                print('4.4 UMAP process done...')
                print('4.4 You can find the UMAP figure in the "Visulization" section of the software.')
                globSet.set_bothTsneUmapDisp_done('umap')
                page.update()
            else:
                pass
        #4.5 violin-umap
        
        if globSet.get_violPlot_status('umap_violin_disped'):
            #displayed
            pass
        else:
            #get the umap task stauts
            b_umapTask_status = globSet.get_violPlot_status('umap_violin_progPloted')
            #process if the task has been done
            if b_umapTask_status is None:
                pass
            elif (b_umapTask_status==True): 
                elemViolinUmap_txt.visible = True
                p_umap_pngPth = globSet.get_finalTaskResults('umap_png_violon')
                elemViolinUmap_fig.src = p_umap_pngPth
                elemViolinUmap_fig.tooltip = globSet.get_finalTaskResults('umap_pdf_violon')
                elemViolinUmap_fig.visible = True
                print('4.5 Umap violin process done...')
                print('4.5 You can find the violin figure in the "Visulization" section of the software.')
                print('4. Drawing completed.')
                print('You can click on the fourth button in the sidebar "Visulization" to see a graphical representation of the best categorical features')
                f_visDivBlock(3)
                print('='*50)
                print('5. You can go to the fifth button in the sidebar "Feat-Selection" to set how the features are selected.')
                globSet.set_violPlot_status_done('umap_violin_disped')
                globSet.set_FSreadyStatusOK()
                page.update()
            else:
                pass
    #check 5: feature selection
    def f_checkFsState_dispInfo():
        if globSet.is_readyFS():
            #the data procession have been done
            if globSet.is_disped_FSresults():
                pass
            else:
                dd_FS_mthdSlect.visible = True
                dd_FS_clsfier.visible = True
                dd_FS_resamMthd.visible = True
                dd_FS_testRatio.visible = True
                dd_FS_submitBtn.visible = True
                FS_select_annot.visible = True
                FS_title_clfier.visible = True
                FS_title_crossFoldNum.visible = True
                FS_title_sample.visible = True
                FS_title.visible = True
                elemText.visible = False
                page.update()
        else:
            pass
    #6. Performance
    def f_checkPerformance():
        if globSet.get_perform_paras('is_plot_done'):
            if globSet.get_perform_paras('is_disped_done') is None:
                elemPerfTitle0_0.visible = True
                elemTitle0_1.value = ""#"(The test is carried out on the feature after feature selection)"
                if globSet.getUserFsMthd()=='LDA':
                    elemFSmethdStr0.value = 'LDA'
                    elemFSmethdStr1.value = 'PCA'
                    elemConfMatrix_fig0.src = globSet.get_perform_paras('fig_conMat_LDA')
                    elemBar_fig0.src = globSet.get_perform_paras('fig_bar_LDA')
                    elemROC_fig0.src = globSet.get_perform_paras('fig_ROC9_LDA')
                    elemExplRatio_title0.visible = False
                    elemExplRatio_fig0.visible = False
                    elemCompTab0.value = page.session.get('s_info_LDA')
                    #######_--------------------------------------
                    elemExplRatio_fig1.src = globSet.get_perform_paras('Fig_PCA_explainRatio')
                    elemConfMatrix_fig1.src = globSet.get_perform_paras('fig_conMat_PCA')
                    elemBar_fig1.src = globSet.get_perform_paras('fig_bar_PCA')
                    elemROC_fig1.src = globSet.get_perform_paras('fig_ROC9_PCA')
                    elemExplRatio_title1.visible = True
                    elemExplRatio_fig1.visible = True
                    elemCompTab1.value = page.session.get('s_info_PCA')
                    page.update()
                else:
                    elemFSmethdStr0.value = 'PCA'
                    elemFSmethdStr1.value = 'LDA'
                    #
                    elemConfMatrix_fig0.src = globSet.get_perform_paras('fig_conMat_PCA')
                    elemBar_fig0.src = globSet.get_perform_paras('fig_bar_PCA')
                    elemROC_fig0.src = globSet.get_perform_paras('fig_ROC9_PCA')
                    elemExplRatio_title0.visible = True
                    elemExplRatio_fig0.src = globSet.get_perform_paras('Fig_PCA_explainRatio')
                    elemExplRatio_fig0.visible = True
                    elemCompTab0.value = page.session.get('s_info_PCA')
                    #######_--------------------------------------
                    elemConfMatrix_fig1.src = globSet.get_perform_paras('fig_conMat_LDA')
                    elemBar_fig1.src = globSet.get_perform_paras('fig_bar_LDA')
                    elemROC_fig1.src = globSet.get_perform_paras('fig_ROC9_LDA')
                    elemExplRatio_title1.visible = False
                    elemExplRatio_fig1.visible = False
                    elemCompTab1.value = page.session.get('s_info_LDA')
                elemPerfMethd0.visible = True
                elemConfMatrix_title0.visible = True
                elemConfMatrix_fig0.visible = True
                elemBar_title0.visible = True
                elemBar_fig0.visible = True
                elemROC_title0.visible = True
                elemROC_fig0.visible = True
                elemCompTabRow0.visible = True

                elemPerfMethd1.visible = True
                elemConfMatrix_title1.visible = True
                elemConfMatrix_fig1.visible = True
                elemBar_title1.visible = True
                elemBar_fig1.visible = True
                elemROC_title1.visible = True
                elemROC_fig1.visible = True
                elemCompTabRow1.visible = True
                page.update()
                
                print('='*50)
                print('6. Performance is ready...')
                print('You can go to the sixth button in the sidebar "Performance" to see the relevant icon results')
                f_visDivBlock(5)
                globSet.set_perform_paras('is_disped_done', True)
                globSet.setAllTaskFish()
                if globSet.isAllTaskFish():
                    btn_saveIcon.disabled = False
                    page.update()
            else:
                pass
        else:
            pass
            
    #3   
    divResults = ft.ListView(spacing=10,height=500)
    #3
    elemBlankDelim = ft.Row([ft.Text(value="", style="headlineMedium")], alignment=ft.MainAxisAlignment.CENTER)
    results_title = ft.Row([ft.Text(value="Results", style="headlineMedium")], alignment=ft.MainAxisAlignment.CENTER)
    divResults.controls.append(results_title)
    divResults.controls.append(elemBlankDelim)
    divResults.controls.append(elemBlankDelim)
    #
    divResults.visible = False 
    class RepeatingTimer(Timer): 
        def run(self):
            while not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
                self.finished.wait(self.interval)
    t = RepeatingTimer(2.5,fCheckProcess)
    t.start()
    
    #4. visulization
    #4.1
    elemAccSortList_txt = ft.Text('1. The TOP-N accuracies of the calculated properties are as follows: ')
    elemAccSortList_fig = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    #4.2
    elem_visual_totalInfo = ft.Text('The computing task has not yet started or is in progress, please check after the end')
    elem_vis_fig_tsne = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/visualInit.png')
    #4.3
    elemViolinTsne_txt = ft.Text('3. The violin figure of the TSNE results is as follows: ')
    elemViolinTsne_fig = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    #4.4
    elem_vis_title_umap = ft.Text(' ')
    p_uMAP_jpgPth = globSet.get_finalTaskResults('umap-pngFile')
    elem_vis_fig_umap = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    #4.5
    elemViolinUmap_txt = ft.Text('5. The violin figure of the UMAP results is as follows: ')    
    elemViolinUmap_fig = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    #4
    elemAccSortList_txt.visible = False
    elemAccSortList_fig.visible = False
    #4
    elem_vis_title_umap.visible = False
    elem_vis_fig_umap.visible = False
    #4
    elemViolinTsne_txt.visible = False
    elemViolinTsne_fig.visible = False
    #4
    elemViolinUmap_txt.visible = False
    elemViolinUmap_fig.visible = False
    #4
    elemVisTitle = ft.Row([ft.Text(value="Visual chart", style="headlineMedium")], alignment=ft.MainAxisAlignment.CENTER)
    elemBlankDelim = ft.Row([ft.Text(value="", style="headlineMedium")], alignment=ft.MainAxisAlignment.CENTER)
    #4. visible
    
    elemContorls = [
        elemVisTitle,
        elemBlankDelim,
        elemAccSortList_txt,
        elemAccSortList_fig,
        elem_visual_totalInfo,
        elem_vis_fig_tsne,
        elemViolinTsne_txt,
        elemViolinTsne_fig,
        elem_vis_title_umap,
        elem_vis_fig_umap,
        elemViolinUmap_txt,
        elemViolinUmap_fig,
    ]
    #
    divVisul = ft.Column(
            controls=elemContorls,
            spacing=5,
            run_spacing=5,
            alignment=ft.MainAxisAlignment.START,  
        )
    divVisul.visible = False
    #5. content for FS
    #5.2 function to deal with the FS method
    def f_getFSName(e):
        s_FS_method = ''
        try:
            s_FS_method = dd_FS_mthdSlect.value
            dd_FS_mthdSlect.disabled = True
            page.session.set("s_FS_method", s_FS_method)
            print(s_FS_method)
            if s_FS_method=='PCA' or s_FS_method=='LDA':
                b_isSlctFSmthd = True
                page.session.set('sFs_method', s_FS_method)
            else:
                page.session.set('sFs_method', None)
                # return [False, s_FS_method]
        except:
            page.session.set('sFs_method', None)
            # return [False, s_FS_method]
    ##5.1 select the fs method
    dd_FS_mthdSlect = ft.Dropdown(
        width=220,
        options=[
            ft.dropdown.Option("PCA"),
            ft.dropdown.Option("LDA"),
         ],
        on_change=f_getFSName,
     )
    dd_FS_mthdSlect.visible = False
    #5.2 function of the FS classifier
    def f_getFS_clsfer(e):
        s_classifier = ''
        try:
            s_classifier = dd_FS_clsfier.value
            page.session.set("s_FS_clfer", s_classifier)
            if s_classifier in ["Random Forest", "RBF SVM", "Gaussian Process", "Neural Net","xgboost"]:
                page.session.set("sFS_clfer", s_classifier)
            else:
                # print(s_classifier)
                page.session.set("sFS_clfer", s_classifier)
        except:
            page.session.set("sFS_clfer", None)
        # print(s_classifier)
        dd_FS_clsfier.disabled = True 
    #5.1 parameter setting
    dd_FS_clsfier=ft.Dropdown(
        width=220,
        options=[
            ft.dropdown.Option("Nearest Neighbors"),
            ft.dropdown.Option("SVM(linear)"),
            ft.dropdown.Option("RBF SVM"),
            ft.dropdown.Option("Gaussian Process"),
            ft.dropdown.Option("Decision Tree"),
            ft.dropdown.Option("Random Forest"),
            ft.dropdown.Option("Neural Net"),
            ft.dropdown.Option("AdaBoost"),
            ft.dropdown.Option("Naive Bayes"),
            ft.dropdown.Option("QDA"),
            ft.dropdown.Option("xgboost"),
            ft.dropdown.Option("lightGBM"),
            ft.dropdown.Option('Gradient Boosting Classifier'),
            ft.dropdown.Option('SVC'),
            ft.dropdown.Option('ExtraTreesClassifier'),
            ft.dropdown.Option('SGDClassifier'),
            ft.dropdown.Option('BernoulliNB'),
            ft.dropdown.Option('Perceptron'),
            ft.dropdown.Option('PassiveAggressiveClassifier'),
            ft.dropdown.Option('BaggingClassifier'),
            ft.dropdown.Option('CalibratedClassifierCV'),
            ft.dropdown.Option('ExtraTreeClassifier'),
            ft.dropdown.Option('NearestCentroid'),
            ft.dropdown.Option('LinearDiscriminantAnalysis'),
            ft.dropdown.Option('LabelSpreading'),
            ft.dropdown.Option('LabelPropagation'),
            ft.dropdown.Option('DummyClassifier')
        ],
        on_change=f_getFS_clsfer,
    )
    dd_FS_clsfier.visible = False
    #5.2
    def f_getFS_resampMthd(e):
        s_resampMthd = ''
        s_simpleMthd = ''
        try:
            s_resampMthd = dd_FS_resamMthd.value
            if s_resampMthd == 'Under sampling':
                page.session.set('s_simpleMthd', 'delete')
            elif s_resampMthd == 'Over sampling':
                page.session.set('s_simpleMthd', 'add')
            elif s_resampMthd == 'Under+Over sampling':
                page.session.set('s_simpleMthd', 'both')
            else:
                page.session.set('s_simpleMthd', None)
        except:
            page.session.set('s_simpleMthd', None)
    #5.1
    dd_FS_resamMthd = ft.Dropdown(
        width=220,
        options=[
            ft.dropdown.Option('Under sampling'),
            ft.dropdown.Option('Over sampling'),
            ft.dropdown.Option('Under+Over sampling'),
        ],
        on_change=f_getFS_resampMthd,
    )
    dd_FS_resamMthd.visible = False
    #5.2
    def f_getFS_testRatio(e):
        f_testRatio = 0
        try:
            s_foldNumber = dd_FS_testRatio.value
            if s_foldNumber == '0.1':
                page.session.set('f_testRatio', 0.1)
            elif s_foldNumber == '0.2':
                page.session.set('f_testRatio', 0.2)
            elif s_foldNumber == '0.3':
                page.session.set('f_testRatio', 0.3)
            else:
                page.session.set('f_testRatio', None)
        except:
            page.session.set('f_testRatio', None)
    #5.1
    dd_FS_testRatio = ft.Dropdown(
        width=220,
        options=[
            ft.dropdown.Option('0.1'),
            ft.dropdown.Option('0.2'),
            ft.dropdown.Option('0.3')
        ],
        on_change=f_getFS_testRatio,
    )
    dd_FS_testRatio.visible = False
    #5.2
    def f_FS_process(e):
        #check the paramaters
        try:
            sFs_method = page.session.get('sFs_method')
            globSet.setUserFsMthd(sFs_method)
        except:
            sFs_method = 'LDA'
            globSet.setUserFsMthd(sFs_method)
        try:
            sFS_clfer = page.session.get('sFS_clfer')
        except:
            sFS_clfer = 'Random Forest'
        try:
            s_simpleMthd = page.session.get('s_simpleMthd')
        except:
            s_simpleMthd = 'delete'
        try:
            f_testRatio = page.session.get('f_testRatio')
        except:
            f_testRatio = 0.2
        #set the elements not visible
        dd_FS_submitBtn.disabled = True
        dd_FS_mthdSlect.disabled = True
        dd_FS_clsfier.disabled = True
        dd_FS_resamMthd.disabled = True
        dd_FS_testRatio.disabled = True
        
        
        #read the csv file
        df_csvData = pd.read_csv(globSet.get_bestFeat_csvPth())
        
        # Feature selection process
        print('5. FS task start...')
        s_4Metrics_info_LDA = f_iLDA_process(df_csvData,sFS_clfer,s_simpleMthd,f_testRatio,'class')
        s_4Metrics_info_PCA = f_iPcaProcess(df_csvData,sFS_clfer,s_simpleMthd,f_testRatio,'class') 
        f_writeCompInfo(s_4Metrics_info_PCA, s_4Metrics_info_LDA, sFs_method)
        page.session.set('s_info_LDA', s_4Metrics_info_LDA)
        page.session.set('s_info_PCA', s_4Metrics_info_PCA)
        #
        print('LDA:')
        print(s_4Metrics_info_LDA)
        print('PCA:')
        print(s_4Metrics_info_PCA)
        print('5. FS task finish.\n')
        # print('\n')
        #
        globSet.set_perform_paras('is_plot_done', True)
        #
        FS_dispResult.visible = True
        #
        fCheckProcess()
        page.update()
            
    #5.1
    dd_FS_submitBtn = ft.ElevatedButton(
        "Feature selection",
        icon=ft.icons.ARROW_CIRCLE_RIGHT,
        bgcolor='#FAF4DD',
        on_click=f_FS_process,
    )
    dd_FS_submitBtn.visible = False
    #5.1 select the 
    #
    elemText = ft.Text(value="This function will be opened after the calculation is complete, plase wait...", style="titleMedium")
    FS_title = ft.Row([ft.Text(value="Feature selection", style="headlineMedium")],alignment=ft.MainAxisAlignment.CENTER)
    FS_title.visible = False
    FS_select_annot = ft.Text('Please select your Feature selection methods:')
    FS_title_clfier = ft.Text('Please select your classifier:')
    FS_title_crossFoldNum = ft.Text('Please select the test set ratio:')
    FS_title_sample= ft.Text('Please select your sampling strategy:')
    FS_select_annot.visible = False
    FS_title_clfier.visible = False
    FS_title_crossFoldNum.visible = False
    FS_title_sample.visible = False
    FS_dispResult = ft.Container(
        content=ft.ElevatedButton(
            "The feature selection task is complete. Please see the results in performance", opacity=0.5
        ),
        bgcolor='#A1EDFF',
        padding=5,
    )
    FS_dispResult.visible = False
    #5
    elemFS = [
        elemText,
        FS_title,
        FS_select_annot,
        dd_FS_mthdSlect,
        FS_title_clfier,
        dd_FS_clsfier,
        FS_title_sample,
        dd_FS_resamMthd,
        FS_title_crossFoldNum,
        dd_FS_testRatio,
        dd_FS_submitBtn,
        FS_dispResult,
    ]
    divFS = ft.Column(
            controls=elemFS,
            spacing=5,
            run_spacing=5,
            alignment=ft.MainAxisAlignment.START,
        )
    divFS.visible = False
    #6 Performance
    elemPerfTitle0_0 = ft.Row([ft.Text(value="Predictive Performance", style="headlineMedium")],
                              alignment=ft.MainAxisAlignment.CENTER)
    elemTitle0_1 = ft.Text(value="The result will be displayed after the calculation", style="headlineMedium")
    elemPerfTitle0_1 = ft.Row([elemTitle0_1],alignment=ft.MainAxisAlignment.CENTER)
    #6.0 method 1
    elemFSmethdStr0 = ft.Text(value=" ", style="headlineMedium")
    elemPerfMethd0 = ft.Row([elemFSmethdStr0],alignment=ft.MainAxisAlignment.START)
    elemConfMatrix_title0 = ft.Text('a. The confusion matrix figure: ')
    elemConfMatrix_fig0 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    elemBar_title0 = ft.Text('b. The four performance metrics figure: ')
    elemBar_fig0 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    elemROC_title0 = ft.Text('c. The ROC figure: ')
    elemROC_fig0 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    elemExplRatio_title0 = ft.Text('d. The explain ratio of PCA feature figure: ')
    elemExplRatio_fig0 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    #6.0 method2
    elemFSmethdStr1 = ft.Text(value=" ", style="headlineMedium")
    elemPerfMethd1 = ft.Row([elemFSmethdStr1],alignment=ft.MainAxisAlignment.START)
    elemConfMatrix_title1 = ft.Text('a. The confusion matrix figure: ')
    elemConfMatrix_fig1 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    elemBar_title1 = ft.Text('b. The four performance metrics figure: ')
    elemBar_fig1 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    elemROC_title1 = ft.Text('c. The ROC figure: ')
    elemROC_fig1 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    elemExplRatio_title1 = ft.Text('d. The explain ratio of PCA feature figure: ')
    elemExplRatio_fig1 = ft.Image(width=400,height=300,fit=ft.ImageFit.FIT_WIDTH,
                          repeat=ft.ImageRepeat.NO_REPEAT,
                          src=f'/data/blank.png')
    #the comparison info
    elemCompTab0 = ft.Text(' ')
    elemCompTabRow0 = ft.Row([elemCompTab0],alignment=ft.MainAxisAlignment.START)
    elemCompTab1 = ft.Text(' ')
    elemCompTabRow1 = ft.Row([elemCompTab1],alignment=ft.MainAxisAlignment.START)
    #6.visible setting
    elemPerfTitle0_0.visible = False
    elemPerfMethd0.visible = False
    elemConfMatrix_title0.visible = False
    elemConfMatrix_fig0.visible = False
    elemBar_title0.visible = False
    elemBar_fig0.visible = False
    elemROC_title0.visible = False
    elemROC_fig0.visible = False
    elemExplRatio_title0.visible = False
    elemExplRatio_fig0.visible = False
    elemCompTabRow0.visible = False
    #6#######_--------------------------------------
    elemPerfMethd1.visible = False
    elemConfMatrix_title1.visible = False
    elemConfMatrix_fig1.visible = False
    elemBar_title1.visible = False
    elemBar_fig1.visible = False
    elemROC_title1.visible = False
    elemROC_fig1.visible = False
    elemExplRatio_title1.visible = False
    elemExplRatio_fig1.visible = False
    elemCompTabRow1.visible = False
    #6.0 main element container
    ls_elems_Perform = [
        elemPerfTitle0_0,
        elemPerfTitle0_1,
        elemFSmethdStr0,
        elemPerfMethd0,
        elemConfMatrix_title0,
        elemConfMatrix_fig0,
        elemBar_title0,
        elemBar_fig0,
        elemROC_title0,
        elemROC_fig0,
        elemExplRatio_title0,
        elemExplRatio_fig0,
        elemCompTabRow0,
        elemFSmethdStr1,#the other method
        elemPerfMethd1,
        elemConfMatrix_title1,
        elemConfMatrix_fig1,
        elemBar_title1,
        elemBar_fig1,
        elemROC_title1,
        elemROC_fig1,
        elemExplRatio_title1,
        elemExplRatio_fig1,
        elemCompTabRow1,
    ]
    divPerform = ft.Column(
        controls=ls_elems_Perform,
        spacing=0,
        run_spacing=0,
        alignment=ft.MainAxisAlignment.START,
    )
    divPerform.visible = False
    #7. Extraction elements
    # find all the files
    def list_dir(file_dir):
        '''
            通过 listdir 得到的是仅当前路径下的文件名，不包括子目录中的文件，如果需要得到所有文件需要递归
        '''
        dir_list = os.listdir(file_dir)
        result_list = []
        for cur_file in dir_list:
            # 获取文件的绝对路径
            path = os.path.join(file_dir, cur_file)
            if os.path.isfile(path): # 判断是否是文件还是目录需要用绝对路径
                result_list.append(path)
            if os.path.isdir(path):
                result_list += list_dir(path) # 递归子目录
        return result_list
    #fitlering the results
    def f_filterCurTaskResults():
        ls_allfiles = list_dir('./results/')
        s_taskID = globSet.getGlobID()
        ls_filterResults = []
        for ind, s_fileName in enumerate(ls_allfiles):
            if s_taskID in s_fileName:
                ls_filterResults.append(s_fileName)
        #return value
        return ls_filterResults
    # Save file dialog
    def save_file_result(e: ft.FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Cancelled!"
        save_file_path.update()
        s_outputZIP_path = ''.join([save_file_path.value,'.zip'])
        ls_files_currentTask = f_filterCurTaskResults()
        if save_file_path.value=='Cancelled!':
            print('\n The file export task has not been executed because you failed to set the output file')
        else:
            with zipfile.ZipFile(s_outputZIP_path,'w') as zipobj:
                for s_1file in ls_files_currentTask:
                    zipobj.write(s_1file)
            print(''.join(['7. All files related to this task have been saved to the zip package:\n',s_outputZIP_path]))
            print('\n\n 8. The calculation task is completed successfully！')

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    save_file_path = ft.Text()
    page.overlay.extend([save_file_dialog])
    elem_title = ft.Row([ft.Text(value="Save Files", style="headlineMedium")],alignment=ft.MainAxisAlignment.CENTER)
    elem_blank = ft.Container(width=400,height=20)#bgcolor="#cccccc"
    s_text = 'Determine a directory to save the results and images associated with this task'
    elem_intro = ft.Container(content=ft.Text((s_text)),margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor='#EEE8A9',##F6EDA1
                width=650,
                height=95,
                border_radius=10,
                )
    btn_saveIcon = ft.ElevatedButton(
        "Save file",
        icon=ft.icons.SAVE,
        on_click=lambda _: save_file_dialog.save_file(),
        disabled=page.web,
    )
    btn_saveIcon.disabled = True
    elem_saveBtn = ft.Row(
        [
            ft.Container(width=200),
            btn_saveIcon
        ]
    )
    elem_savePathInfo = ft.Row([save_file_path],alignment=ft.MainAxisAlignment.START)
    elem_blank_btm = ft.Container(width=400,height=300)#bgcolor="#cccccc"
    ls_save_elems = [elem_title, elem_blank, elem_intro, elem_blank, elem_saveBtn,elem_savePathInfo,elem_blank_btm]
    divSave = ft.Column(
        controls=ls_save_elems,
        spacing=0,
        run_spacing=1,
        alignment=ft.MainAxisAlignment.START,
    )
    divSave.visible = False
    
    #7. Help
    elem_help_title = ft.Row([ft.Text(value="Help", style="headlineMedium")],alignment=ft.MainAxisAlignment.CENTER)
    elem_help_intro = ft.Container(
                    content=ft.Text(('1. For details on the use of this software, see "iPropManual.pdf" in this package.\n'
                                     '2. For questions regarding the use of this software, please contact:\n tafchl{[at]}mail.nankai.edu.cn'
                                     )),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor='#EEE8A9',##F6EDA1
                    width=650,
                    height=95,
                    border_radius=10,
    )
    elem_help_blank = ft.Container(width=400,height=20)#bgcolor="#cccccc"
    elem_help_blank_l = ft.Container(width=100,height=50)
    elem_help_logo = ft.Image(
        src=f'/copyright.png',
        fit="contain",
        repeat="noRepeat",
    )
    div_delimiter = ft.Container(width=680,height=3,bgcolor="#aaaaaa")
    div_help_logo = ft.Row([elem_help_logo],alignment=ft.MainAxisAlignment.CENTER)
    
    ls_elems_help = [
        elem_help_title,
        elem_help_intro,
        elem_help_blank,
        div_delimiter,
        elem_help_blank,
        div_help_logo,
    ]
    divHelp = ft.Column(
        controls=ls_elems_help,
        spacing=0,
        run_spacing=1,
        alignment=ft.MainAxisAlignment.START,
    )
    divHelp.visible = False
    #0. main page layout
    rBox = ft.Column([sec_intro,divParas,divProgress,divResults,divVisul,divFS,divPerform,divSave,divHelp], 
                     alignment="start", expand=True)
    
    #function: write the comparison table
    def f_writeCompInfo(s_PCA, s_LDA, s_FS_mthd):
        #the output txt table
        s_compTabFile = ''.join([globSet.getGlobID(),'_Sn_CompaTable.txt'])
        p_compTabFile = geneSmartPth('results',s_compTabFile)
        #
        f_id_compTab = open(p_compTabFile,'w')
        if s_FS_mthd=='PCA':
            f_id_compTab.write('PCA:\n')
            f_id_compTab.write(s_PCA)
            f_id_compTab.write('\n\n\nLDA:\n')
            f_id_compTab.write(s_LDA)
        else:
            f_id_compTab.write('LDA:\n')
            f_id_compTab.write(s_LDA)
            f_id_compTab.write('\n\n\nPCA:\n')
            f_id_compTab.write(s_PCA)
        f_id_compTab.close()
    
    
    def f_chgVisDiv(e):
        #
        i_clickItemInd = e.control.selected_index
        ls_visibStatus = [True if i==i_clickItemInd else False for i in range(9)]
        
        #
        sec_intro.visible=False
        divParas.visible=ls_visibStatus[0]
        divProgress.visible=ls_visibStatus[1]
        divResults.visible =ls_visibStatus[2]
        divVisul.visible = ls_visibStatus[3]
        divFS.visible = ls_visibStatus[4]
        divPerform.visible = ls_visibStatus[5]
        divSave.visible = ls_visibStatus[6]
        divHelp.visible = ls_visibStatus[7]
        page.update()
    
    def f_showIntroDiv(e):
        #
        sec_intro.visible=True
        ls_visibStatus = [False for i in range(5)]
        divParas.visible=ls_visibStatus[0]
        page.update()
    #main page
    rail = ft.navigation_rail.NavigationRail(
        selected_index=None,
        label_type="all",
        bgcolor = '#E4E4E4',#EDFBFF#F2FAFF#D9DCE0
        min_width=100,
        height=750,
        leading=ft.FloatingActionButton(text="iProps", on_click=f_showIntroDiv),
        group_alignment=-0.8,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.PIX_OUTLINED,#icon=ft.icons.LOCAL_ATTRACTION,
                selected_icon=ft.icons.PIX_SHARP,
                label="Start",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MANAGE_HISTORY,
                selected_icon=ft.icons.MANAGE_HISTORY,
                label="Progress"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS),
                label="Results",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.BUBBLE_CHART,
                selected_icon_content=ft.Icon(ft.icons.BUBBLE_CHART_OUTLINED),
                label_content=ft.Text("Visulization"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.REDUCE_CAPACITY,
                selected_icon_content=ft.Icon(ft.icons.REDUCE_CAPACITY),
                label_content=ft.Text("Feat-Selection"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INSIGHTS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.INSIGHTS_SHARP),
                label_content=ft.Text("Performance"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.FOLDER_ZIP_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.FOLDER_ZIP_ROUNDED),
                label_content=ft.Text("ExtractFiles"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.HELP_CENTER_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.HELP),
                label_content=ft.Text("Help"),
            ),
        ],
        on_change=f_chgVisDiv,
    )
    

    page.controls.append(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1,),
                rBox,
            ],
            expand=False,
        )
    )
    page.scroll="always"
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")