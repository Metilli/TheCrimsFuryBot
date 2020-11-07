#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import random
import time
import datetime 
import json
import threading
import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import CommonFunctionsModule as common
import AssultModule as assult
import GangRobberyModule as gangRob
import SingleRobberyModule as singleRob
from firebase import firebase
import uuid 
from PIL import Image, ImageTk
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("TheCrims Fury Bot v1")

def quickedit(enabled=1): # This is a patch to the system that sometimes hangs
        import ctypes
        '''
        Enable or disable quick edit mode to prevent system hangs, sometimes when using remote desktop
        Param (Enabled)
        enabled = 1(default), enable quick edit mode in python console
        enabled = 0, disable quick edit mode in python console
        '''
        # -10 is input handle => STD_INPUT_HANDLE (DWORD) -10 | https://docs.microsoft.com/en-us/windows/console/getstdhandle
        # default = (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x200)
        # 0x40 is quick edit, #0x20 is insert mode
        # 0x8 is disabled by default
        # https://docs.microsoft.com/en-us/windows/console/setconsolemode
        kernel32 = ctypes.windll.kernel32
        if enabled:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
            print("Console Quick Edit Enabled")
        else:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))
            print("Console Quick Edit Disabled")

quickedit(0) # Disable quick edit in terminal

def getPCcode():
    return str(hex(uuid.getnode()))

def stopBot():
    common.getCurrentStats()
    botStatusSingle.set("Bot mode: Stopping")
    botStatusGang.set("Bot mode: Stopping")
    botStatusAssult.set("Bot mode: Stopping")
    singleRob.stopRobbery = True
    gangRob.stopRobbery = True
    assult.isAssultStop = True
    botMode = 0
    while not singleRob.isRobberyDone:
        time.sleep(0.1)
    while not gangRob.isRobberyDone:
        time.sleep(0.1)
    while not assult.isAssultDone:
        time.sleep(0.05)
    global assultStep
    assultStep = 0
    time.sleep(0.5)
    botStatusSingle.set("Bot mode: Ready to start")
    botStatusGang.set("Bot mode: Ready to start")
    botStatusAssult.set("Bot mode: Ready to start")
    enableButtons()

#Button Function Region Start
def singleRobbery(ticketCount):
    common.browser_navigation_panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    common.getCurrentStats()
    botStatusSingle.set("Bot mode: Doing single robbery")
    botStatusGang.set("Bot mode: Doing single robbery")
    botStatusAssult.set("Bot mode: Doing single robbery")
    common.botMode = 1
    setHospitalPrisonOutOptions()
    time.sleep(0.1)
    ticketInt = int(ticketCount.get())
    #singleRob.startRobbery(ticketInt)
    disableButtons()
    singleThread = threading.Thread(target=singleRob.startRobbery, args=(ticketInt,))
    singleThread.start()
  

def gangRobbery(ticketCount,isLeader):
    common.browser_navigation_panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    common.getCurrentStats()
    isLeaderBool = False
    if isLeader.get() == 1:
        isLeaderBool = True
    botStatusSingle.set("Bot mode: Doing gang robbery")
    botStatusGang.set("Bot mode: Doing gang robbery")
    botStatusAssult.set("Bot mode: Doing gang robbery")
    common.botMode = 2
    setHospitalPrisonOutOptions()
    time.sleep(0.1)
    ticketInt = int(ticketCount.get())
    disableButtons()
    #gangRob.startRobbery(ticketInt,isLeaderBool)
    gangRobThread = threading.Thread(target=gangRob.startRobbery, args=(ticketInt,isLeaderBool,))
    gangRobThread.start()
  
def assultFunc(isGangCheck):
    common.browser_navigation_panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    common.getCurrentStats()
    assult.isAssultStop = False
    isGangAssult = False
    if isGangCheck == 1:
        isGangAssult = True
    botStatusAssult.set("Bot mode: Doing assults")
    botStatusSingle.set("Bot mode: Doing assults")
    botStatusGang.set("Bot mode: Doing assults")
    common.botMode = 3
    setHospitalPrisonOutOptions()
    time.sleep(0.1)
    disableButtons()
    #assult.assult(isGangAssult)
    assultThread = threading.Thread(target=assult.assult, args=(isGangAssult,))
    assultThread.start()

def setHospitalPrisonOutOptions():
    if assultisExitHospitalVar.get() == 1:
        if assultexitHospitalCbo.current() == 0:
            common.assultisUsePrivateCareHospital = True
            common.assultisUseCreditHospital = False
        else:
            common.assultisUsePrivateCareHospital = False
            common.assultisUseCreditHospital = True
    else:
        common.assultisUsePrivateCareHospital = False
        common.assultisUseCreditHospital = False

    if isExitPrisonVar.get() == 1:
        if exitPrisonCbo.current() == 0:
            common.assultisUseBribePrison = True
            common.assultisUseFreeCardPrison = False
            common.assultisUseCreditPrison = False
        elif exitPrisonCbo.current() == 1:
            common.assultisUseBribePrison = False
            common.assultisUseFreeCardPrison = True
            common.assultisUseCreditPrison = False
        else:
            common.assultisUseBribePrison = False
            common.assultisUseFreeCardPrison = False
            common.assultisUseCreditPrison = True
    else:
        common.assultisUseBribePrison = False
        common.assultisUseFreeCardPrison = False
        common.assultisUseCreditPrison = False

    if SingleRobberyisExitHospitalVar.get() == 1:
        if SingleRobberyexitHospitalCbo.current() == 0:
            common.singleRobisUsePrivateCareHospital = True
            common.singleRobisUseCreditHospital = False
        else:
            common.singleRobisUsePrivateCareHospital = False
            common.singleRobisUseCreditHospital = True
    else:
        common.singleRobisUsePrivateCareHospital = False
        common.singleRobisUseCreditHospital = False

    if GangRobberyisExitHospitalVar.get() == 1:
        if GangRobberyexitHospitalCbo.current() == 0:
            common.gangRobisUsePrivateCareHospital = True
            common.gangRobisUseCreditHospital = False
        else:
            common.gangRobisUsePrivateCareHospital = False
            common.gangRobisUseCreditHospital = True
    else:
        common.gangRobisUsePrivateCareHospital = False
        common.gangRobisUseCreditHospital = False


