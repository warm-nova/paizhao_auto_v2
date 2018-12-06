import os
import sys
import subprocess
from appium import webdriver
import shutil
import time
import base64
import datetime

#包路径
lovezuoye_pkgname = "ai.zuoye.app"
lovezuoye_mainactivity = "com.homework.app.ui.activity.WelcomeActivity"
paizuoye_pkgname = "com.knowbox.ocr"
paizuoye_mainactivity = "com.knowbox.ocr.MainActivity"

#手机的图片路径
nowpath = os.getcwd() + "\\questionPic"
sdcard_path = "/storage/sdcard0/DCIM/Camera"
sdcard_path2 = "/storage/emulated/legacy/DCIM/Camera"

def fullProcessPic(datetag):
    #爱作业流程
    desired_caps_lovezuoye = {
        'platformName': 'Android',
        'deviceName': '220cba31',
        # 'deviceName': '10.200.29.50:5555',
        'platformVersion': '4.3',
        'appPackage': 'ai.zuoye.app',  # 红色部分如何获取下面讲解
        'appActivity': 'com.homework.app.ui.activity.WelcomeActivity',
        'noReset': True
    }

    desired_caps_paizuoye = {
        'platformName': 'Android',
        'deviceName': '220cba31',
        # 'deviceName': '10.200.29.50:5555',
        'platformVersion': '4.3',
        'appPackage': 'com.knowbox.ocr',  # 红色部分如何获取下面讲解
        'appActivity': 'MainActivity',
        'noReset': True
    }

    print("Step 1:Detect path in pc",nowpath)
    counter = 0
    for path, childpath, files in os.walk(nowpath):
        for i in range(len(files)):
            if files[i][-3:] == 'jpg' or files[i][-3:] == "JPG" or files[i][-3:] == 'PNG' or files[i][-3:] == 'png':

                driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps_lovezuoye)

                #搞相册
                delpic_inappium = driver.execute_script('mobile: shell', {
                    'command': 'rm',
                    'args': ['-f', '/storage/emulated/legacy/DCIM/Camera/*.jpg'],
                    'includeStderr': True,
                    'timeout': 8000})
                delpic_ocr = driver.execute_script('mobile: shell', {
                    'command': 'rm',
                    'args': ['-f', '/storage/emulated/legacy/as_ocr/images/PhotoCheck/*.*'],
                    'includeStderr': True,
                    'timeout': 8000})
                refresh_ocr = driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['broadcast', '-a', 'android.intent.action.MEDIA_MOUNTED', '-d',
                             'file:///storage/emulated/legacy/as_ocr/images/PhotoCheck/'],
                    'includeStderr': True,
                    'timeout': 8000})

                #等待这个activity的出现
                driver.wait_activity("com.homework.app.ui.activity.HomeActivity",15,interval=2)
                try:
                    time.sleep(4)
                    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='ai.zuoye.app:id/lav_camera']").click()
                except:
                    #更新了返回重新按
                    time.sleep(4)
                    driver.press_keycode(4)
                    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='ai.zuoye.app:id/lav_camera']").click()
                print("Step 2: Delete picture in album")
                nowpic = nowpath + "\\" + files[i]
                print("Now pic is:" + nowpic)

                #传照片
                with open(nowpic,"rb") as f:
                     image_data = f.read()
                     base64_data = base64.b64encode(image_data,altchars=None)
                finaldata = str(base64_data,encoding='utf-8')
                driver.push_file("/storage/emulated/legacy/DCIM/Camera/test.jpg",finaldata)
                print("Step 3:Sync picture in mobile phone")
                refresh_pic = driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['broadcast', '-a', 'android.intent.action.MEDIA_MOUNTED', '-d',
                             'file:///storage/emulated/legacy/DCIM/Camera/test.jpg'],
                    'includeStderr': True,
                    'timeout': 10000})
                print("Step 3:Go for formal test")

                try:
                    time.sleep(4)
                    driver.find_element_by_xpath(
                        "//android.widget.ImageView[@resource-id='ai.zuoye.app:id/iv_album']").click()
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        "//android.widget.GridView[@resource-id='ai.zuoye.app:id/grid']/android.widget.FrameLayout[1]/android.widget.TextView[1]").click()
                    driver.find_element_by_xpath(
                        "//android.widget.Button[@resource-id='ai.zuoye.app:id/commit']").click()
                    aizuoye_time_start = datetime.datetime.now()
                    print("TIME START:",aizuoye_time_start)
                    aizuoye_time_count = 0
                    while True:
                        try:
                            driver.find_element_by_xpath("//android.widget.TextView[@resource-id='ai.zuoye.app:id/tv_share']")
                            aizuoye_time_end = datetime.datetime.now()
                            print("TIME END:", aizuoye_time_end)
                            break
                        except:
                            time.sleep(0.5)
                            aizuoye_time_count = aizuoye_time_count + 0.5
                            if aizuoye_time_count > 15:
                                aizuoye_time_end = datetime.MINYEAR
                                print("TIME END:", aizuoye_time_end)
                                break
                except:
                    continue

                time.sleep(1)

                img_folder = os.getcwd() + '\\questionScreenshot\\'

                screen_save_path = files[i] + "_lovezuoye" + "_" + datetag + '.png'
                print("Step 4 : Screenshot in " + img_folder)
                print("NO." + str(counter) + " FINISHED")
                driver.get_screenshot_as_file(img_folder + screen_save_path)
                # driver.reset()
                driver.quit()

                driver2 = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps_paizuoye)
                time.sleep(6)
                driver2.tap([(360, 780)], 200)
                try:
                    time.sleep(4)
                    driver2.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.knowbox.ocr:id/tv_album']").click()
                    driver2.find_element_by_xpath("//android.view.View[@resource-id='com.knowbox.ocr:id/check_view']").click()
                    driver2.find_element_by_xpath("//android.widget.TextView[@resource-id='com.knowbox.ocr:id/button_apply']").click()

                    paizuoye_time_count=0
                    paizuoye_time_start=datetime.datetime.now()
                    print("TIME START:", paizuoye_time_start)
                    while True:
                        try:
                            driver.find_element_by_xpath("//android.widget.TextView[@resource-id='ai.zuoye.app:id/tv_share']")
                            paizuoye_time_end = datetime.datetime.now()
                            print("TIME END:", paizuoye_time_end)
                            break
                        except:
                            time.sleep(0.5)
                            paizuoye_time_count = paizuoye_time_count + 0.5
                            if paizuoye_time_count > 15:
                                paizuoye_time_end = datetime.MINYEAR
                                print("TIME END:", paizuoye_time_end)
                                break

                except:
                    continue

                time.sleep(10)
                img_folder = os.getcwd() + '\\questionScreenshot\\'
                screen_save_path = files[i] + "_paizuoye" + "_" + datetag + '.png'
                print("STEP4 : SCREENSHOT IN " + img_folder)
                print("NO." + str(counter) + " FINISHED")
                driver2.get_screenshot_as_file(img_folder + screen_save_path)
                driver2.quit()
                counter = counter + 1
                print("ALL FINISH.")
