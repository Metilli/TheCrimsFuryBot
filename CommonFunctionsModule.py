#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import random
import time
import winreg
import threading
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pynput.mouse import Button, Controller
from pynput import keyboard
import SingleRobberyModule as singleRob
import GangRobberyModule as gangRob
import AssultModule as assult
import logging
import urllib3


#Example MouseSensitivity
#Read value 
#logging.info (get_reg('MouseSensitivity'))

#Set Value 1/20 (will just write the value to reg, the changed mouse val requires a win re-log to apply*)
#set_reg('MouseSensitivity', str(10))

driver = None
data = None
browser_navigation_panel_height = None
botMode = 0
'''
def on_press(key):
  a = 1

def on_release(key):
  if key == keyboard.Key.esc:
    stopBot()
'''
    
def Print(message):
    print(message)
    logging.info(message)

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.dirname(__file__)
  return os.path.join(base_path, relative_path)


def clickAssult(button,step):
    global assultStep
    assultStep = step
    click(button)

assultStep = 0
openAssultMenuxOffset = 0.0
selectAssultOffset = 0.0
doAssultOffset = 0.0
def click(button):
    global assultStep
    global openAssultMenuxOffset
    global selectAssultOffset
    global doAssultOffset
    yOffset = random.uniform(0, button.size["height"])
    xOffset = random.uniform(0, button.size["width"])
    if assultStep == 1:
        openAssultMenuxOffset = xOffset
    elif assultStep == 2:
        selectAssultOffset = random.uniform(0,openAssultMenuxOffset)
        xOffset = selectAssultOffset
    elif assultStep == 3:
        doAssultOffset = random.uniform(0,selectAssultOffset)
        xOffset = doAssultOffset
    assultStep = 0
    mouse.position = (button.location["x"] + button.size["width"]*0.1 + xOffset * 0.8,button.location["y"]+button.size["height"]*0.1+browser_navigation_panel_height + yOffset * 0.8)
    mouse.press(Button.left)
    mouse.release(Button.left)

def login(username,password):
    try:
        time.sleep(random.uniform(0.4,1))
        usernameEntry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Username']")))
        usernameEntry.send_keys(username)
        time.sleep(random.uniform(0.4,1))
        passwordEntry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Password']")))
        passwordEntry.send_keys(password)

        time.sleep(random.uniform(0.4,1))
        enterButton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div/div/div[2]/div[1]/form/button")))
        click(enterButton)
    except:
        Print("Info: Can't login automatically")

def staminaRatio():
    try:
        stamina = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_right']/div/*//div[contains(text(),'%')]")))
        return int(stamina[0].text.split(':')[1][:-1])
    except:
        Print("Error: Can't read stamina ratio")

def addictionRatio():
  try:
    addiction = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_right']/div/*//div[contains(text(),'%')]")))
    return int(addiction[1].text.split(':')[1][:-1])
  except:
    Print("Error: Can't read addiction ratio")

def makeDetox():
    try:
        time.sleep(random.uniform(data["hospitalMin"],data["hospitalMax"]))
        hospital = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-hospital')]")))
        click(hospital)

        time.sleep(random.uniform(data["detoxMin"],data["detoxMax"]))
        detox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Detoxicate for cash')]")))
        click(detox)
    except selenium.common.exceptions.TimeoutException as ex:
        Print("Making detox was failed.")
        
def getTicketCount():
    try:
        ticketCount = WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Tickets')]//span"))).text
        return int(ticketCount)
    except:
        common.Print("Error: Can't check ticket count")
        return 1