#Button Function Region End


def saveLevelSettingsFunc():
    try:
        data["isAttack"]["Hitman"] = isAttackHitman.get()
        data["isAttack"]["Pimp"] = isAttackPimp.get()
        data["isAttack"]["Businessman"] = isAttackBusinessman.get()
        data["isAttack"]["Robber"] = isAttackRobber.get()
        data["isAttack"]["Dealer"] = isAttackDealer.get()
        data["isAttack"]["Broker"] = isAttackBroker.get()
        data["isAttack"]["Gangster"] = isAttackGangster.get()
        data["attackLevels"]["PimpLevel"] = PimpLevelVarMin.get() + "," + PimpLevelVarMax.get()
        data["attackLevels"]["HitmanLevel"] = HitmanLevelVarMin.get()+ "," +HitmanLevelVarMax.get()
        data["attackLevels"]["BusinessmanLevel"] = BusinessmanLevelVarMin.get()+ "," +BusinessmanLevelVarMax.get()
        data["attackLevels"]["RobberLevel"] = RobberLevelVarMin.get()+ "," +RobberLevelVarMax.get()
        data["attackLevels"]["DealerLevel"] = DealerLevelVarMin.get()+ "," +DealerLevelVarMax.get()
        data["attackLevels"]["BrokerLevel"] = BrokerLevelVarMin.get()+ "," +BrokerLevelVarMax.get()
        
        assult.cacheAttackArrays()
        with open(common.resource_path('./profile/config.txt'), 'w',encoding='utf8') as outfile:
            json.dump(data, outfile,indent=4,ensure_ascii=False)
        messagebox.showinfo("Save successful", "Assult levels saved successful.")
    except:
        messagebox.showerror("Save failed", "Something went wrong.")

def saveSettingsFunc():
    try:
        data["username"] = usernameVar.get()
        data["password"] = passwordVar.get()
        data["robberyPageMin"] = float(openRobberyPageMinVar.get())
        data["robberyPageMax"] = float(openRobberyPageMaxVar.get())
        data["robMin"] = float(clickRobMinVar.get())
        data["robMax"] = float(clickRobMaxVar.get())
        data["nightClubMin"] = float(nightlifeMinVar.get())
        data["nightClubMax"] = float(nightlifeMaxVar.get())
        data["enterClubMin"] = float(nightclubMinVar.get())
        data["enterClubMax"] = float(nightclubMaxVar.get())
        data["buyMin"] = float(drinkMinVar.get())
        data["buyMax"] = float(drinkMaxVar.get())
        data["exitMin"] = float(exitMinVar.get())
        data["exitMax"] = float(exitMaxVar.get())
        data["gangRobMin"] = float(gangclickRobMinVar.get())
        data["gangRobMax"] = float(gangclickRobMaxVar.get())
        data["runFromAssultMin"] = float(assultExitMinVar.get())
        data["runFromAssultMax"] = float(assultExitMaxVar.get())
        data["attackOpenMin"] = float(openAssultMinVar.get())
        data["attackOpenMax"] = float(openAssultMaxVar.get())
        data["attackSingleMin"] = float(selectAssultMinVar.get())
        data["attackSingleMax"] = float(selectAssultMaxVar.get())
        data["attackDoneMin"] = float(doAssultMinVar.get())
        data["attackDoneMax"] = float(doAssultMaxVar.get())
        data["attackEnterClubMin"] = float(assultEnterClubMinVar.get())
        data["attackEnterClubMax"] = float(assultEnterClubMaxVar.get())
        data["attackStayClubMin"] = float(assultStayClubMinVar.get())
        data["attackStayClubMax"] = float(assultStayClubMaxVar.get())

        with open(common.resource_path('./profile/config.txt'), 'w',encoding='utf8') as outfile:
            json.dump(data, outfile,indent=4,ensure_ascii=False)
        messagebox.showinfo("Save successful", "Settings saved successful.")
    except:
        messagebox.showerror("Save failed", "Something went wrong.")
    

def disableButtons():
    singleRobberyButton['state'] = tk.DISABLED
    gangRobberyButton['state'] = tk.DISABLED
    assultButton['state'] = tk.DISABLED
    HitmanLevel['state'] = tk.DISABLED
    BusinessmanLevel['state'] = tk.DISABLED
    PimpLevel['state'] = tk.DISABLED
    RobberLevel['state'] = tk.DISABLED
    BrokerLevel['state'] = tk.DISABLED
    DealerLevel['state'] = tk.DISABLED
    saveLevelSettings['state'] = tk.DISABLED
    isLeaderCheckButton['state'] = tk.DISABLED
    isGangAssultCheckButton['state'] = tk.DISABLED

