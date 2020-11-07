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

driver = None
data = None

def fillStamina():
    time.sleep(random.uniform(data["enterClubMin"],data["enterClubMax"]))
    enterClub = WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Enter')]")))
    common.click(enterClub[0])
    waitUntilEnterClub(3)
    tinsideClub = time.time()

    time.sleep(random.uniform(data["buyMin"],data["buyMax"]))
    buy = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content_middle']/div/div[3]/table[2]/tbody/tr/td[4]/button")))
    common.click(buy)

    time.sleep(random.uniform(data["exitMin"],data["exitMax"]))
    exitClub = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'exit-button')]")))
    common.click(exitClub)
    isOutOfNightclub = False
    while not isOutOfNightclub:
        time.sleep(0.05)
        if "nightclub" not in driver.current_url:
            common.Print("Info: Time for filling stamina inside club: "+str(time.time() - tinsideClub))
            isOutOfNightclub = True
            time.sleep(0.3)
    if common.staminaRatio() == 100:
        return True
    else:
        return False

def waitUntilExitClub(maxTime):
    startTime = time.time()
    while time.time()-startTime < maxTime:
        time.sleep(0.01)
        try:
            exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
        except:
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

hitmanAttackArray = []
businessmanAttackArray = []
pimpAttackArray = []
robberAttackArray = []
dealerAttackArray = []
brokerAttackArray = []
isAttackGangsterBool = False
def cacheAttackArrays():
    global hitmanAttackArray
    global businessmanAttackArray
    global pimpAttackArray
    global robberAttackArray
    global dealerAttackArray
    global brokerAttackArray
    global isAttackGangsterBool

    if data["isAttack"]["Gangster"] == 1:
        isAttackGangsterBool = True

    min = int(data["attackLevels"]["HitmanLevel"].split(",")[0])-1
    max = int(data["attackLevels"]["HitmanLevel"].split(",")[1])
    allRoles = data["hitmanRoles"].split(",")
    hitmanAttackArray = allRoles[min:max]
    
    min = int(data["attackLevels"]["BusinessmanLevel"].split(",")[0])-1
    max = int(data["attackLevels"]["BusinessmanLevel"].split(",")[1])
    allRoles = data["businessmanRoles"].split(",")
    businessmanAttackArray = allRoles[min:max]
    
    min = int(data["attackLevels"]["PimpLevel"].split(",")[0])-1
    max = int(data["attackLevels"]["PimpLevel"].split(",")[1])
    allRoles = data["pimpRoles"].split(",")
    pimpAttackArray = allRoles[min:max]
    
    min = int(data["attackLevels"]["RobberLevel"].split(",")[0])-1
    max = int(data["attackLevels"]["RobberLevel"].split(",")[1])
    allRoles = data["robberRoles"].split(",")
    robberAttackArray = allRoles[min:max]
    
    min = int(data["attackLevels"]["DealerLevel"].split(",")[0])-1
    max = int(data["attackLevels"]["DealerLevel"].split(",")[1])
    allRoles = data["dealerRoles"].split(",")
    dealerAttackArray = allRoles[min:max]
    
    min = int(data["attackLevels"]["BrokerLevel"].split(",")[0])-1
    max = int(data["attackLevels"]["BrokerLevel"].split(",")[1])
    allRoles = data["brokerRoles"].split(",")
    brokerAttackArray = allRoles[min:max]

