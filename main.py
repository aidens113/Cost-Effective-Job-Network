import time
import math
import random
import os
import sys
import requests
import threading
from os.path import expanduser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
from datetime import datetime
import time,string,zipfile,os
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import date
import smtplib
from email.message import EmailMessage
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageEnhance 
import keyboard
import discord
from ftplib import FTP 
import fileinput
import asyncio
import logging
from telethon import TelegramClient, events, sync

gmail_user = 'email'
gmail_app_password = 'gmailAppPassword'
    
thesemsgs = []

def press_key(key, driver):
    actions = ActionChains(driver)
    actions.send_keys(key)
    actions.perform()

def randPressKeys(driver,thesekeys):
    for myi in thesekeys:
        press_key(myi,driver)
        time.sleep(random.uniform(0.01, 0.2))
        
def thisKeyDown(driver,key):
    actions = ActionChains(driver)
    actions.key_down(key)
    actions.perform()

def thisKeyUp(driver,key):
    actions = ActionChains(driver)
    actions.key_up(key)
    actions.perform()

def randkeys(element, keys, driver):
    for myi in keys:
        element.send_keys(myi)
        time.sleep(random.uniform(0.05, 0.25))
        
def initdriver(doData):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    if doData == True:
        chrome_options.add_argument("user-data-dir=C:\\Users\\yourUsernameHere\\AppData\\Local\\Google\\Chrome\\User Data\\")
    #chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    driver.set_page_load_timeout(20)
    driver.delete_all_cookies()
    #driver.set_window_position(-10000,0)
    return driver


def getDomain(url):
    try:
        domain = url.split("//")[1]
        try:
            domain = domain.split("/")[0]
        except:
            print("ERR")

        try:
            domain = domain.replace("www.","")
        except:
            print("ERR")
        
        return domain
    except:
        print("ERR")
        return url



client = discord.Client()

        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def sendMsg():
    global thesemsgs
    while True:
        try:
            if len(thesemsgs) >= 1:
                for msg in thesemsgs:
                    await client.wait_until_ready()
                    channel = client.get_channel(id=msg[0])
                    await channel.send(msg[1])
                    
                thesemsgs = []
                                                 
        except Exception as EEEEE:
            print("ERR msg: "+str(EEEEE))