def getCurrentStats():
    try:
        allStats = driver.find_elements(By.XPATH,"//*[@id='content_right']//*[contains(@class,'user_profile_stats')]//span[@class='menuyellowtext']")
        i = 0
        statsText = "Info: "
        for item in allStats:
            if item.text != "":
                if i == 0:
                    statsText += " Intelligence: "
                elif i == 1:
                    statsText += " Charisma: "
                elif i == 2:
                    statsText += " Strength: "
                elif i == 3:
                    statsText += " Tolerance: "
                statsText += item.text
                i += 1
        Print(statsText)
        allPowers = driver.find_elements(By.XPATH,"//*[@id='content_right']//a[contains(@href,'power-information')]//span[@class='menuyellowtext']")
        i = 0
        powerText = "Info: "
        for item in allPowers:
            if item.text != "":
                if i == 0:
                    powerText += "Single Robbery Power: "
                elif i == 1:
                    powerText += " Gang Robbery Power: "
                elif i == 2:
                    powerText += " Assult Power: "
                powerText += item.text
                i += 1
        Print(powerText)
    except NoSuchElementException as nse:
        print(nse)
        print("-----")
        print(str(nse))
        print("-----")
        print(nse.args)
        print("=====")
        Print("Error: Can't read user stats.")

def getAlertMessageAsync():
    t = threading.Thread(target=getAlertMessagesThread)
    t.start()

def getAlertMessagesThread():
    global driver
    while True:
        try:
            # Wait for the alert to be displayed and store it in a variable
            WebDriverWait(driver,1).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except Exception as e:
            a=1

def getMessageAsync():
    messageThread = threading.Thread(target=getMessageThread)
    messageThread.start()
          
isNeedToCheckIfUserDie = False
def getMessageThread():
    global stopRobberyThread
    global isNeedToCheckIfUserDie
    global isAssultStop
    recievedMessages = []
    messageInfoArr = None
    while True:
        try:
            messageArr = None
            messageInfoLive = WebDriverWait(driver,  60).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//*//div[contains(@class,'message-content')]")))
            if messageInfoArr != messageInfoLive:
                messageInfoArr = messageInfoLive
                messageArr = messageInfoArr
                for message in messageArr:
                    Print(message.text)
                    if "decreased" in message.text:
                        recievedMessages.append(message.text)
                        assult.isDeadCheck = True
                        singleRob.isCheckUserDie = True
                        gangRob.isCheckUserDie = True
                    elif "increased" in message.text:
                        recievedMessages.append(message.text)
                    elif "planl" in message.text:
                        #assult.assultWithTrustedAccount()
                        recievedMessages.append(message.text)
                        assult.isAssultStop = True
                    else:
                        recievedMessages.append(message.text)
        except Exception as e:
            #Print("Get message exception: " + str(e))
            a = 1

def checkUserDie(isPrisonCheck):
    global assultisUseCreditHospital
    global assultisUsePrivateCareHospital
    global assultisUseCreditPrison
    global assultisUseFreeCardPrison
    global assultisUseBribePrison
    global singleRobisUseCreditHospital
    global singleRobisUsePrivateCareHospital
    global gangRobisUseCreditHospital
    global gangRobisUsePrivateCareHospital
    global botMode
    time.sleep(random.uniform(0.5,1.5))
    if not isPrisonCheck:
        driver.refresh()
    leftContents =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@id,'content_left')]//li")))
    if len(leftContents) == 1:
        Print("Info: User in hospital")
        if botMode == 1:
            getOutHospital(singleRobisUseCreditHospital,singleRobisUsePrivateCareHospital)
            singleRob.isDead = True
            gangRob.isDead = True
            assult.isDead = True
        elif botMode == 2:
            getOutHospital(gangRobisUseCreditHospital,gangRobisUsePrivateCareHospital)
            singleRob.isDead = True
            gangRob.isDead = True
            assult.isDead = True
        elif botMode == 3:
            getOutHospital(assultisUseCreditHospital,assultisUsePrivateCareHospital)
            singleRob.isDead = True
            gangRob.isDead = True
            assult.isDead = True
    elif len(leftContents) == 2:
        Print("Info: User in prison")
        getOutPrison(assultisUseCreditPrison,assultisUseFreeCardPrison,assultisUseBribePrison)
        singleRob.isDead = True
        gangRob.isDead = True
        assult.isDead = True
    else:
        Print("Info: User is alive")

