# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

import json
import urllib2

import sys
import getopt
import ConfigParser
import re
import subprocess
import threading
import platform


opts, args = getopt.getopt(sys.argv[1:], "hc:")
username = ""
password = ""
driverpath = ""


slackAPP_controlRemedyScriptNetworkListenSwitch = "http://124.251.110.252/SlackAPP/slackEventListen/controlRemedyScriptNetworkListenSwitch"
slackAPP_setRemedyNetListenTrue = "http://124.251.110.252/SlackAPP/slackEventListen/setRemedyNetListenTrue"
# netMonitoringUrl = "127.0.0.1"

configPath = "config.ini"

# for op, value in opts:
#     if op == "-c":
#         configPath = value
#     elif op == "-h":
#         print "-c -------- config file path"
#         print ""
#         print "Please download the chrome driver before use"
#         print "driver download and version, CSDN link ：http://blog.csdn.net/chaomaster/article/details/52963265"
#         print "when the script exit ,we must log out the remedy"
#         print "Please ensure that the parameters of the input is correct, otherwise may cause driver abnormal or logon failure"
#         sys.exit()

# if not configPath:
#     print "ERR : no configuration \n"
#     print "please create configuration file\n"
#     print ""
#     print "Please download the chrome driver before use"
#     print "driver download and version, CSDN link ：http://blog.csdn.net/chaomaster/article/details/52963265"
#     print "when the script exit ,we must log out the remedy"
#     print "Please ensure that the configuration file's parameters of the input is correct, otherwise may cause driver abnormal or logon failure"
#     sys.exit()




try:
    config = ConfigParser.ConfigParser()
    with open(configPath, 'r+') as cfgfile:
        config.readfp(cfgfile)

    username = config.get("info", "username")
    password = config.get("info", "password")
    driverpath = config.get("info", "driverpath")
    audioPath = config.get("info", "audiopath")

    slack_channel = "#remedy-stuff"
    detail_slack_notice_channel = "#random"

    slackAPP_postMessageAPI = config.get("info", "slackAPP_postMessageAPI")
    slackApp_postUser = config.get("info", "slackApp_postUser")
except:
    print "ERR : no configuration \n"
    print "please create configuration file\n"
    print "configuration must be renamed config.ini\n"
    print "configuration need to fill username .password .driverPath .audioPath\n"
    print "driver download and version, CSDN link : http://blog.csdn.net/chaomaster/article/details/52963265\n"
    print "the script will be exit in 5 second\n"
    time.sleep(5)

if (not username) or (not password) or (not driverpath):
    print "Please send the user name, password, drive path to configuration file, such as config.ini "
    sys.exit()


def postSlackAPP(requestMessage): #调用 slack 接口方法
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=slackAPP_postMessageAPI, headers=headers, data=json.dumps(requestMessage))
    response = urllib2.urlopen(request)
    return "发送成功"

def postNetSwitch(postMessage):
    header = {'Content-Type': 'application/json'}
    netRequest = urllib2.Request(url=slackAPP_controlRemedyScriptNetworkListenSwitch, headers=header, data=json.dumps(postMessage))
    response = urllib2.urlopen(netRequest)

def postNetStatus(postMessage):
    header = {'Content-Type': 'application/json'}
    netRequest = urllib2.Request(url=slackAPP_setRemedyNetListenTrue, headers=header,
                                 data=json.dumps(postMessage))
    response = urllib2.urlopen(netRequest)