def enableButtons():
    singleRobberyButton['state'] = tk.NORMAL
    gangRobberyButton['state'] = tk.NORMAL
    assultButton['state'] = tk.NORMAL
    HitmanLevel['state'] = tk.NORMAL
    BusinessmanLevel['state'] = tk.NORMAL
    PimpLevel['state'] = tk.NORMAL
    RobberLevel['state'] = tk.NORMAL
    BrokerLevel['state'] = tk.NORMAL
    DealerLevel['state'] = tk.NORMAL
    saveLevelSettings['state'] = tk.NORMAL
    isLeaderCheckButton['state'] = tk.NORMAL
    isGangAssultCheckButton['state'] = tk.NORMAL

def checkAccount(username,password):
    firebaseRef = firebase.FirebaseApplication('https://thecrimsfurybot.firebaseio.com/', None)
    result = firebaseRef.get('/PremiumAccounts', '')
    isMatch = False
    isExpire = False
    isSamePC = False
    today = int(currentTime)
    accountData = json.loads(str(result).replace("'", "\""))
    i = 0
    for account in accountData:
        if username == str(accountData[account]["username"]) and password == str(accountData[account]["password"]):
            isMatch = True
            if today < int(accountData[account]["expireDate"]):
                try:
                    if getPCcode() == str(accountData[account]["pcCode"]):
                        isSamePC = True
                        accountStatusVar.set("Successful login. Bot expire time: " + str(datetime.datetime.fromtimestamp(accountData[account]["expireDate"]))+" (London Time)")
                        enableBot()
                        break
                    else:
                        isSamePC = False
                        accountStatusVar.set("Login failed. You can't share your account with others.")
                        break
                except:
                    insterPCcode(account,getPCcode())
                    accountStatusVar.set("Successful login. Bot expire time: " + str(datetime.datetime.fromtimestamp(accountData[account]["expireDate"])))
                    isSamePC = True
                    data["botUsername"] = username
                    data["botPassword"] = password
                    with open(common.resource_path('./profile/config.txt'), 'w',encoding='utf8') as outfile:
                        json.dump(data, outfile,indent=4,ensure_ascii=False)
                    enableBot()
                    break
            else:
                isExpire = True
                accountStatusVar.set("Login failed. Bot expire time is : " + str(datetime.datetime.fromtimestamp(accountData[account]["expireDate"])) + " (London Time)")
                break
        i += 1

    if not isMatch:
        accountStatusVar.set("Username or password is wrong.")

def insterPCcode(parent,code):
    firebaseRef = firebase.FirebaseApplication('https://thecrimsfurybot.firebaseio.com/', None)
    result = firebaseRef.put("/PremiumAccounts/"+parent,"pcCode",code)


def disableBot():
    tabControl.hide(tabSingleRobbery)
    tabControl.hide(tabGangRobbery)
    tabControl.hide(tabAssult)
    tabControl.hide(tabSettings)
    root.geometry("300x450")

def enableBot():
    tabControl.add(tabSingleRobbery)
    tabControl.add(tabGangRobbery)
    tabControl.add(tabAssult)
    tabControl.add(tabSettings)
    tabControl.pack(expand=1, fill="both")
    root.geometry("300x600")
#region Init