def isSkipEnemy(role,enemyLevel):
    global hitmanAttackArray
    global businessmanAttackArray
    global pimpAttackArray
    global robberAttackArray
    global dealerAttackArray
    global brokerAttackArray
    skipTarget = True
    if data["hitmanName"] in role:
        if data["isAttack"]["Hitman"] == 1:
            for attackRole in hitmanAttackArray:
                if attackRole in enemyLevel:
                    skipTarget = False
                    break
    elif data["businessmanName"] in role:
        if data["isAttack"]["Businessman"] == 1:
            for attackRole in businessmanAttackArray:
                if attackRole in enemyLevel:
                    skipTarget = False
                    break
    elif data["pimpName"] in role:
        if data["isAttack"]["Pimp"] == 1:
            for attackRole in pimpAttackArray:
                if attackRole in enemyLevel:
                    skipTarget = False
                    break
    elif data["robberName"] in role:
       if data["isAttack"]["Robber"] == 1:
            for attackRole in robberAttackArray:
                if attackRole in enemyLevel:
                    skipTarget = False
                    break
    elif data["dealerName"] in role:
       if data["isAttack"]["Dealer"] == 1:
            for attackRole in dealerAttackArray:
                if attackRole in enemyLevel:
                    skipTarget = False
                    break
    elif data["brokerName"] in role:
        if data["isAttack"]["Broker"] == 1:
            for attackRole in brokerAttackArray:
                if attackRole in enemyLevel:
                    skipTarget = False
                    break
    elif data["gangsterName"] in role:
        if data["isAttack"]["Gangster"] == 1:
            skipTarget = False
    return skipTarget