def sendresumes():
    global thesemsgs
    resumes = []
    while True:
        response = requests.get("https://yourdomain/mmbot/incomingApplications.txt",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"})
        allmsgs = str(response.text)
        print(allmsgs)
        firstResumes = allmsgs.split("END")
        for resume in firstResumes:
            try:
                resumes.append(resume.split("START")[1])            
            except Exception as EEee:
                print("ERR"+str(EEee))
        if len(resumes) >= 1:
            for msg in resumes:
                thesemsgs.append([949822226679607336,msg])
            resumes = []
            requests.get("https://yourdomain/mmbot/moderation.php?cmd=deleteOldApplications",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"})
            time.sleep(3)
        time.sleep(60)

def updateJobs():
    while True:
        try:
            jobs = []
            response = requests.get("https://yourdomain/mmbot/directory/",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"})
            allmsgs = str(response.text)
            #print(allmsgs)
            firstJobs = allmsgs.split('<a href=')
            for job in firstJobs:
                if '"/mmbot/directory/jobpost' in str(job):
                    print("found new jobs")
                    jobURL = str("https://yourdomain/mmbot/directory/"+str(job.split('"/mmbot/directory/')[1].split('"')[0])+"\n")
                    jobs.append(jobURL)

            file = open("jobsToPromote.txt","w")
            file.writelines(jobs)
            file.close()
            time.sleep(60)
        except Exception as EEEEE:
            print("ERR updatejobs: "+str(EEEEE))
            time.sleep(60)

def postToTelegram(theList,secondsToWait):
    while True:
        try:
            api_id = int(appidhere)
            api_hash = 'hashhere'

            client = TelegramClient('anon', api_id, api_hash)
            client.start()

            file = open("ad.txt","r")
            theAD = file.read()
            file.close()

            file = open(str("tgnetwork/"+theList),"r")
            allLinks = file.readlines()
            file.close()

            for link in allLinks:
                try:
                    client.send_message(link, theAD)
                    time.sleep(random.uniform(4.0,10.0))
                except Exception as ERrr:
                    print("ERR sending msg: "+str(ERrr))
            time.sleep(secondsToWait)
            if secondsToWait == 0:
                return
        except Exception as EEEEE:
            print("ERR: "+str(EEEEE))
            time.sleep(secondsToWait)
            if secondsToWait == 0:
                return
        
def promoteIncomingJobs():
    while True:
        try:
            file = open("jobsToPromote.txt","r")
            allJobs = file.readlines()
            file.close()

            if len(allJobs) >= 1:
                for job in allJobs:
                    response = requests.get(str(job.strip().replace("\n","").replace("\r","")),headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"})
                    file = open("jobpostad.txt","r")
                    theText = file.read()
                    file.close()
                    theAD = theText.replace("*TITLE*",response.text.split("<title>")[1].split("</title>")[0]).replace("*LINK*",job.strip().replace("\n","").replace("\r",""))
                    print(theAD)
                    postToTelegram(theAD)

                    time.sleep(random.uniform(300.0,600.0))
            
        except Exception as EEEEE:
            print("ERR"+str(EEEEE))


def sendDiscordMsg(theList,secondsToWait):
    while True:
        try:
            file = open("ad.txt","r")
            theAD = file.read()
            file.close()

            file = open(str("discordnetwork/"+theList),"r")
            allServers = file.readlines()
            file.close()

            print(allServers)

            driver = initdriver(True)

            for theServer in allServers:
                print(theServer)
                for _ in range(2):
                    try:
                        driver.get(theServer.strip().replace("\n","").replace("\r",""))
                        break
                    except Exception as EEee:
                        print("ERR"+str(EEee))

                time.sleep(random.randint(15.0,25.0))

                for msg in theAD.split("\n"):
                    if len(msg) >= 3:
                        randPressKeys(driver,msg)
                    thisKeyDown(driver,Keys.SHIFT)
                    press_key(Keys.ENTER,driver)
                    thisKeyUp(driver,Keys.SHIFT)
                time.sleep(3)
                
                press_key(Keys.ENTER, driver)

                time.sleep(random.randint(5.0,20.0))

            try:
                driver.close()
                driver.quit()
            except Exception as EEee:
                print("ERR closing driver"+str(EEee))
            if secondsToWait == 0:
                return
            time.sleep(secondsToWait)
        except Exception as EEEEE:
            print("ERR send discord"+str(EEEEE))
            time.sleep(secondsToWait)
            if secondsToWait == 0:
                return
            
promoteincomingthread = threading.Thread(target=promoteIncomingJobs)
promoteincomingthread.start()

jobupdatethread = threading.Thread(target=updateJobs)
jobupdatethread.start()

sendresumethread = threading.Thread(target=sendresumes)
sendresumethread.start()

print("WELCOME TO THE AIO PRIVATE AD NETWORK")
print("REMINDER: Before sending a command, have you configured ad.txt?")
print("----------------------------------------------------------------")
print("AVAILABLE NICHE FILES")
for thisItem in os.listdir("discordnetwork/"):
    print("-"+str(thisItem))
print("----------------------------------------------------------------")
print("COMMANDS")
print("broadcast exampleList.txt")
print("abroadcast exampleList.txt secondsToWait (automatically broadcast message every x seconds)")
print("----------------------------------------------------------------")
cmd = input("$ ")
if "broadcast" in cmd:
    #sendDiscordMsg(str(cmd.split(" ")[1].strip()),0)
    postToTelegram(str(cmd.split(" ")[1].strip()),0)
if "abroadcast" in cmd:
    #sendDiscordMsg(str(cmd.split(" ")[1].strip()),int(str(cmd.split(" ")[2].strip())))
    postToTelegram(str(cmd.split(" ")[1].strip()),int(str(cmd.split(" ")[2].strip())))
client.loop.create_task(sendMsg())
client.run('DiscordBotTokenHere')