currentTime = 0
resourcePath = common.resource_path('./selenium/chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver2 = webdriver.Chrome(options=chrome_options, executable_path=resourcePath)
start_url = "http://worldtimeapi.org/api/timezone/Europe/London.txt"
driver2.get(start_url)
allText = driver2.find_element(By.XPATH,"//*[contains(text(),'unixtime')]").text
arr = allText.split("\n")
for item in arr:
    if "unixtime" in item:
        itemArr = item.split(":")
        currentTime = itemArr[1]


options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-logging","enable-automation"])
resourcePath = common.resource_path('./selenium/chromedriver.exe')
driver = webdriver.Chrome(options=options, executable_path=resourcePath)
driver.get("https://www.thecrims.com")
driver.maximize_window()

common.driver = driver
singleRob.driver = driver
gangRob.driver = driver
assult.driver = driver

file = open(common.resource_path('./profile/config.txt'), "r", encoding='utf8')
configText = file.read()
data = json.loads(configText)
assult.data = data
singleRob.data = data
gangRob.data = data
common.data = data

common.browser_navigation_panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
try:
    common.Print("-------------------------------------------\n\n\n\n\n\nWelcome to TheCrims Furry Bot")
    common.Print("We are starting a new day of crime")
    common.login(data["username"],data["password"])
    today = datetime.datetime.today()
    dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
    common.Print("date and time = "+ dt_string)	
    time.sleep(0.5)
    if "newspaper" in driver.current_url:
        common.Print("Login automatically")
    else:
        common.Print("Login manually")
except:
  common.Print("Login manually")

#endregion

#region Interface
root = tk.Tk()
root.attributes('-topmost', True)
root.title("TheCrims Fury Bot Beta v1.0")
root.iconphoto(False, tk.PhotoImage(file=common.resource_path('./icon.gif')))

tabControl = ttk.Notebook(root)
tabLogin = ttk.Notebook(tabControl)
tabSingleRobbery = ttk.Frame(tabControl)
tabGangRobbery = ttk.Frame(tabControl)
tabAssult = ttk.Frame(tabControl)
tabSettings = ttk.Frame(tabControl)
tabControl.add(tabLogin, text='Login')
tabControl.add(tabSingleRobbery, text='Single Robbery')
tabControl.add(tabGangRobbery, text='Gang Robbery')
tabControl.add(tabAssult, text='Assult')
tabControl.add(tabSettings, text='Settings')
tabControl.pack(expand=1, fill="both")

#region tabLogin
im = ImageTk.PhotoImage(Image.open(common.resource_path('./logo.gif'))) # the one-liner I used in my app
w1 = tk.Label(tabLogin, image=im,borderwidth =0,highlightthickness = 0)
w1.grid(column= 0, row = 0,columnspan=2,padx = 10,pady = 10)


usernameLabel = ttk.Label(tabLogin, justify=tk.LEFT, text = "Username", background="white")
usernameLabel.grid(column = 0, row = 1,padx = 10,pady = 10)

usernameEntryVar = tk.StringVar(tabLogin, value='')
usernameEntry = ttk.Entry(tabLogin, width = 15, textvariable = usernameEntryVar)
usernameEntry.grid(column = 1, row = 1,padx = 10,pady = 10)

passwordLabel = ttk.Label(tabLogin, justify=tk.LEFT, text = "Password", background="white")
passwordLabel.grid(column = 0, row = 2,padx = 10,pady = 10)

passwordEntryVar = tk.StringVar(tabLogin, value='')
passwordEntry = ttk.Entry(tabLogin, width = 15, textvariable = passwordEntryVar)
passwordEntry.grid(column = 1, row = 2,padx = 10,pady = 10)

loginButton = ttk.Button(tabLogin, text = "Login", command = lambda:checkAccount(usernameEntryVar.get(),passwordEntryVar.get()))
loginButton.grid(column= 0, row = 3,columnspan=2,padx = 10,pady = 10)

accountStatusVar = tk.StringVar(tabLogin)
accountStatus = ttk.Label(tabLogin, textvariable=accountStatusVar,background="white",wraplength = "250")
accountStatus.grid(column= 0, row = 4,columnspan=2,padx = 10,pady = 10)
accountStatusVar.set("You must be logged in to start. Contact e-mail address: thecrimsfurybot@gmail.com")

usernameEntryVar.set(data["botUsername"])
passwordEntryVar.set(data["botPassword"])
#endregion

#region tabSingleRob

ticketLabel = ttk.Label(tabSingleRobbery, justify=tk.LEFT, text = "Ticket to use")
ticketLabel.grid(column = 0, row = 0)
ticketLabel.grid(padx = 10,pady = 10)

ticketCountSingleRobbery = tk.StringVar(root, value='0')
ticketTextBox = ttk.Entry(tabSingleRobbery, width = 15, textvariable = ticketCountSingleRobbery)
ticketTextBox.grid(column = 1, row = 0,padx = 10,pady = 10)

singleRobberyButton = ttk.Button(tabSingleRobbery, text = "Single Robbery", command = lambda:singleRobbery(ticketCountSingleRobbery))
singleRobberyButton.grid(column= 0, row = 1,columnspan=2,padx = 10,pady = 10)

SingleRobberyisExitHospitalVar = tk.IntVar(tabSingleRobbery)
SingleRobberyisExitHospital = ttk.Checkbutton(tabSingleRobbery, text="Auto exit hospital", variable=SingleRobberyisExitHospitalVar)
SingleRobberyisExitHospital.grid(column = 0,columnspan = 1,row=3,padx = 5,pady = 5)

SingleRobberyexitHospitalVar = tk.StringVar() 
SingleRobberyexitHospitalCbo = ttk.Combobox(tabSingleRobbery, textvariable = SingleRobberyexitHospitalVar) 
SingleRobberyexitHospitalCbo['values'] = ("Private care","Credit") 
SingleRobberyexitHospitalCbo.grid(column = 1,columnspan = 1, row = 3,padx = 5,pady = 5)
SingleRobberyexitHospitalCbo.current(0)

botStatusSingle = tk.StringVar(tabSingleRobbery)
botStatus = ttk.Label(tabSingleRobbery, textvariable=botStatusSingle)
botStatus.grid(column = 0, row = 4)
botStatus.grid(columnspan = 3,padx = 10,pady = 20)
botStatusSingle.set("Bot mode: Ready to start")

#stopLabel = tk.Label(tabSingleRobbery, text = "Press ESC to stop",fg = "red")
#stopLabel.grid(column = 0, row = 6)
#stopLabel.grid(columnspan = 3,padx = 10,pady = 10)

stopBot1 = ttk.Button(tabSingleRobbery, text = "Stop Bot", command = stopBot)
stopBot1.grid(column= 0, row = 6,columnspan=2,padx = 10,pady = 10)
#endregion

#region tabGangRobbery

ticketLabel2 = ttk.Label(tabGangRobbery, justify=tk.LEFT, text = "Ticket to use")
ticketLabel2.grid(column = 0, row = 0)
ticketLabel2.grid(padx = 10,pady = 10)
  
ticketCountGangRobbery = tk.StringVar(root, value='0')
ticketTextBox2 = ttk.Entry(tabGangRobbery, width = 15, textvariable = ticketCountGangRobbery)
ticketTextBox2.grid(column = 1, row = 0,padx = 10,pady = 10)

isLeaderCheckValue = tk.IntVar(tabGangRobbery)
gangRobberyButton = ttk.Button(tabGangRobbery, text = "Gang Robbery", command = lambda:gangRobbery(ticketCountGangRobbery,isLeaderCheckValue))
gangRobberyButton.grid(column= 0, row = 1,columnspan=2,padx = 10,pady = 10)

isLeaderCheckButton = ttk.Checkbutton(tabGangRobbery, text="Gang Leader", variable=isLeaderCheckValue)
isLeaderCheckButton.grid(column = 0,columnspan = 2,row=2,padx = 10,pady = 5)

GangRobberyisExitHospitalVar = tk.IntVar(tabGangRobbery)
GangRobberyisExitHospital = ttk.Checkbutton(tabGangRobbery, text="Auto exit hospital", variable=GangRobberyisExitHospitalVar)
GangRobberyisExitHospital.grid(column = 0,columnspan = 1,row=3,padx = 5,pady = 5)

GangRobberyexitHospitalVar = tk.StringVar() 
GangRobberyexitHospitalCbo = ttk.Combobox(tabGangRobbery, textvariable = GangRobberyexitHospitalVar) 
GangRobberyexitHospitalCbo['values'] = ("Private care","Credit") 
GangRobberyexitHospitalCbo.grid(column = 1,columnspan = 1, row = 3,padx = 5,pady = 5)
GangRobberyexitHospitalCbo.current(0)

botStatusGang = tk.StringVar(tabGangRobbery)
botStatus2 = ttk.Label(tabGangRobbery, textvariable=botStatusGang)
botStatus2.grid(column = 0, row = 4)
botStatus2.grid(columnspan = 3,padx = 10,pady = 20)
botStatusGang.set("Bot mode: Ready to start")

emptyLabel4 = ttk.Label(tabGangRobbery, justify=tk.LEFT, text="  ")
emptyLabel4.grid(column = 0, row = 5,padx = 10,pady = 10)
  
#stopLabel2 = tk.Label(tabGangRobbery, text = "Press ESC to stop",fg = "red")
#stopLabel2.grid(column = 0, row = 6)
#stopLabel2.grid(columnspan = 3,padx = 10,pady = 10)

stopBot2 = ttk.Button(tabGangRobbery, text = "Stop Bot", command = stopBot)
stopBot2.grid(column= 0, row = 6,columnspan=2,padx = 10,pady = 10)
#endregion

#region tabAssult
rowIndex = 0
isGangAssultCheckValue = tk.IntVar(tabAssult)
assultButton = ttk.Button(tabAssult, text = "Assult", command = lambda:assultFunc(isGangAssultCheckValue.get()))
assultButton.grid(column=0, row = rowIndex, columnspan = 3,padx = 5,pady = 5)
rowIndex += 1

isGangAssultCheckButton = ttk.Checkbutton(tabAssult, text="Gang Assult", variable=isGangAssultCheckValue)
isGangAssultCheckButton.grid(column = 0,columnspan = 3,row=rowIndex,padx = 5,pady = 5)
rowIndex += 1

assultisExitHospitalVar = tk.IntVar(tabAssult)
assultisExitHospital = ttk.Checkbutton(tabAssult, text="Auto exit hospital", variable=assultisExitHospitalVar)
assultisExitHospital.grid(column = 0,columnspan = 1,row=rowIndex,padx = 5,pady = 5)

assultexitHospitalVar = tk.StringVar() 
assultexitHospitalCbo = ttk.Combobox(tabAssult, textvariable = assultexitHospitalVar) 
assultexitHospitalCbo['values'] = ("Private care","Credit") 
assultexitHospitalCbo.grid(column = 1,columnspan = 2, row = rowIndex,padx = 5,pady = 5)
assultexitHospitalCbo.current(0)
rowIndex += 1

isExitPrisonVar = tk.IntVar(tabAssult)
isExitPrison = ttk.Checkbutton(tabAssult, text="Auto exit prison", variable=isExitPrisonVar)
isExitPrison.grid(column = 0,columnspan = 1,row=rowIndex,padx = 5,pady = 5)

exitPrisonVar = tk.StringVar() 
exitPrisonCbo = ttk.Combobox(tabAssult, textvariable = exitPrisonVar) 
exitPrisonCbo['values'] = ("Bribe","Free card","Credit") 
exitPrisonCbo.grid(column = 1,columnspan = 2, row = rowIndex,padx = 5,pady = 5)
exitPrisonCbo.current(0)
rowIndex += 1

checkBoxExplanationLabel = ttk.Label(tabAssult, justify=tk.LEFT, text="Check characters and set min and max levels to attack.",wraplength=220)
checkBoxExplanationLabel.grid(column = 0, columnspan = 3, row = rowIndex,padx = 5,pady = 5)

minTimeLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Min level")
minTimeLabel.grid(column = 1,columnspan = 1, row = rowIndex, padx = 5,pady = 3)
maxTimeLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Max level")
maxTimeLabel.grid(column = 2,columnspan = 1, row = rowIndex, padx = 5,pady = 3)
rowIndex += 1

isAttackHitman = tk.IntVar(tabAssult)
isAttackBusinessman = tk.IntVar(tabAssult)
isAttackPimp = tk.IntVar(tabAssult)
isAttackRobber = tk.IntVar(tabAssult)
isAttackDealer = tk.IntVar(tabAssult)
isAttackBroker = tk.IntVar(tabAssult)
isAttackGangster = tk.IntVar(tabAssult)

isAttackHitman.set(data["isAttack"]["Hitman"])
isAttackBusinessman.set(data["isAttack"]["Businessman"])
isAttackPimp.set(data["isAttack"]["Pimp"])
isAttackRobber.set(data["isAttack"]["Robber"])
isAttackDealer.set(data["isAttack"]["Dealer"])
isAttackBroker.set(data["isAttack"]["Broker"])
isAttackGangster.set(data["isAttack"]["Gangster"])

HitmanLabel = ttk.Checkbutton(tabAssult, text="Hitman", variable=isAttackHitman)
HitmanLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
HitmanLevelVarMin = tk.StringVar() 
HitmanLevel = ttk.Combobox(tabAssult, width = 5, textvariable = HitmanLevelVarMin) 
HitmanLevel['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
HitmanLevel.grid(column = 1,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["HitmanLevel"].split(",")[0]) - 1
HitmanLevel.current(currentLevel)
HitmanLevelVarMax = tk.StringVar() 
HitmanLevel2 = ttk.Combobox(tabAssult, width = 5, textvariable = HitmanLevelVarMax) 
HitmanLevel2['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
HitmanLevel2.grid(column = 2,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["HitmanLevel"].split(",")[1]) - 1
HitmanLevel2.current(currentLevel)
rowIndex +=1

BusinessmanLabel = ttk.Checkbutton(tabAssult, text="Businessman", variable=isAttackBusinessman)
BusinessmanLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
BusinessmanLevelVarMin = tk.StringVar() 
BusinessmanLevel = ttk.Combobox(tabAssult, width = 5, textvariable = BusinessmanLevelVarMin) 
BusinessmanLevel['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
BusinessmanLevel.grid(column = 1,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["BusinessmanLevel"].split(",")[0]) - 1
BusinessmanLevel.current(currentLevel)
BusinessmanLevelVarMax = tk.StringVar() 
BusinessmanLevel2 = ttk.Combobox(tabAssult, width = 5, textvariable = BusinessmanLevelVarMax) 
BusinessmanLevel2['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
BusinessmanLevel2.grid(column = 2,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["BusinessmanLevel"].split(",")[1]) - 1
BusinessmanLevel2.current(currentLevel)
rowIndex += 1

PimpLabel = ttk.Checkbutton(tabAssult, text="Pimp", variable=isAttackPimp)
PimpLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)

PimpLevelVarMin = tk.StringVar() 
PimpLevel = ttk.Combobox(tabAssult, width = 5, textvariable = PimpLevelVarMin) 
PimpLevel['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
PimpLevel.grid(column = 1,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["PimpLevel"].split(",")[0])-1
PimpLevel.current(currentLevel)

PimpLevelVarMax = tk.StringVar() 
PimpLevel2 = ttk.Combobox(tabAssult, width = 5, textvariable = PimpLevelVarMax) 
PimpLevel2['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
PimpLevel2.grid(column = 2,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["PimpLevel"].split(",")[1])-1
PimpLevel2.current(currentLevel)
rowIndex += 1

RobberLabel = ttk.Checkbutton(tabAssult, text="Robber", variable=isAttackRobber)
RobberLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
RobberLevelVarMin = tk.StringVar() 
RobberLevel = ttk.Combobox(tabAssult, width = 5, textvariable = RobberLevelVarMin) 
RobberLevel['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
RobberLevel.grid(column = 1,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["RobberLevel"].split(",")[0])-1
RobberLevel.current(currentLevel)
RobberLevelVarMax = tk.StringVar() 
RobberLevel2 = ttk.Combobox(tabAssult, width = 5, textvariable = RobberLevelVarMax) 
RobberLevel2['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
RobberLevel2.grid(column = 2,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["RobberLevel"].split(",")[1])-1
RobberLevel2.current(currentLevel)
rowIndex +=1 

DealerLabel = ttk.Checkbutton(tabAssult,  text="Dealer", variable=isAttackDealer)
DealerLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
DealerLevelVarMin = tk.StringVar() 
DealerLevel = ttk.Combobox(tabAssult, width = 5, textvariable = DealerLevelVarMin) 
DealerLevel['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
currentLevel = int(data["attackLevels"]["DealerLevel"].split(",")[0])-1
DealerLevel.current(currentLevel)
DealerLevel.grid(column = 1,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
DealerLevelVarMax = tk.StringVar() 
DealerLevel2 = ttk.Combobox(tabAssult, width = 5, textvariable = DealerLevelVarMax) 
DealerLevel2['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
DealerLevel2.grid(column = 2,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["DealerLevel"].split(",")[1])-1
DealerLevel2.current(currentLevel)
rowIndex +=1 

BrokerLabel = ttk.Checkbutton(tabAssult,  text="Broker", variable=isAttackBroker)
BrokerLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
BrokerLevelVarMin = tk.StringVar() 
BrokerLevel = ttk.Combobox(tabAssult, width = 5, textvariable = BrokerLevelVarMin) 
BrokerLevel['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
BrokerLevel.grid(column = 1,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["BrokerLevel"].split(",")[0]) -1
BrokerLevel.current(currentLevel)
BrokerLevelVarMax = tk.StringVar() 
BrokerLevel2 = ttk.Combobox(tabAssult, width = 5, textvariable = BrokerLevelVarMax) 
BrokerLevel2['values'] = ('1','2', '3','4', '5','6', '7','8', '9','10', '11','12', '13') 
BrokerLevel2.grid(column = 2,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
currentLevel = int(data["attackLevels"]["BrokerLevel"].split(",")[1]) -1
BrokerLevel2.current(currentLevel)
rowIndex += 1

GangsterLabel = ttk.Checkbutton(tabAssult,  text="Gangster", variable=isAttackGangster)
GangsterLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex,padx = 5,pady = 3)
rowIndex += 1

saveLevelSettings = ttk.Button(tabAssult, text = "Save Levels", command = saveLevelSettingsFunc)
saveLevelSettings.grid(column=0, row = rowIndex, columnspan = 3,padx = 5,pady = 10)
rowIndex += 1

botStatusAssult = tk.StringVar(tabAssult)
botStatus3 = ttk.Label(tabAssult, textvariable=botStatusAssult)
botStatus3.grid(column = 0, row = rowIndex)
botStatus3.grid(columnspan = 4,padx = 5,pady = 20)
botStatusAssult.set("Bot mode: Ready to start")
rowIndex += 1


#stopLabel3 = tk.Label(tabAssult, text = "Press ESC to stop",fg = "red")
#stopLabel3.grid(column = 0, row = rowIndex)
#stopLabel3.grid(columnspan = 3,padx = 5,pady = 10)
#rowIndex += 1

stopBot3 = ttk.Button(tabAssult, text = "Stop Bot", command = stopBot)
stopBot3.grid(column=0, row = rowIndex, columnspan = 3,padx = 5,pady = 10)
rowIndex += 1
#endregion

#region tabSettings
rowIndex = 0
usernameLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Username")
usernameLabel.grid(column = 0,columnspan = 1,sticky=tk.W, row = rowIndex, padx = 10,pady = 3)
usernameVar = tk.StringVar(root)
usernameEntry = ttk.Entry(tabSettings, width = 15, textvariable = usernameVar)
usernameEntry.grid(column = 1,columnspan = 2, row = rowIndex,padx = 10,pady = 3)

rowIndex += 1
usernameVar.set(data["username"])
passwordLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Password")
passwordLabel.grid(column = 0,columnspan = 1,sticky=tk.W, row = rowIndex, padx = 10,pady = 3)
passwordVar = tk.StringVar(root)
passwordEntry = ttk.Entry(tabSettings, width = 15, textvariable = passwordVar)
passwordEntry.grid(column = 1,columnspan = 2, row = rowIndex,padx = 10,pady = 3)
passwordVar.set(data["password"])

rowIndex += 1
singleRobberySeperator = ttk.Label(tabSettings, justify=tk.LEFT, text="Single Rob. Settings", font = "Verdana 8 bold")
singleRobberySeperator.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
minTimeLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Min Time")
minTimeLabel.grid(column = 1,columnspan = 1, row = rowIndex, padx = 5,pady = 3)
maxTimeLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Max Time")
maxTimeLabel.grid(column = 2,columnspan = 1, row = rowIndex, padx = 5,pady = 3)

rowIndex += 1
openRobberyPageLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Open robbery page")
openRobberyPageLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
openRobberyPageMinVar = tk.StringVar(root)
openRobberyPageMinEntry = ttk.Entry(tabSettings,width = 7, textvariable = openRobberyPageMinVar)
openRobberyPageMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
openRobberyPageMinVar.set(data["robberyPageMin"])
openRobberyPageMaxVar = tk.StringVar(root)
openRobberyPageMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = openRobberyPageMaxVar)
openRobberyPageMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
openRobberyPageMaxVar.set(data["robberyPageMax"])

rowIndex += 1
clickRobLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Click rob button")
clickRobLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
clickRobMinVar = tk.StringVar(root)
clickRobMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = clickRobMinVar)
clickRobMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
clickRobMinVar.set(data["robMin"])
clickRobMaxVar = tk.StringVar(root)
clickRobMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = clickRobMaxVar)
clickRobMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
clickRobMaxVar.set(data["robMax"])

rowIndex += 1
nightlifeLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Open nightlife page")
nightlifeLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
nightlifeMinVar = tk.StringVar(root)
nightlifeMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = nightlifeMinVar)
nightlifeMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
nightlifeMinVar.set(data["nightClubMin"])
nightlifeMaxVar = tk.StringVar(root)
nightlifeMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = nightlifeMaxVar)
nightlifeMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
nightlifeMaxVar.set(data["nightClubMax"])

rowIndex += 1
nightclubLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Enter nightclub page")
nightclubLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
nightclubMinVar = tk.StringVar(root)
nightclubMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = nightclubMinVar)
nightclubMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
nightclubMinVar.set(data["enterClubMin"])
nightclubMaxVar = tk.StringVar(root)
nightclubMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = nightclubMaxVar)
nightclubMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
nightclubMaxVar.set(data["enterClubMax"])

rowIndex += 1
drinkLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Click buy button")
drinkLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
drinkMinVar = tk.StringVar(root)
drinkMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = drinkMinVar)
drinkMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
drinkMinVar.set(data["buyMin"])
drinkMaxVar = tk.StringVar(root)
drinkMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = drinkMaxVar)
drinkMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
drinkMaxVar.set(data["buyMax"])

rowIndex += 1
exitLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Click exit button")
exitLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
exitMinVar = tk.StringVar(root)
exitMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = exitMinVar)
exitMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
exitMinVar.set(data["exitMin"])
exitMaxVar = tk.StringVar(root)
exitMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = exitMaxVar)
exitMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
exitMaxVar.set(data["exitMax"])

rowIndex += 1
gangRobberySeperator = ttk.Label(tabSettings, justify=tk.LEFT, text="Gang Rob. Settings", font = "Verdana 8 bold")
gangRobberySeperator.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)