isAssultStop = False
isAssultDone = True
isDeadCheck = False
isDead = False
def assult(isGangAssult):
    isAssultStopLocal = False
    global isAssultDone
    isAssultDone = False
    isTriedAttack = False
    isRunFromAssult = False
    exitLocationY = {"x":1,"y":2}
    while not isAssultStopLocal:
        global isDeadCheck
        global isAssultStop
        i = 0
        while not waitUntilExitClub(random.uniform(0.35,0.5)) and i < 1:
            try:
                i += 1
                exitt = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                if exitLocationY["y"] != exitClub.location["y"] or exitLocation["x"] != exitClub.location["x"]:
                    common.click(exitt)
            except:
                a = 1
        isAssultStopLocal = isAssultStop
        if common.getTicketCount() == 0:
            isAssultStop = True
        if isAssultStopLocal:
            common.Print("Info: Assult stopped.")
            break
        try:
            if not "nightlife" in driver.current_url:
                time.sleep(random.uniform(data["nightClubMin"],data["nightClubMax"]))
                nightLife = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'menu-nightlife')]")))
                common.click(nightLife)
            global isDead
            if isDead:
                try:
                    leftContents =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@id,'content_left')]//li")))
                    if len(leftContents) < 2:
                        isAssultStop = True
                        continue
                    enterClub = WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Enter')]")))
                    if len(enterClub) >= 7:
                        isDead = False
                    else:
                        time.sleep(random.uniform(0.7,1.25))
                        driver.refresh()
                        continue
                except:
                    time.sleep(random.uniform(0.7,2))
                    driver.refresh()
                    continue
        except:
            common.Print("Can not click nightlife tab.")
        try:#Hapis varsa burada kontrol et
            leftContents =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@id,'content_left')]//li")))
            if len(leftContents) == 1:
                common.Print("Info: User in hospital")
                common.checkUserDie(False)
                continue
            elif len(leftContents) == 2:
                common.Print("Info: User in prison")
                isDeadCheck = False
                common.checkUserDie(True)
                continue
        except:
            a = 1
        try:
            if isDeadCheck:#Hastane ise burada kontrol et
                common.Print("Info: Check if dead ")
                common.checkUserDie(False)
                isDeadCheck = False
                continue
        except Exception as e:
            common.Print("Info: Error try to check user die in assult." + str(e))
        clubExitMin = data["attackStayClubMin"] 
        clubExitMax = data["attackStayClubMax"] 
        try:
            if common.staminaRatio() < 49:
                time.sleep(random.uniform(data["attackEnterClubMin"],data["attackEnterClubMax"]))#Delay to enter club
                common.Print("Info: Need to fill stamina. Current stamina: " + str(common.staminaRatio()))
                if not fillStamina():
                    time.sleep(random.uniform(data["attackEnterClubMin"],data["attackEnterClubMax"]))#Delay to enter club
                    common.Print("Info: Fill stamina failed. Bot will try again to fill stamina. Current stamina: " + str(common.staminaRatio()))
                    if not fillStamina():
                        time.sleep(random.uniform(data["attackEnterClubMin"],data["attackEnterClubMax"]))#Delay to enter club
                        common.Print("Info: Fill stamina failed. Do it manually. Current stamina: " + str(common.staminaRatio()))
                else:
                    common.Print("Info: Stamina full. Current stamina: " + str(common.staminaRatio()))
            if common.addictionRatio() > random.uniform(30,50):
                common.Print("Info: Need to reduce addiction. Current addiction: " + str(common.addictionRatio()) )
                common.makeDetox()
                time.sleep(random.uniform(data["nightClubMin"],data["nightClubMax"]))
                nightLife = driver.find_element(By.XPATH, "//*[contains(@id,'menu-nightlife')]")
                common.click(nightLife)
            time.sleep(random.uniform(data["attackEnterClubMin"],data["attackEnterClubMax"]))#Delay to enter club
            enterClub = WebDriverWait(driver, 8).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']//button[contains(text(),'Enter')]")))
            if len(enterClub) > 6:
                clubIndex = random.randint(int(len(enterClub))-8, int(len(enterClub))-1)
            else:
                driver.refresh()
                continue
            common.click(enterClub[clubIndex])
            waitUntilEnterClub(random.uniform(1,3))
            tFirstInside = time.time()
            common.Print("Info: Entered to night club.")
        except:
            time.sleep(1)
        try:
            visitor = WebDriverWait(driver, random.uniform(clubExitMin/2,clubExitMax/2)).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class,'visitor-')]")))
            tin = time.time()
            if len(visitor) > 1:
                if time.time() - tFirstInside < 0.10:
                    time.sleep(random.uniform(data["runFromAssultMin"]+0.05,data["runFromAssultMax"]+0.08))
                    common.Print("Extra time to leave")
                else:
                    time.sleep(random.uniform(data["runFromAssultMin"],data["runFromAssultMax"]))
                exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                exitLocationY = exitClub.location
                common.click(exitClub)
                common.Print("Info: There are more than one enemy inside club. Run..")
                common.Print("Info: Exit from night club. time: " + "{:.2f}".format((time.time()-tin)))
            '''
            if isAssultStopLocal:
                isAssultStop = True
                try:
                    exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                    common.click(exitClub)
                    waitUntilExitClub(7)
                    common.Print("Info: Assult stopped.")
                except:
                    common.Print("Info: Assult stopped.")
                break
            '''
            username = visitor[0].text.split("\n")[0]
            role = visitor[0].text.split("\n")[1]
            enemyLevel = visitor[0].text.split("\n")[2]
            common.Print("Info: Username: " + username+ " Role: "+role+" subRole: "+enemyLevel)
            skipTarget = isSkipEnemy(role,enemyLevel)
            if skipTarget:
                if time.time() - tFirstInside < 0.10:
                    time.sleep(random.uniform(data["runFromAssultMin"]+0.05,data["runFromAssultMax"]+0.08))
                    common.Print("Extra time to leave")
                else:
                    time.sleep(random.uniform(data["runFromAssultMin"],data["runFromAssultMax"]))
                exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                exitLocationY = exitClub.location
                common.click(exitClub)
                common.Print("Info: Run from enemy. Escape time: " + "{:.2f}".format((time.time()-tin)) + " ms")
                isRunFromAssult = True
            else:
                common.Print("Info: Attack is started to "+ username)
                tAttackStart = time.time()
                time.sleep(random.uniform(data["attackOpenMin"],data["attackOpenMax"]))
                attack1 = driver.find_element(By.XPATH, "//button[contains(@id,'nightclub-singleassault-select-open')]")
                common.clickAssult(attack1,1)
         
                time.sleep(random.uniform(data["attackSingleMin"],data["attackSingleMax"]))
                if not isGangAssult:
                    attack2 = driver.find_element(By.XPATH, "//a[contains(@id,'nightclub-select-assault-type-single')]")
                    common.clickAssult(attack2,2)
                else:
                    attack2 = driver.find_element(By.XPATH, "//a[contains(@id,'nightclub-select-assault-type-gang')]")
                    common.clickAssult(attack2,2)

                time.sleep(random.uniform(data["attackDoneMin"],data["attackDoneMax"]))
                attack3 = driver.find_element(By.XPATH, "//button[contains(@id,'nightclub-attack')]")
                common.clickAssult(attack3,3)
                common.Print("Info: Attack is successful to " + username + ". Attack time: " + "{:.2f}".format((time.time()-tAttackStart)))
                #isTriedAttack = True
        except Exception as e:
            '''
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            common.Print(exc_type, fname, exc_tb.tb_lineno)'''
            try:
                '''
                if isAssultStopLocal:
                    isAssultStop = True
                    common.Print("Info: Assult stopped.")
                    exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                    common.click(exitClub)
                    break
                '''
                if "nightclub" in driver.current_url:
                    visitor = WebDriverWait(driver, random.uniform(clubExitMin/2,clubExitMax/2)).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class,'visitor-')]")))
                    tin = time.time()
                    '''
                    if isAssultStopLocal:
                        isAssultStop = True
                        common.Print("Info: Assult stopped.")
                        exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                        exitLocationY = exitClub.location
                        common.click(exitClub)
                        break
                    '''
                    if len(visitor) > 1:
                        time.sleep(random.uniform(data["runFromAssultMin"],data["runFromAssultMax"]))
                        exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                        common.click(exitClub)
                        common.Print("Info: There are more than one enemy inside club. Run..")
                        common.Print("Info: Exit from night club. time: " + "{:.2f}".format((time.time()-tin)))
                    username = visitor[0].text.split("\n")[0]
                    role = visitor[0].text.split("\n")[1]
                    enemyLevel = visitor[0].text.split("\n")[2]
                    common.Print("Info: Username: " + username+ " Role: "+role+" subRole: "+enemyLevel)

                    skipTarget = isSkipEnemy(role,enemyLevel)
                    if skipTarget:
                        time.sleep(random.uniform(data["runFromAssultMin"],data["runFromAssultMax"]))
                        exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                        exitLocationY = exitClub.location
                        common.click(exitClub)
                        common.Print("Info: Run from enemy. Escape time: " + "{:.2f}".format((time.time()-tin)) + " ms")
                        isRunFromAssult = True
                    else:
                        common.Print("Info: Attack is started to "+ username)
                        tAttackStart = time.time()
                        time.sleep(random.uniform(data["attackOpenMin"],data["attackOpenMax"]))
                        attack1 = driver.find_element(By.XPATH, "//button[contains(@id,'nightclub-singleassault-select-open')]")
                        common.clickAssult(attack1,1)
         
                        time.sleep(random.uniform(data["attackSingleMin"],data["attackSingleMax"]))
                        if not isGangAssult:
                            attack2 = driver.find_element(By.XPATH, "//a[contains(@id,'nightclub-select-assault-type-single')]")
                            common.clickAssult(attack2,2)
                        else:
                            attack2 = driver.find_element(By.XPATH, "//a[contains(@id,'nightclub-select-assault-type-gang')]")
                            common.clickAssult(attack2,2)

                        time.sleep(random.uniform(data["attackDoneMin"],data["attackDoneMax"]))
                        attack3 = driver.find_element(By.XPATH, "//button[contains(@id,'nightclub-attack')]")
                        common.clickAssult(attack3,3)
                        common.Print("Info: Attack is successful to " + username + ". Attack time: " + "{:.2f}".format((time.time()-tAttackStart)))
                        #isTriedAttack = True
            except Exception as e:
                try:
                    if "nightclub" in driver.current_url:
                        time.sleep(random.uniform(data["runFromAssultMin"],data["runFromAssultMax"]*1.2))
                        exitClub = driver.find_element(By.XPATH, "//button[contains(@id,'exit-button')]")
                        exitLocationY = exitClub.location
                        common.click(exitClub)
                        common.Print("Info: Exit from night club.")
                except:
                    a=1

    isAssultDone = True

def assultWithTrustedAccount():
    menu =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='menu-user']")))
    trustedLink =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='app']//a[contains(href,'trusted')]")))
    enter =  WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='content_middle']/div/div[3]/table/tbody/tr/td[2]/form/input[2]")))
