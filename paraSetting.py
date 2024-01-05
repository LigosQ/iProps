#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 20:12:54 2023

@author: sealight
"""
import flet as ft,pickle
import warnings,os
from files import globSet,geneSmartPth

class ErrorCoding(Exception):
    pass

def main(page):
    #
    warnings.filterwarnings('ignore')
    page.title='iProp-p Ver 0.7'
    page.bgcolor="#f2f2f3"#f2f2f3
    page.window_width=870
    page.window_height=870
    theme = ft.Theme()
    theme.page_transitions.android = "openUpwards"
    theme.page_transitions.ios = "cupertino"
    theme.page_transitions.macos = "fadeUpwards"
    theme.page_transitions.linux = "zoom"
    theme.page_transitions.windows = "zoom"
    page.theme = theme
    page.scroll = "adaptive"
    
    try:
        globSet.getGlobID()
    except:
        globSet._init()
        
    def f_checkPara_bigThan0(v_1para):
        try:
            float(v_1para)
        except:
            raise ErrorCoding('Your 1st parameter is not a number.')
        if '.' in v_1para:
            v_1para = float(v_1para)
        else:
            v_1para = int(v_1para)
        if v_1para >= 0:
            pass
        else:
            raise ErrorCoding('Int type parameter should be greater than 0')
    def f_checkParaIsStr(v_1para,s_correctType):
        if isinstance(v_1para, str):
            if os.path.exists(v_1para) and os.path.isfile(v_1para):
                if os.path.splitext(v_1para)[-1] == '.csv':
                    pass
                else:
                    raise ErrorCoding('The file extension you provide should be ".csv"')
            else:
                raise ErrorCoding(''.join(['The file you set ',v_1para, ' does not exist. And it"s not a file']))
            
    def f_checkParaAndRange(v_1para,s_correctType,f_min=0,f_max=1):
        try:
            float(v_1para)
        except:
            raise ErrorCoding('Your 1st parameter is not a number.')
        if '.' in v_1para:
            v_1para = float(v_1para)
        else:
            v_1para = int(v_1para)
        if isinstance(v_1para, type(s_correctType)):
            if isinstance(s_correctType, type(1)):
                if v_1para>=1:
                    pass
                else:
                    raise ErrorCoding('Int type parameter should be greater than 0')
            elif isinstance(s_correctType, type(0.01)):
                if v_1para>=f_min and v_1para<=f_max:
                    pass
                else:
                    raise ErrorCoding('Data of type float should be between 0 and 1')
        else:
            raise ErrorCoding(''.join(['The argument you provided is not of type ',s_correctType]))
    
    t_dlgText = ft.Text("You selected the feature but didn't set the parameters")
    dlg = ft.AlertDialog(
        title=t_dlgText, on_dismiss=lambda e: print("Dialog dismissed!")
        )
    
    def open_dlg(e):
        t_dlgText.value = "You selected the feature but didn't set the parameters"
        page.dialog = dlg
        dlg.open = True
        page.update()
    def open_dlg_OK(e):
        t_dlgText.value = 'All parameters are set sucessfully according to your input.'
        page.dialog = dlg
        dlg.open = True
        page.update()
    def open_dlg_reset(e):
        t_dlgText.value = 'All parameters are set to the initilize status.'
        page.dialog = dlg
        dlg.open = True
        page.update()
    def open_dlg_Noclicked(e):
        t_dlgText.value = 'You haven\'t set any parameters.'
        page.dialog = dlg
        dlg.open = True
        page.update()
    def open_dlg_wrongSchmNo(e):
        t_dlgText.value = 'You given scheme NO. is wrong, it should be >=1.'
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def btn_setParas(e):       
        #
        d_allParas = {'ACC': 2, 'CC': 2, 'AC': 2, 'Moran': 10, 'numbroto': 10, 
                      'geary': 10, 'socnumber': 10, 'QsOrder': 10, 
                      'ScGeneral': {'lambda': 2, 'w': 0.1}, 'PAAC': {'lambda': 30,'w':0.05}, 'CKSAAGP': {'nlag':5,'redSchmNo':1},
                      'CKSAAP': 5, 'rTrip': {'i_redSchmNo': 1, 'i_tripepTypeNo': 0}, 
                      'ScPseAAC': {'lambda': 2, 'w': 0.1},'userCsv':'pi','orDip':10,
                      'APAAC':{'lambda':30, 'w':0.05}}
        ls_checkboxes = [c_ORDip,c_188,c_ACC,c_CC,c_AC,c_Moran,cb_numbroto,cb_Geary,
                         cb_socnumber,cb_QsOrder,cb_scGeneral,cb_PAAC,cb_CTDC,cb_CTDD,
                         cb_CTDT,cb_DDE,cb_ScPseAAC,cb_CKSAAGP,cb_CKSAAP,cb_rTrip,
                         cb_userCsv,cb_APAAC]
        ls_valueElems = [t_info,None,tb_accPara,tb_ccPara,tb_acPara,tb_MoranPara,
                         tb_NmbrotoPara,tb_GearyPara,tb_socnumberPara,tb_QsOrderPara,
                         [tb_scGeneral_lag,tb_scGeneral_w],[tb_PAAC_l,tb_PAAC_w],None,None,None,None,
                         [tb_ScPseAAC_lambda,tb_ScPseAAC_w],[tb_CKSAAGP_l,tb_CKSAAGP_No],tb_CKSAAP,
                         [tb_rTrip_schm,tb_rTrip_t],text_csvinfo,
                         [tb_APAAC_lambda,tb_APAAC_w]]
        ls_featNames = ['orDip','188d','ACC','CC','AC','Moran','numbroto','geary',
                        'socnumber','QsOrder','ScGeneral','PAAC','CTDC','CTDD',
                        'CTDT','DDE','ScPseAAC','CKSAAGP','CKSAAP','rTrip','userCsv',
                        'APAAC']
        i_slctedNum = 0
        for i,varElem in enumerate(ls_checkboxes):
            if varElem.value:
                i_slctedNum += 1
            else:
                pass
        if i_slctedNum==0:
            open_dlg_Noclicked(e)
            print('You haven\'t set any parameters.')
            return 0
        ##检查选中了特征的情况下，未设置参数的情况。如果出现，进行颜色提示
        for i,varElem in enumerate(ls_checkboxes):
            if varElem.value:
                if ls_featNames[i] in ['188d','CTDC','CTDD','CTDT','DDE']:
                    pass
                elif ls_featNames[i] in ['ACC','CC','AC','Moran','numbroto','geary',
                                         'socnumber','QsOrder','CKSAAP']:
                    if((ls_valueElems[i].value)==''):
                        ls_valueElems[i].bgcolor = '#FEA29E'
                        ls_valueElems[i].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'orDip':
                    if((ls_valueElems[i].value)==''):
                        ls_valueElems[i].bgcolor = '#FEA29E'
                        ls_valueElems[i].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'ScGeneral':
                    if (ls_valueElems[i][0].value==''):
                        ls_valueElems[i][0].bgcolor = '#FEA29E'
                        ls_valueElems[i][0].update()
                        open_dlg(e)
                        return 0
                    if (ls_valueElems[i][1].value==''):
                        ls_valueElems[i][1].bgcolor = '#FEA29E'
                        ls_valueElems[i][1].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'CKSAAGP':
                    if (ls_valueElems[i][0].value==''):
                        ls_valueElems[i][0].bgcolor = '#FEA29E'
                        ls_valueElems[i][0].update()
                        open_dlg(e)
                        return 0
                    if (ls_valueElems[i][1].value==''):
                        ls_valueElems[i][1].bgcolor = '#FEA29E'
                        ls_valueElems[i][1].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'ScPseAAC':
                    if (ls_valueElems[i][0].value==''):
                        ls_valueElems[i][0].bgcolor = '#FEA29E'
                        ls_valueElems[i][0].update()
                        open_dlg(e)
                        return 0
                    if (ls_valueElems[i][1].value==''):
                        ls_valueElems[i][1].bgcolor = '#FEA29E'
                        ls_valueElems[i][1].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'rTrip':
                    if (ls_valueElems[i][0].value==''):
                        ls_valueElems[i][0].bgcolor = '#FEA29E'
                        ls_valueElems[i][0].update()
                        open_dlg(e)
                        return 0
                    if (ls_valueElems[i][1].value==''):
                        ls_valueElems[i][1].bgcolor = '#FEA29E'
                        ls_valueElems[i][1].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'PAAC':
                    if (ls_valueElems[i][0].value==''):
                        ls_valueElems[i][0].bgcolor = '#FEA29E'
                        ls_valueElems[i][0].update()
                        open_dlg(e)
                        return 0
                    if (ls_valueElems[i][1].value==''):
                        ls_valueElems[i][1].bgcolor = '#FEA29E'
                        ls_valueElems[i][1].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'APAAC':
                    if (ls_valueElems[i][0].value==''):
                        ls_valueElems[i][0].bgcolor = '#FEA29E'
                        ls_valueElems[i][0].update()
                        open_dlg(e)
                        return 0
                    if (ls_valueElems[i][1].value==''):
                        ls_valueElems[i][1].bgcolor = '#FEA29E'
                        ls_valueElems[i][1].update()
                        open_dlg(e)
                        return 0
                elif ls_featNames[i] == 'userCsv':
                    if (ls_valueElems[i].value==''):
                        ls_valueElems[i].value = 'You have not selected the file'
                        ls_valueElems[i].color = '#FEA29E'
                        ls_valueElems[i].update()
                        open_dlg(e)
                        return 0
        ###检查提供参数的正确性
        for i,varElem in enumerate(ls_checkboxes):
            if varElem.value:
                if ls_featNames[i] in ['188d','CTDC','CTDD','CTDT','DDE']:
                    pass
                elif ls_featNames[i] in ['ACC','CC','AC','Moran','numbroto','geary',
                                         'socnumber','QsOrder','CKSAAP','orDip']:
                    f_checkParaAndRange((ls_valueElems[i].value),1)
                    d_allParas[ls_featNames[i]] = int(ls_valueElems[i].value)
                elif ls_featNames[i] == 'CKSAAGP':
                    f_checkParaAndRange((ls_valueElems[i][0].value),1)
                    f_checkParaAndRange((ls_valueElems[i][1].value),1)
                    d_temp = dict()
                    d_temp['nlag'] = int(ls_valueElems[i][0].value)
                    d_temp['redSchmNo'] = int(ls_valueElems[i][1].value)
                    d_allParas['CKSAAGP'] = d_temp
                elif ls_featNames[i] == 'ScGeneral':
                    f_checkParaAndRange((ls_valueElems[i][0].value),1)
                    f_checkParaAndRange((ls_valueElems[i][1].value),0.01)
                    d_temp = dict()
                    d_temp['lambda'] = int(ls_valueElems[i][0].value)
                    d_temp['w'] = float(ls_valueElems[i][1].value)
                    d_allParas['ScGeneral'] = d_temp
                elif ls_featNames[i] == 'ScPseAAC':
                    f_checkParaAndRange((ls_valueElems[i][0].value),1)
                    f_checkParaAndRange((ls_valueElems[i][1].value),0.01)
                    d_temp = dict()
                    d_temp['lambda'] = int(ls_valueElems[i][0].value)
                    d_temp['w'] = float(ls_valueElems[i][1].value)
                    d_allParas['ScPseAAC'] = d_temp
                elif ls_featNames[i] == 'rTrip':
                    f_checkParaAndRange((ls_valueElems[i][0].value),1)
                    f_checkPara_bigThan0((ls_valueElems[i][1].value))
                    d_temp = dict()
                    d_temp['i_redSchmNo'] = int(ls_valueElems[i][0].value)
                    d_temp['i_tripepTypeNo'] = int(ls_valueElems[i][1].value)
                    d_allParas['rTrip'] = d_temp
                    
                elif ls_featNames[i] == 'PAAC':
                    f_checkParaAndRange((ls_valueElems[i][0].value),1)
                    f_checkParaAndRange((ls_valueElems[i][1].value),0.01)
                    d_temp = dict()
                    d_temp['lambda'] = int(ls_valueElems[i][0].value)
                    d_temp['w'] = float(ls_valueElems[i][1].value)
                    d_allParas['PAAC'] = d_temp
                elif ls_featNames[i] == 'APAAC':
                    f_checkParaAndRange((ls_valueElems[i][0].value),1)
                    f_checkParaAndRange((ls_valueElems[i][1].value),0.01)
                    d_temp = dict()
                    d_temp['lambda'] = int(ls_valueElems[i][0].value)
                    d_temp['w'] = float(ls_valueElems[i][1].value)
                    d_allParas['APAAC'] = d_temp
                elif ls_featNames[i] == 'userCsv':
                    s_csvPth = page.session.get("csvFilePth")
                    f_checkParaIsStr(s_csvPth,'a')
                    d_allParas['userCsv'] = s_csvPth
                    print(d_allParas['userCsv'])
        if len(ls_checkboxes)==0:
            open_dlg_Noclicked(e)
        else:
            p_paraFilePth = geneSmartPth.geneSmartPth('data','paras.data')
            with open(p_paraFilePth, 'wb') as f:
                pickle.dump(d_allParas, f)
            open_dlg_OK(e)
        print("All parameters are set sucessfully according to your input.")
        
    def resetParas(e):
        d_allParas = dict()
        d_allParas['ACC'] = 2
        d_allParas['CC'] = 2
        d_allParas['AC'] = 2
        d_allParas['Moran'] = 10
        d_allParas['numbroto'] = 10
        d_allParas['geary'] = 10
        d_allParas['socnumber'] = 10
        d_allParas['QsOrder'] = 10
        d_allParas['ScGeneral'] = {'lambda':2,'w':0.1}
        d_allParas['PAAC'] = {'lambda':30,'w':0.05}
        d_allParas['CKSAAGP'] = {'nlag':5,'redSchmNo':1}
        d_allParas['CKSAAP'] = 5
        d_allParas['rTrip'] = {'i_redSchmNo':1,'i_tripepTypeNo':0}
        d_allParas['ScPseAAC'] = {'lambda':2,'w':0.1}
        d_allParas['userCsv'] = 'nk'
        d_allParas['orDip'] = 10
        d_allParas['APAAC'] = {'lambda':30, 'w':0.05}
        p_paraFilePth = geneSmartPth.geneSmartPth('data','paras.data')
        with open(p_paraFilePth, 'wb') as f:
            pickle.dump(d_allParas, f)
        open_dlg_reset(e)
        print("All parameters are set to initilize status.")
    
    elem_help_title = ft.Row([ft.Text(value="Feature Parameters Setting", style="headlineMedium")],alignment=ft.MainAxisAlignment.CENTER)

    # t = ft.Text()
    imglogo = ft.Image(
        src_base64='''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''',
        width=107,
        height=107,
        fit=ft.ImageFit.FIT_HEIGHT,
        repeat=ft.ImageRepeat.NO_REPEAT,
    )
    header = ft.Row(spacing=155,controls=[imglogo, elem_help_title])
    
    ##1#ORDip
    def dispElement(e):
        if c_ORDip.value:
            t_info.visible = True
            t_info.update()
        else:
            t_info.visible = False
            t_info.update() 
    t_info = ft.TextField(label="Number of features extracted", hint_text="Enter an integer(default:10)")
    t_info.visible = False
    c_ORDip = ft.Checkbox(label="1. ORDip", value=False, on_change=dispElement)
    r_ordip = ft.Row([c_ORDip,t_info])
    #####--------------------------------------------
    
    ##2#188d
    def dispElement188(e):
        if c_188.value:
            t_188info.value = "|  No parameters required"
            t_188info.update()
        else:
            t_188info.value = ""
            t_188info.update() 
    t_188info = ft.Text(value="", style="BODY_MEDIUM",color="#4f6a8f")
    c_188 = ft.Checkbox(label="2. 188D", value=False, on_change=dispElement188)
    r_188 = ft.Row([c_188,t_188info])
    r_188.visible = False
    
    ##3#ACC
    def dispACCParaBox(e):
        if c_ACC.value:
            tb_accPara.visible = True
            tb_accPara.update()
        else:
            tb_accPara.visible = False
            tb_accPara.update()
    tb_accPara = ft.TextField(label="lag value(ACC)", hint_text="Enter an integer(default:2)")
    tb_accPara.visible=False
    c_ACC = ft.Checkbox(label="3. ACC", value=False, on_change=dispACCParaBox)
    r_ACC = ft.Row([c_ACC,tb_accPara])
    
    ##4#CC
    def dispCCParaBox(e):
        if c_CC.value:
            tb_ccPara.visible = True
            tb_ccPara.update()
        else:
            tb_ccPara.visible = False
            tb_ccPara.update()
    tb_ccPara = ft.TextField(label="lag value(CC)", hint_text="Enter an integer(default:2)")
    tb_ccPara.visible=False
    c_CC = ft.Checkbox(label="4. CC", value=False, on_change=dispCCParaBox)
    r_CC = ft.Row([c_CC,tb_ccPara])
    
    ##5#AC
    def dispACParaBox(e):
        if c_AC.value:
            tb_acPara.visible = True
            tb_acPara.update()
        else:
            tb_acPara.visible = False
            tb_acPara.update()
    tb_acPara = ft.TextField(label="lag value(AC)", hint_text="Enter an integer(default:2)")
    tb_acPara.visible=False
    c_AC = ft.Checkbox(label="5. AC", value=False, on_change=dispACParaBox)
    r_AC = ft.Row([c_AC,tb_acPara])
    
    ##6#Moran
    def dispMoranParaBox(e):
        if c_Moran.value:
            tb_MoranPara.visible=True
            tb_MoranPara.update()
        else:
            tb_MoranPara.visible=False
            tb_MoranPara.update()
    tb_MoranPara = ft.TextField(label="nlag value(Moran)", hint_text="Enter an integer(default:10)")
    tb_MoranPara.visible=False
    c_Moran = ft.Checkbox(label="6. Moran", value=False, on_change=dispMoranParaBox)
    r_Moran = ft.Row([c_Moran,tb_MoranPara])
    
    ##7#Nmbroto
    def dispNumbrotoParaBox(e):
        if cb_numbroto.value:
            tb_NmbrotoPara.visible=True
            tb_NmbrotoPara.update()
        else:
            tb_NmbrotoPara.visible=False
            tb_NmbrotoPara.update()
    tb_NmbrotoPara = ft.TextField(label="nlag value(Nmbroto)", hint_text="Enter an integer(default:10)")
    tb_NmbrotoPara.visible=False
    cb_numbroto = ft.Checkbox(label="7. Nmbroto", value=False, on_change=dispNumbrotoParaBox)
    r_Nmbroto = ft.Row([cb_numbroto,tb_NmbrotoPara])
    
    ##8#Geary
    def dispGearyParaBox(e):
        if cb_Geary.value:
            tb_GearyPara.visible=True
            tb_GearyPara.update()
        else:
            tb_GearyPara.visible=False
            tb_GearyPara.update()
    tb_GearyPara = ft.TextField(label="nlag value(Geary)", hint_text="Enter an integer(default:10)")
    tb_GearyPara.visible=False
    cb_Geary = ft.Checkbox(label="8. Geary", value=False, on_change=dispGearyParaBox)
    r_Geary = ft.Row([cb_Geary,tb_GearyPara])
    
    ##9#SocNumber
    def dispSocnumberParaBox(e):
        if cb_socnumber.value:
            tb_socnumberPara.visible=True
            tb_socnumberPara.update()
        else:
            tb_socnumberPara.visible=False
            tb_socnumberPara.update()
    tb_socnumberPara = ft.TextField(label="nlag value(Socnumber)", hint_text="Enter an integer(default:10)")
    tb_socnumberPara.visible=False
    cb_socnumber = ft.Checkbox(label="9. Socnumber", value=False, on_change=dispSocnumberParaBox)
    r_Geary = ft.Row([cb_socnumber,tb_socnumberPara])
    
    ##10#QsOrder
    def dispQsOrderParaBox(e):
        if cb_QsOrder.value:
            tb_QsOrderPara.visible=True
            tb_QsOrderPara.update()
        else:
            tb_QsOrderPara.visible=False
            tb_QsOrderPara.update()
    tb_QsOrderPara = ft.TextField(label="nlag value(QsOrder)", hint_text="Enter an integer(default:10)")
    tb_QsOrderPara.visible=False
    cb_QsOrder = ft.Checkbox(label="10. QsOrder", value=False, on_change=dispQsOrderParaBox)
    r_QsOrder = ft.Row([cb_QsOrder,tb_QsOrderPara])
    
    ##11#SC-PseAAC-General
    def dispScgeneralParaBox(e):
        if cb_scGeneral.value:
            tb_scGeneral_lag.visible = True
            tb_scGeneral_lag.update()
            tb_scGeneral_w.visible = True
            tb_scGeneral_w.update()
        else:
            tb_scGeneral_lag.visible = False
            tb_scGeneral_lag.update()
            tb_scGeneral_w.visible = False
            tb_scGeneral_w.update()
    tb_scGeneral_lag = ft.TextField(label="lambda value(SC-PseAAC-General)", hint_text="Enter an integer(default:2)")
    tb_scGeneral_lag.visible = False
    tb_scGeneral_w = ft.TextField(label="w value(SC-PseAAC-General)", hint_text="(default:0.1)")
    tb_scGeneral_w.visible = False
    cb_scGeneral = ft.Checkbox(label="11. SC-PseAAC-General", value=False, on_change=dispScgeneralParaBox)
    r_scGeneral = ft.Row([cb_scGeneral,tb_scGeneral_lag,tb_scGeneral_w])
    
    ##12#PAAC
    def dispPaacParaBox(e):
        if cb_PAAC.value:
            tb_PAAC_l.visible = True
            tb_PAAC_l.update()
            tb_PAAC_w.visible = True
            tb_PAAC_w.update()
        else:
            tb_PAAC_l.visible = False
            tb_PAAC_l.update()
            tb_PAAC_w.visible = False
            tb_PAAC_w.update()
    tb_PAAC_l = ft.TextField(label="i_lambda value(PAAC)", hint_text="Enter an integer(default:30)")
    tb_PAAC_l.visible = False
    tb_PAAC_w = ft.TextField(label="w value(PAAC)", hint_text="Enter an integer(default:0.05)")
    tb_PAAC_w.visible = False
    cb_PAAC = ft.Checkbox(label="12. PAAC", value=False, on_change=dispPaacParaBox)
    r_PAAC = ft.Row([cb_PAAC,tb_PAAC_l,tb_PAAC_w])
   
    ##13#CTDC
    def dispCTDCParaBox(e):
        if cb_CTDC.value:
            t_CTDC.value = "|  No parameters required"
            t_CTDC.update()
        else:
            t_CTDC.value = ""
            t_CTDC.update()
    t_CTDC = ft.Text(value="", style="BODY_MEDIUM",color="#4f6a8f")
    cb_CTDC = ft.Checkbox(label="13. CTDC", value=False, on_change=dispCTDCParaBox)
    r_CTDC = ft.Row([cb_CTDC,t_CTDC])
    r_CTDC.visible = False
    ##14#CTDD
    def dispCTDDParaBox(e):
        if cb_CTDD.value:
            t_CTDD.value = "|  No parameters required"
            t_CTDD.update()
        else:
            t_CTDD.value = ""
            t_CTDD.update()
    t_CTDD = ft.Text(value="", style="BODY_MEDIUM",color="#4f6a8f")
    cb_CTDD = ft.Checkbox(label="14. CTDD", value=False, on_change=dispCTDDParaBox)
    r_CTDD = ft.Row([cb_CTDD,t_CTDD])
    r_CTDD.visible = False
    ##15#CTDT
    def dispCTDTParaBox(e):
        if cb_CTDT.value:
            t_CTDT.value = "|  No parameters required"
            t_CTDT.update()
        else:
            t_CTDT.value = ""
            t_CTDT.update()
    t_CTDT = ft.Text(value="", style="BODY_MEDIUM",color="#4f6a8f")
    cb_CTDT = ft.Checkbox(label="15. CTDT", value=False, on_change=dispCTDTParaBox)
    r_CTDT = ft.Row([cb_CTDT,t_CTDT])
    r_CTDT.visible = False
    ##16#DDE
    def dispDDEParaBox(e):
        if cb_DDE.value:
            t_DDE.value = "|  No parameters required"
            t_DDE.update()
        else:
            t_DDE.value = ""
            t_DDE.update()
    t_DDE = ft.Text(value="", style="BODY_MEDIUM",color="#4f6a8f")
    cb_DDE = ft.Checkbox(label="16. DDE", value=False, on_change=dispDDEParaBox)
    r_DDE = ft.Row([cb_DDE,t_DDE])
    r_DDE.visible = False
    ##17#scpseAAC
    def dispScPseParaBox(e):
        if cb_ScPseAAC.value:
            tb_ScPseAAC_lambda.visible = True
            tb_ScPseAAC_lambda.update()
            tb_ScPseAAC_w.visible = True
            tb_ScPseAAC_w.update()
        else:
            tb_ScPseAAC_lambda.visible = False
            tb_ScPseAAC_lambda.update()
            tb_ScPseAAC_w.visible = False
            tb_ScPseAAC_w.update()
    tb_ScPseAAC_lambda = ft.TextField(label="lambda value(SC-PseAAC)", hint_text="an integer(default:2)")
    tb_ScPseAAC_lambda.visible = False
    tb_ScPseAAC_w = ft.TextField(label="w value(SC-PseAAC)", hint_text="(default:0.1)")
    tb_ScPseAAC_w.visible = False
    cb_ScPseAAC = ft.Checkbox(label="17. SC-PseAAC", value=False, on_change=dispScPseParaBox)
    r_ScPseAAC = ft.Row([cb_ScPseAAC,tb_ScPseAAC_lambda,tb_ScPseAAC_w])
    
    ##18#CKSAAGP
    def disp_CKSAAGP_ParaBox(e):
        if cb_CKSAAGP.value:
            tb_CKSAAGP_l.visible = True
            tb_CKSAAGP_l.update()
            tb_CKSAAGP_No.visible = True
            tb_CKSAAGP_No.update()
        else:
            tb_CKSAAGP_l.visible = False
            tb_CKSAAGP_l.update()
            tb_CKSAAGP_No.visible = False
            tb_CKSAAGP_No.update()
    tb_CKSAAGP_l = ft.TextField(label="gap value(CKSAAGP)", hint_text="(default:5)")
    tb_CKSAAGP_l.visible = False
    tb_CKSAAGP_No = ft.TextField(label="red Scheme NO.(CKSAAGP)", hint_text="(default:1)")
    tb_CKSAAGP_No.visible = False
    cb_CKSAAGP = ft.Checkbox(label="18. CKSAAGP", value=False, on_change=disp_CKSAAGP_ParaBox)
    r_CKSAAGP = ft.Row([cb_CKSAAGP,tb_CKSAAGP_l,tb_CKSAAGP_No])
    
    ##19#CKSAAP
    def disp_CKSAAP_ParaBox(e):
        if cb_CKSAAP.value:
            tb_CKSAAP.visible = True
            tb_CKSAAP.update()
        else:
            tb_CKSAAP.visible = False
            tb_CKSAAP.update()
    tb_CKSAAP = ft.TextField(label="gap value(CKSAAP)", hint_text="(default:5)")
    tb_CKSAAP.visible = False
    cb_CKSAAP = ft.Checkbox(label="19. CKSAAP", value=False, on_change=disp_CKSAAP_ParaBox)
    r_CKSAAP = ft.Row([cb_CKSAAP,tb_CKSAAP])
   
    ##20#rTrip
    def disp_rTrip_ParaBox(e):
        if cb_rTrip.value:
            tb_rTrip_schm.visible = True
            tb_rTrip_schm.update()
            tb_rTrip_t.visible = True
            tb_rTrip_t.update()
        else:
            tb_rTrip_schm.visible = False
            tb_rTrip_schm.update()
            tb_rTrip_t.visible = False
            tb_rTrip_t.update()
    tb_rTrip_schm = ft.TextField(label="Reduced Scheme No.(rTrip,>=1)", hint_text="an integer(default:1)")
    tb_rTrip_schm.visible = False
    tb_rTrip_t = ft.TextField(label="Tripeptide Type No.(rTrip)", hint_text="(an integer:0~5)")
    tb_rTrip_t.visible = False
    cb_rTrip = ft.Checkbox(label="20. rTrip", value=False, on_change=disp_rTrip_ParaBox)
    r_rTrip = ft.Row([cb_rTrip,tb_rTrip_schm,tb_rTrip_t])
    
    ##21#userGivenCsv
    text_csvinfo = ft.Text(value="", style="BODY_MEDIUM",color="#4f6a8f")
    #1. pick files dialog
    def pick_csvflies_result(e: ft.FilePickerResultEvent):
        #
        text_csvinfo.value=(
            ",".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        text_csvinfo.update()
        if text_csvinfo.value=="Cancelled!":
            pass
        else:
            s_filePth = os.path.abspath(e.files[0].path)
            page.session.set("csvFilePth", s_filePth)
    pick_csvFile_dialog = ft.FilePicker(on_result=pick_csvflies_result)
    file_btn = ft.ElevatedButton(
        "Click and select the csv file",
        height=30,
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _:pick_csvFile_dialog.pick_files(allow_multiple=False),
    )
    file_btn.visible=False
    #User given csv feature
    def disp_slctCsv_btn(e):
        if cb_userCsv.value:
            file_btn.visible=True
            file_btn.update()
        else:
            file_btn.visible=False
            text_csvinfo.value = ""
            file_btn.update()
            text_csvinfo.update()
    cb_userCsv = ft.Checkbox(label="21. User‘s Feature", value=False, on_change=disp_slctCsv_btn)
    r_userCsv = ft.Row([cb_userCsv,file_btn,text_csvinfo])
    page.overlay.extend([pick_csvFile_dialog])
    
    #APAAC
    def disp_APAAC_ParaBox(e):
        if cb_APAAC.value:
            tb_APAAC_lambda.visible = True
            tb_APAAC_lambda.update()
            tb_APAAC_w.visible = True
            tb_APAAC_w.update()
        else:
            tb_APAAC_lambda.visible = False
            tb_APAAC_lambda.update()
            tb_APAAC_w.visible = False
            tb_APAAC_w.update()
    tb_APAAC_lambda = ft.TextField(label="Lambda Value", hint_text="an integer(default:30)")
    tb_APAAC_lambda.visible = False
    tb_APAAC_w = ft.TextField(label="w value", hint_text="a decimal(default:0.05)")
    tb_APAAC_w.visible = False
    cb_APAAC = ft.Checkbox(label="22. APAAC", value=False, on_change=disp_APAAC_ParaBox)
    r_APAAC = ft.Row([cb_APAAC,tb_APAAC_lambda,tb_APAAC_w])
    
    btn_setPara = ft.ElevatedButton(text="Set parameters", on_click=btn_setParas)
    btn_reset = ft.ElevatedButton(text="Initialize", on_click=resetParas)
    r_btnLine = ft.Row([btn_setPara,btn_reset])
    
    page.add(header, r_ordip, r_188, r_ACC, r_CC, r_AC, r_Moran,r_Nmbroto,r_Geary,
             r_QsOrder,r_scGeneral, r_PAAC, r_CTDC, r_CTDD, r_CTDT, r_DDE, r_ScPseAAC,
             r_CKSAAGP, r_CKSAAP, r_rTrip, r_userCsv, r_APAAC, r_btnLine)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)