rowIndex += 1
gangclickRobLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Click gang rob join")
gangclickRobLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row =rowIndex, padx = 10,pady = 3)
gangclickRobMinVar = tk.StringVar(root)
gangclickRobMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = gangclickRobMinVar)
gangclickRobMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
gangclickRobMinVar.set(data["gangRobMin"])
gangclickRobMaxVar = tk.StringVar(root)
gangclickRobMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = gangclickRobMaxVar)
gangclickRobMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
gangclickRobMaxVar.set(data["gangRobMax"])

rowIndex += 1
assultSeperator = ttk.Label(tabSettings, justify=tk.LEFT, text="Assult Settings", font = "Verdana 8 bold")
assultSeperator.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 12,pady = 3)

rowIndex += 1
assultEnterClubLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Re-enter club time")
assultEnterClubLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
assultEnterClubMinVar = tk.StringVar(root)
assultEnterClubMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = assultEnterClubMinVar)
assultEnterClubMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
assultEnterClubMinVar.set(data["attackEnterClubMin"])
assultEnterClubMaxVar = tk.StringVar(root)
assultEnterClubMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = assultEnterClubMaxVar)
assultEnterClubMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
assultEnterClubMaxVar.set(data["attackEnterClubMax"])

rowIndex += 1
assultStayClubLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Stay inside club time")
assultStayClubLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
assultStayClubMinVar = tk.StringVar(root)
assultStayClubMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = assultStayClubMinVar)
assultStayClubMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
assultStayClubMinVar.set(data["attackStayClubMin"])
assultStayClubMaxVar = tk.StringVar(root)
assultStayClubMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = assultStayClubMaxVar)
assultStayClubMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
assultStayClubMaxVar.set(data["attackStayClubMax"])

