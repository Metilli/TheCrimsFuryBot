#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import random
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import CommonFunctionsModule as common
import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk

driver = None
data = None

def waitUntilExitClub(maxTime):
    startTime = time.time()
    while time.time()-startTime < maxTime:
        time.sleep(0.05)
        try:
            exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
        except:
            return True
            
    else:
        return False

def waitUntilEnterClub():
    startTime = time.time()
    while time.time()-startTime < 4:
        if "nightclub" in driver.current_url:
            return True
    else:
        return False


stopRobbery = False
isRobberyDone = True
isCheckUserDie = False
isDead = False
def startRobbery(robberyCount):
    global isRobberyDone
    global stopRobbery
    isRobberyDone = False
    stopRobbery = False
    totalMoneyAtStart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='content_right']//*[contains(text(),'$')]"))).text
    i = 0
    totalFail = 0
    startRobberyTime = time.time()
    isSomeFails = True
    failedRobberyCount = 0
    totalRobberySuccessful = 0
    while isSomeFails:
        isSomeFails = False
        while i < robberyCount:
            if common.getTicketCount() == 0:
                stopRobbery = True
            global isCheckUserDie
            if stopRobbery:
                i = robberyCount
                failedRobberyCount = 0
                isSomeFails = False
                break
            if isCheckUserDie:
                common.checkUserDie(False)
                isCheckUserDie = False
            global isDead
            if isDead:
                leftContents =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@id,'content_left')]//li")))
                if len(leftContents) < 2:
                    stopRobbery = True
                    continue
            i += 1
            tinRound = time.time()
            try:
                checkAddictionAndStamina()
                makeSingleRobbery()
                common.Print("Info: This robbery successful."+ str(i))
                common.Print("Info: Time elapsed: " + str(round(time.time() - tinRound,2))+" ms")  # CPU seconds elapsed (floating point)
                totalRobberySuccessful += 1
            except:
                failedRobberyCount += 1
                common.Print("Info: This robbery failed."+ str(i))
                common.Print("Info: Time elapsed: "+ str(round(time.time() - tinRound,2))+" ms")  # CPU seconds elapsed (floating point)
        else:
            if failedRobberyCount > 0:
                robberyCount = failedRobberyCount
                failedRobberyCount = 0
                totalFail += 1
                i = 0
                isSomeFails = True
                common.Print("Info: Some robberies was unsuccesfull. This time robbery will be done again: "+ str(robberyCount))
                if totalFail > 3:
                    stopRobbery = True
    else:
        common.Print("Info: Total robbery time: " + str(round(time.time() - startRobberyTime,1)/60)+ " min")  # CPU seconds elapsed (floating point)
        totalMoney = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content_right']//*[contains(text(),'$')]"))).text
        common.Print("Info: Total money at start: "+ str(totalMoneyAtStart))
        common.Print("Info: Total money at end: "+ str(totalMoney))
        stopRobbery = True
        isRobberyDone = True
        global totalPrizes
        if len(totalPrizes) > 1:
            common.Print("Info: Total prizes:")
            i = 0
            for item in totalPrizes:
                if i > 0:
                    common.Print(str(totalPrizes[item]) + " " + str(item))   
                i += 1

def checkAddictionAndStamina():
    if common.addictionRatio() > random.uniform(20, 50):
        common.makeDetox()
    if common.staminaRatio() < 50:
        fillStamina()

totalPrizes = dict.fromkeys(range(1))
def makeSingleRobbery():
    global totalPrizes
    time.sleep(random.uniform(data["robberyPageMin"],data["robberyPageMax"]))
    robberyMenu = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-robbery')]")))
    common.click(robberyMenu)
    
    try:
        time.sleep(random.uniform(data["robMin"],data["robMax"]))
        robBustard = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'singlerobbery-rob')]")))
        common.click(robBustard)
    except:#It means you get out hospital and can't find button. So refresh it to find it.
        time.sleep(random.uniform(0.5,1))
        driver.refresh()
        time.sleep(random.uniform(data["robMin"],data["robMax"]))
        robBustard = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'singlerobbery-rob')]")))
        common.click(robBustard)

    isCompleteRobbery = False
    try:
        isSuccesful = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'alert-success')]")))
        if "received" in isSuccesful.text:
            isCompleteRobbery = True
            reportArr = isSuccesful.text.split("received")
            reportDetails = reportArr[1].replace(":","")
            reportDetailsArr = reportDetails.split("\n")
            i = 0
            for prize in reportDetailsArr:
                i += 1
                if i > 1:
                    lineArr = prize.split(" ")
                    prizeCount = lineArr[0]
                    prizeNameArr = lineArr[1:]
                    prizeName = ""
                    for item in prizeNameArr:
                        prizeName += item
                    common.Print("Extra prize: " + str(prizeCount) + " " + prizeName)
                    if prizeName in totalPrizes:
                        totalPrizes[prizeName] += int(prizeCount)
                    else:
                        totalPrizes[prizeName] = int(prizeCount)
    except:
        isCompleteRobbery = False

    return isCompleteRobbery

def fillStamina():
    time.sleep(random.uniform(data["nightClubMin"],data["nightClubMax"]))
    nightLife = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-nightlife')]")))
    common.click(nightLife)
    
    try:
        time.sleep(random.uniform(data["enterClubMin"],data["enterClubMax"]))
        enterClub = WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Enter')]")))
        common.click(enterClub[0])
        waitUntilEnterClub(random.uniform(1,3))
        tinsideClub = time.time()
    except:
        time.sleep(random.uniform(0.5,1)) #It means you get out hospital and can't find any club. So refresh it and find clubs.
        driver.refresh()
        time.sleep(random.uniform(data["enterClubMin"],data["enterClubMax"]))
        enterClub = WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Enter')]")))
        common.click(enterClub[0])
        waitUntilEnterClub(random.uniform(1,3))
        tinsideClub = time.time()

    time.sleep(random.uniform(data["buyMin"],data["buyMax"]))
    buy = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Buy')]")))
    common.click(buy)

    time.sleep(random.uniform(data["exitMin"],data["exitMax"]))
    exitClub = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'exit-button')]")))
    common.click(exitClub)
    common.Print("Info: Time for filling stamina inside club: " + str(time.time() - tinsideClub))
    isOutOfNightclub = False
    while not isOutOfNightclub:
        time.sleep(0.01)
        if "nightclub" not in driver.current_url:
            isOutOfNightclub = True
            time.sleep(0.3)
    if common.staminaRatio() == 100:
        return True
    else:
        return False

def waitUntilEnterClub(maxTime):
    startTime = time.time()
    while time.time()-startTime < maxTime:
        if "nightclub" in driver.current_url:
            return True
    else:
        return False
