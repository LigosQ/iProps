#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 10:55:19 2023

@author: sealight
"""
from nicegui import ui,app
import os,sys,platform
global pPath
pPath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pPath)
import nest_asyncio
# nest_asyncio.apply()
try:
    from geneSmartPth_mini import f_geneAbsPath_frmROOT
except:
    from files.geneSmartPth_mini import f_geneAbsPath_frmROOT

app.native.window_args['resizable'] = False
app.add_static_files(local_directory="UIelements",url_path="/UIelements")

ui.query("#app").style("position: relative")
ui.query(".nicegui-layout").style("width:1337px; height: 517px")
ui.query(".nicegui-layout").style("margin:0px auto;background-repeat: no-repeat;overflow: hidden; background-image: url('/UIelements/bg2.png')")

icon_about = ui.html("<img src='UIelements/logo.png' width='70px' height='70px' style='margin-left:17px'>")
icon_about.style("position:absolute; top: -7px; left: -2px;z-index:9; width: 67px")

Header = ui.label('iProps')
Header.style("width: 1337px;height:57px;position:absolute;top: 0px;background: black;opacity: 0.4;left:-17px; color: #ffffff")
Header.classes("text-5xl text-left pl-28 pt-1")

class Demo:
    def __init__(self):
        self.vis: bool = False
        
    def chgVis(self,e):
        self.vis = not(self.vis)
        ui.update()

demo = Demo()
isVisEmail = Demo()

with ui.row():
    #########
    ourEmailV = ui.label("tafchl(at)mail.nankai.edu.cn").bind_visibility_from(isVisEmail,"vis")
    ourEmailV.style("width: 75px; width: 57px; position: absolute; top: 12px; left: 907px; border: 0px;color: white;font-size:21px; ")
    #########
    ourmail = ui.button('Email', on_click=isVisEmail.chgVis)
    ourmail.style("width: 275px; width: 97px; position: absolute; top: 8px; left: 1197px; border: 1px solid white;color: white; ")

with ui.stepper().props('vertical').classes('w-full bg-gray-500/50 mt-9 text-white text-xl') as stepper:
    with ui.step('Introduction'):
        ui.label('iProp is a one-stop analysis and processing software based on numerical feature binary classification for the analysis andmodeling of protein sequence binary classification tasks.')
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
    with ui.step('Feature evaluation'):
        ui.label('The function is capable of computing up to 24 major numerical features of protein sequences. Before computation, users are allowed to set the built-in machine learning classifier for the purpose of classifying and evaluating these numerical features. Notably, the function supports handling imbalanced data during computation. When comparing numerical features laterally, the feature with the best classification ability is considered as the optimal numerical feature of this function. It\'s worth noting that the output of the reduced dipeptide feature consists of the numerical features corresponding to the best N reduction schemes out of 568 schemes in terms of classification ability. Finally, the function also conducts a preliminary evaluation and analysis of the optimal features through visualization.')
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
            ui.button('Back', on_click=stepper.previous).props('flat')
    with ui.step('Parameter setting'):
        ui.label('The function allows users to set parameters for the numerical feature calculation function. It\'s important to note that these parameters are written into a file. If parameters are not set after the current calculation, the next calculation will use the settings from this calculation. Therefore, attention should be paid to the state of parameters in each calculation. This function provides a reset feature to restore the default parameter settings.')
        with ui.stepper_navigation():
            ui.button('Done', on_click=stepper.next)
            ui.button('Back', on_click=stepper.previous).props('flat')
    with ui.step('Auto machine learning and interpretaion'):
        ui.label('This function offers automatic machine learning for user-provided numerical feature files. Additionally, it provides model interpretation through visualization, potentially offering valuable information for related research.')
        with ui.stepper_navigation():
            ui.button('Done', on_click=stepper.next)
            ui.button('Back', on_click=stepper.previous).props('flat')
    with ui.step('Cite us:'):
        ui.label('Feng Changli, Wu Jin, Wei Haiyan, Xu Lei, Zou Quan*. CRCF: A Method of Identifying Secretory Proteins of Malaria Parasites. IEEE/ACM Trans Comput Biol Bioinform. 2022 Jul-Aug;19(4):2149-2157. doi: 10.1109/TCBB.2021.3085589. Epub 2022 Aug 8. PMID: 34061749.')
        with ui.stepper_navigation():
            ui.button('Done', on_click=lambda: ui.notify('Now that you\'ve finished reading, you can use the above features by clicking on the three buttons.', type='positive'))
            ui.button('Back', on_click=stepper.previous).props('flat')

##########################
class ErrorCoding(Exception):
    pass

def f_openCmdAndRunCmd(s_cmd):
    import subprocess
    from time import sleep
    import win32api
    import win32con

    key_map = {
        "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34, "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39,
        "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
        "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
        "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
        'ENTER': 13, 'SHIFT': 16, 'CTRL': 17,
        '.':0xBE, '`':192,'~':192, '!':0x31, '@':0x32, "#": 0x33, "$": 0x34, 
        "%": 0x35, "^": 0x36, "&": 0x37, "*": 0x38, "(": 0x39,")": 0x30,
        '[': 219,'{': 219, ']': 221,'}': 221, '+': 107, '=': 107, '-': 109, '_': 109,
        ':':186,';':186,'\\':220,'/':191,',':188,"'":222,'.':190,' ':32}
    ls_upSyms = ['~','!','@','#','$','%','^','&','*','(',')','_','+','{','}',':']
    ls_downSyms = ['`','1','2','3','4','5','6','7','8','9','0','-','=','[',']','\\',';',"\'",',','.','/']
    ls_badSysbs = ['~','!','@','#','$','%','^','&','*','(',')','_','+','{','}','`',
                   '-','=','[',']','\\',';',"\'",',']

    for c_1symb in s_cmd:
        if c_1symb in ls_badSysbs:
            raise ErrorCoding(f'This version of the code only supports numbers and letters composed of the path, your path appears {c_1symb}')

    subprocess.Popen('start C:\windows\system32\cmd.exe', shell=True)
    sleep(0.2)

    for chr in s_cmd:
        if chr in ls_upSyms:
            i_keyCode = key_map[chr]
            win32api.keybd_event(16, 0, 0, 0)  
            win32api.keybd_event(i_keyCode, 0, 0, 0)  
            win32api.keybd_event(i_keyCode, 0, win32con.KEYEVENTF_KEYUP, 0)  
            win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)  
        elif chr in ls_downSyms:
            i_keyCode = key_map[chr]
            win32api.keybd_event(i_keyCode, 0, 0, 0)  
        elif chr.isupper():
            win32api.keybd_event(16, 0, 0, 0)  
            win32api.keybd_event(key_map[chr], 0, 0, 0)
            win32api.keybd_event(key_map[chr], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
            win32api.keybd_event(key_map[chr.upper()], 0, 0, 0)
    win32api.keybd_event(13,0,0,0) #enter
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
    

def f_newTermAndFlet(s_pyFileName):
    curWorkPth_abs = os.getcwd()
    curWorkPth_abs = str(curWorkPth_abs)
    #组合终端中的命令
    p_pyFile = f_geneAbsPath_frmROOT('',s_pyFileName)
    p_root = f_geneAbsPath_frmROOT('','')
    s_myCmd1 = ''.join(['cd ', p_root])
    s_myCmd2 = ''.join(['python ',p_pyFile])
    s_allCmd = ' && '.join([s_myCmd1, s_myCmd2])
    #获取当前的平台信息
    s_osInfo = platform.platform().lower()
    if ('macos' in s_osInfo):
        from applescript import tell
        tell.app('Terminal', 'do script "' + s_allCmd + '"' , background = True)
    elif ("linux" in s_osInfo):
        s_allCmd_linux = ''.join(["gnome-terminal -e 'bash -c \"",s_allCmd,";exec bash\"'"])
        os.system(s_allCmd_linux)
    elif "windows" in s_osInfo:
        s_myCmd1 = ''.join(['cd /d ', p_root])
        s_allCmd = '&&'.join([s_myCmd1, s_myCmd2])
        f_openCmdAndRunCmd(s_myCmd2)
    else:
        raise ErrorCoding('The code cannot identify the class of the current operating system. Currently, it only supports linux, MacOs, and windows.')

def f_runEval1():
    f_newTermAndFlet('featEval.py')

def f_runParas():
    f_newTermAndFlet('paraSetting.py')
    
def f_runEval3():
    f_newTermAndFlet('AutoMLPlus.py')

with ui.row():
    ##########
    with ui.button('',on_click=f_runEval1).\
    props("push outline rounded").style('''width: 307px;height:267px;position:absolute;
                        top:527px;left:150px;
                        font-size:37px;border:1px solid white;'''):
         ui.image('UIelements/eval2.png').style("width:227px")
         ui.label('Auto Feature Evaluation').classes('text-center text-white hover:text-rose-400 leading-9 normal-case')
    ############
    with ui.button('',on_click=f_runParas).classes('text-center text-white').\
        props("push outline rounded").style('''width: 307px;height:267px;position:absolute;
                            top:527px;left:515px;
                            font-size:37px;border:1px solid white;'''):
        ui.image('UIelements/setting.png').style("width:227px")
        ui.label('Parameters Setting').classes('text-center text-white hover:text-rose-400 leading-9 normal-case')
    ############
    with ui.button('',on_click=f_runEval3).classes('text-center text-white').\
        props("push outline rounded").style('''width: 307px;height:267px;position:absolute;
                            top:527px;left:877px;
                            font-size:37px;border:1px solid white;'''):
        ui.image('UIelements/interp2.png').style("width:227px")
        ui.label('Auto ML Interpretation').classes('text-center text-white hover:text-rose-400 leading-9 normal-case')
ui.query(".q-stepper__title").style('font-size:21px; z-index:99;opacity:1; color: yellow')

#####################
ui.run(
    favicon="🚀",
    title="Test GUI",
    native=True,
    window_size=(1337, 857),
    fullscreen=False,
    reload=False
)