rowIndex += 1
assultexitLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Run away exit")
assultexitLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
assultExitMinVar = tk.StringVar(root)
assultexitMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = assultExitMinVar)
assultexitMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
assultExitMinVar.set(data["runFromAssultMin"])
assultExitMaxVar = tk.StringVar(root)
assultexitMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = assultExitMaxVar)
assultexitMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
assultExitMaxVar.set(data["runFromAssultMax"])

rowIndex += 1
assultOpenAssultLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Open assult menu")
assultOpenAssultLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
openAssultMinVar = tk.StringVar(root)
openAssultMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = openAssultMinVar)
openAssultMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
openAssultMinVar.set(data["attackOpenMin"])
openAssultMaxVar = tk.StringVar(root)
openAssultMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = openAssultMaxVar)
openAssultMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
openAssultMaxVar.set(data["attackOpenMax"])

rowIndex += 1
assultTypeLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Select assult type")
assultTypeLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
selectAssultMinVar = tk.StringVar(root)
selectAssultMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = selectAssultMinVar)
selectAssultMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
selectAssultMinVar.set(data["attackSingleMin"])
selectAssultMaxVar = tk.StringVar(root)
selectAssultMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = selectAssultMaxVar)
selectAssultMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
selectAssultMaxVar.set(data["attackSingleMax"])