def NetCheck(ip):   #检测网络状况
    try:
        if platform.system() == "Windows":
            # print "正确进入 windows 分支"
            p = subprocess.Popen(["ping", "-n", "4", ip],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outW = p.stdout.read()
            errW = p.stderr.read()
            regex1 = re.compile("100%")
            regex2 = re.compile("找不到主机")
            # print ""
            # print "outW"
            # print outW
            # print ""
            # print "errW"
            # print errW
            # print ""
            if (len(regex1.findall(outW))) or (len(regex2.findall(outW))):
                # print ip + " online"
                return False
            else:
                # print ip + " offline"
                return True
        else:
            p = subprocess.Popen(["ping", "-c", "4", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.stdout.read()
            err = p.stderr.read()
            regex1 = re.compile("100.0% packet loss")
            regex2 = re.compile("100% packet loss")
            # print out
            # print err
            if (len(regex1.findall(out)) == 0) and (len(regex2.findall(out)) == 0) and ((len(err)) == 0):
                # print ip + ' online'
                return True
            else:
                # print ip + ' offine'
                return False
    except:
        print "NetCheck work error"
        return False

def threadOffline(threadName, delay):
    i = 1
    netMonitoringStart = {"channel": slack_channel, "user": slackApp_postUser, "swi": "open"}
    postNetSwitch(netMonitoringStart)
    while True:
        time.sleep(120)
        flag1 = NetCheck("www.baidu.com")
        flag2 = NetCheck("chinabluemix.itsm.unisysedge.cn")
        netMonitoringContinue = {"bo": "true"}
        postNetStatus(netMonitoringContinue)
        # print flag
        # print i
        # i += 1
        if (flag1 == False) and (flag2 == False):
            print "Abnormal network"
            netErrorNC = {"channel": slack_channel, "text": slackApp_postUser + "   网络异常，请注意！！！"}
            postSlackAPP(netErrorNC)
            # netMonitoringErr = {"status": "err"}
            # postNetMonitoring(netMonitoringErr)
            offlineBrowser = webdriver.Chrome(executable_path=driverpath)
            offlineBrowser.get(audioPath)
            break

# def isElementExist(element):  # 判断函数
#     flag = True
#     try:
#         browser.find_element_by_xpath(element)
#         return flag
#     except:
#         flag = False
#         return flag





def threadMain(threadName, delay):


# 驱动配置及下载 CSDN 连接 ：http://blog.csdn.net/chaomaster/article/details/52963265

# browser = webdriver.Firefox(executable_path='/Users/xuechao/seleniumSupport/geckodriver')
    browser = webdriver.Chrome(executable_path=driverpath)

    browser.get('https://chinabluemix.itsm.unisysedge.cn/arsys/shared/loggedout.jsp')
    browser.implicitly_wait(50)


# 登录 remedy
    browser.find_element_by_id('username-id').send_keys(username)
    browser.find_element_by_id('pwd-id').send_keys(password)
    browser.find_element_by_id('loginText').click()


# 处理流程
    locator1 = (By.XPATH, ".//*[@id='WIN_1_304017100']/div/div")  # 定位已指派页面按钮
    locator2 = (By.CSS_SELECTOR, ".BaseTableCellOdd.BaseTableCellOddColor.BaseTableStaticText")  # 定位 ticket

# 添加死循环

    i = 1  # 计数

    enTestString = "Test"
    enTestString2 = "Test"
    enTestString3 = "TEST"
    cnTestString = u"测试"

    while True:
        try:
            WebDriverWait(browser, 50, 0.5).until(EC.visibility_of_element_located(locator1))
            browser.find_element_by_xpath(".//*[@id='WIN_1_304017100']/div/div").click()

        # except NoSuchElementException as e:
        #     try:
        #         browser.switch_to_alert().accept()
        #

        except:
            print u"进入未受理标签失败"
            # browser.refresh()
            #     print u"获取元素失败，请正常登出后重启脚本"
            ackErrorNC = {"channel": slack_channel, "text": slackApp_postUser + " Remedy script exception! ! (Abnormal details: Can not find the ACK label)"}
            postSlackAPP(ackErrorNC)

            # netMonitoringStop = {"status": "stop"}
            # postNetMonitoring(netMonitoringStop)

            ackBrowser = webdriver.Chrome(executable_path=driverpath)
            ackBrowser.get(audioPath)
                # print audioPath

        finally:

            try:
                WebDriverWait(browser, 30000000, 0.5).until(EC.visibility_of_element_located(locator2))  # 模拟等待 时间无限大

                testString = browser.find_element_by_xpath(".//*[@id='T302087200']/tbody/tr[2]/td[2]/nobr/span").text # 过滤 测试 或者 test
                if ((enTestString in testString) == False) and ((cnTestString in testString) == False) and ((enTestString2 in testString) == False) and ((enTestString3 in testString) == False):
                    doubleClickArea = browser.find_element_by_css_selector(".BaseTableCellOdd.BaseTableCellOddColor.BaseTableStaticText")
                    ActionChains(browser).double_click(doubleClickArea).perform()
                else:
                    print "【test】 ticket, please manual processing"
                    testBrowser = webdriver.Chrome(executable_path=driverpath)
                    testBrowser.get(audioPath)
                    # exit()
            finally:
                try:
                    browser.find_element_by_xpath(".//*[@id='arid_WIN_2_536870940']").send_keys("in progress")  # 添加初始响应

                    time.sleep(1)

                    # browser.find_element_by_xpath(u".//*[@id='WIN_2_536870930']/div/div").click()  # 受理 .//*[@id='WIN_2_536870924']/div

                    # ackArea = browser.find_element_by_css_selector("#WIN_2_536870924")
                    ackArea = browser.find_element_by_xpath(".//*[@id='WIN_2_536870924']/div/div")
                    # ActionChains(browser).double_click(ackArea).perform()
                    saveArea = browser.find_element_by_xpath(".//*[@id='WIN_2_301614800']/div/div")

                    saveArea.click()

                    time.sleep(1)

                    ackArea.click()

                    print "already deal " + str(i) + " ticket"
                    print "ticket summary: " + testString
                    i += 1
                    time.sleep(2)
                    browser.refresh()  # 浏览器刷新

                    try:   # 警告框处理
                        browser.switch_to_alert().accept()
                        ackAlertNC = {"channel": slack_channel, "text": slackApp_postUser + "   accept alert box"}
                        postSlackAPP(ackAlertNC)
                        print "accept alert box"
                    except :
                        print "no such alert box"
                        # print e

                    timeString = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
                    # f = open("ticket.log", "a+")
                    # f.read()
                    # f.write(timeString + " " + testString + "\n")
                    # f.close()

                    ticketDetailNC = {"channel": detail_slack_notice_channel, "text": " Ticket Detail : " + timeString + "          " + testString}
                    postSlackAPP(ticketDetailNC)

                    time.sleep(3)



                except:
                    print "Accept button failed to get OR Failed to add initial response"

                    ackLableErrorNC = {"channel": slack_channel, "text": slackApp_postUser + "   fech exception, please confirm with remedy script"}
                    postSlackAPP(ackLableErrorNC)

                    # netMonitoringStop = {"status": "stop"}
                    # postNetMonitoring(netMonitoringStop)

                    # ackLableBrowser = webdriver.Chrome(executable_path=webdriver)
                    # ackLableBrowser.get(audioPath)
                    # exit()




                    browser.refresh()

                    try:   # 警告框处理
                        browser.switch_to_alert().accept()
                        ackAlertNC = {"channel": slack_channel, "text": slackApp_postUser + "   accept alert box"}
                        postSlackAPP(ackAlertNC)
                        print "accept alert box"
                    except :
                        print "no such alert box"
                        # print e


threads = []
t1 = threading.Thread(target=threadMain, args=("thread", 0,))
threads.append(t1)
t2 = threading.Thread(target=threadOffline, args=("threadMain", 0,))
threads.append(t2)

if __name__ == "__main__":
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()



# locator2 = (By.XPATH, ".//*[@id='T302087200']/tbody/tr[2]/td[@class='BaseTableCellOdd BaseTableCellOddColor BaseTableStaticText'][1]")
# try:
#     WebDriverWait(browser, 30, 0.5).until(EC.visibility_of_element_located(locator2))
#     doubleClickArea = browser.find_element_by_xpath(".//*[@id='T302087200']/tbody/tr[2]/td[@class='BaseTableCellOdd BaseTableCellOddColor BaseTableStaticText'][1]")
#     ActionChains(browser).double_click(doubleClickArea).perform()
#     print '获取成功'
# finally:
#     browser.close()


# 注销 remedy
# print '开始注销'
# browser.find_element_by_xpath('.//*[@id="WIN_0_300000044"]/div/div').click()
#
#
# browser.implicitly_wait(30)
#
# browser.quit()