assultisUseCreditHospital = False
assultisUsePrivateCareHospital = False
assultisUseCreditPrison = False
assultisUseFreeCardPrison = False
assultisUseBribePrison = False
singleRobisUseCreditHospital = False
singleRobisUsePrivateCareHospital = False
gangRobisUseCreditHospital = False
gangRobisUsePrivateCareHospital = False
def getOutHospital(isCredit,isFreeCard):
    time.sleep(random.uniform(1,3))
    hospital = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-hospital')]")))
    click(hospital)
    credits = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='content_right']//*[contains(text(),'Credits:')]"))).text
    creditAmount = int(credits[8:])
    if isFreeCard:
        time.sleep(random.uniform(1,2))
        try:
            getOut = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH,"//*[@id='content_middle']//button[contains(text(),'Activate')]")))
            click(getOut[0])
            Print("Info: Used private care to leave hospital")
        except:
            Print("Info: Get out with private care is failed. Bot stopped.")
            getCurrentStats()
            singleRob.stopRobbery = True
            gangRob.stopRobbery = True
            assult.isAssultStop = True
    elif isCredit:
        if creditAmount >= 10:
            time.sleep(random.uniform(1,2))
            getOut = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH,"//*[@id='content_middle']//button[contains(text(),'buy private care')]")))
            click(getOut[0])
            Print("Info: Used credit to leave hospital")
            WebDriverWait(driver,5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            time.sleep(random.uniform(1,2))
            alert.accept()
        else:
            Print("Info: Your credit is not enoght to get out hospital.")
            Print("Info: Bot stopped.")
            getCurrentStats()
            singleRob.stopRobbery = True
            gangRob.stopRobbery = True
            assult.isAssultStop = True
    else:
        getCurrentStats()
        singleRob.stopRobbery = True
        gangRob.stopRobbery = True
        assult.isAssultStop = True
        
def getOutPrison(isCredit,isFreeCard,isMoney):
    time.sleep(random.uniform(1,3))
    prison = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-prison')]")))
    click(prison)
    credits = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='content_right']//*[contains(text(),'Credits:')]"))).text
    creditAmount = int(credits[8:])
    if isMoney:
        payBribe =  WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Bribe')]")))
        time.sleep(random.uniform(1,2))
        click(payBribe[0])
        Print("Info: Used bribe to leave prison")
        time.sleep(random.uniform(data["nightClubMin"],data["nightClubMax"]))
        nightLife = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-nightlife')]")))
        click(nightLife)
    elif isFreeCard:
        try:
            time.sleep(random.uniform(1,2))
            getOut = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Activate')]")))
            click(getOut[0])
            Print("Info: Used free card to leave prison") 
        except:
            Print("Info: Get out with private care is failed. Bot stopped.")
            getCurrentStats()
            singleRob.stopRobbery = True
            gangRob.stopRobbery = True
            assult.isAssultStop = True
    elif isCredit:
        if creditAmount >= 20:
            time.sleep(random.uniform(1,2))
            getOut = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Run')]")))
            click(getOut[0])
            WebDriverWait(driver,5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            time.sleep(random.uniform(1,2))
            alert.accept()
        else:
            Print("Info: Your credit is not enoght to get out prison.")
            Print("Info: Bot stopped.")
            getCurrentStats()
            singleRob.stopRobbery = True
            gangRob.stopRobbery = True
            assult.isAssultStop = True
    else:
        getCurrentStats()
        singleRob.stopRobbery = True
        gangRob.stopRobbery = True
        assult.isAssultStop = True

mouse = Controller()
'''
listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()
'''
logging.basicConfig(filename=resource_path('./profile/log.txt'), level=logging.INFO)

logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("urllib3").propagate = False
http = urllib3.PoolManager(num_pools=50)