rowIndex += 1
assultDoLabel = ttk.Label(tabSettings, justify=tk.LEFT, text="Do assult")
assultDoLabel.grid(sticky=tk.W,column = 0,columnspan = 1, row = rowIndex, padx = 10,pady = 3)
doAssultMinVar = tk.StringVar(root)
doAssultMinEntry = ttk.Entry(tabSettings, width = 7, textvariable = doAssultMinVar)
doAssultMinEntry.grid(column = 1, row = rowIndex,padx = 5,pady = 3)
doAssultMinVar.set(data["attackDoneMin"])
doAssultMaxVar = tk.StringVar(root)
doAssultMaxEntry = ttk.Entry(tabSettings, width = 7, textvariable = doAssultMaxVar)
doAssultMaxEntry.grid(column = 2, row = rowIndex,padx = 5,pady = 3)
doAssultMaxVar.set(data["attackDoneMax"])

rowIndex += 1
saveSettings = ttk.Button(tabSettings, text = "Save Settings", command = saveSettingsFunc)
saveSettings.grid(column=0, row = rowIndex, columnspan =3,padx = 10,pady = 10)
#endregion
#endregion
    
assult.cacheAttackArrays()
common.getMessageAsync()
common.getAlertMessageAsync()
disableBot()
root.mainloop()
