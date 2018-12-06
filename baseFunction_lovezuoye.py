import os
import sys
import subprocess
from appium import webdriver
import shutil
import time
import base64
import datetime

pkgname = "ai.zuoye.app"
mainactivity = "com.homework.app.ui.activity.WelcomeActivity"

#传递图片到手机中
def syncpic_lovezuoye():
    #传入图片
    nowpath = os.getcwd() + "\\questionPic"
    sdcard_path = "/storage/sdcard0/DCIM/Camera"
    sdcard_path2 = "/storage/emulated/legacy/DCIM/Camera"

    desired_caps = {
        'platformName': 'Android',
        'deviceName': '220cba31',
        # 'deviceName': '10.200.29.50:5555',
        'platformVersion': '4.3',
        'appPackage': 'ai.zuoye.app',  # 红色部分如何获取下面讲解
        'appActivity': 'com.homework.app.ui.activity.WelcomeActivity',
        'noReset': True
    }

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='ai.zuoye.app:id/lav_camera']").click()

    print("step 2:Detect path in PC:", nowpath)
    counter=0
    for path,childpath,files in os.walk(nowpath):
        for i in range(len(files)):
            if files[i][-3:] == 'jpg' or files[i][-3:] == "JPG" or files[i][-3:] == 'PNG' or files[i][-3:] == 'png':

                delpic_inappium = driver.execute_script('mobile: shell', {
                    'command': 'rm',
                    'args': ['-f', '/storage/emulated/legacy/DCIM/Camera/*.jpg'],
                    'includeStderr': True,
                    'timeout': 3000})
                delpic_ocr = driver.execute_script('mobile: shell', {
                    'command': 'rm',
                    'args': ['-f', '/storage/emulated/legacy/as_ocr/images/PhotoCheck/*.*'],
                    'includeStderr': True,
                    'timeout': 3000})
                refresh_ocr = driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['broadcast','-a','android.intent.action.MEDIA_MOUNTED','-d','file:///storage/emulated/legacy/as_ocr/images/PhotoCheck/'],
                    'includeStderr': True,
                    'timeout': 3000})

                print("STEP 1: DEL PIC FINISH")
                nowpic = nowpath + "\\" + files[i]
                print("Now pic is:" + nowpic)

                with open(nowpic,"rb") as f:
                     image_data = f.read()
                     base64_data = base64.b64encode(image_data,altchars=None)


                finaldata = str(base64_data,encoding='utf-8')
                #print(finaldata)
                driver.push_file("/storage/emulated/legacy/DCIM/Camera/test.jpg",finaldata)


                #syncpic = 'adb push ' + nowpic + " /storage/emulated/legacy/DCIM/Camera/test.jpg"  # 传入图片
                #step2 = subprocess.Popen(syncpic, shell=True, stdout=subprocess.PIPE)
                #print(syncpic)

                print("STEP 2:SYNC PICTURE FINISH.")

                refresh_pic = driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['broadcast', '-a', 'android.intent.action.MEDIA_MOUNTED', '-d',
                             'file:///storage/emulated/legacy/DCIM/Camera/test.jpg'],
                    'includeStderr': True,
                    'timeout': 10000})



                print("STEP 3 FINISH")

                # start_appium = "appium -a 127.0.0.1 -p 4723 --session-override"
                # step0 = subprocess.Popen(start_appium, shell=True, stdout=subprocess.PIPE)
                # print("RUN SUCCESS")
                try:
                    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='ai.zuoye.app:id/iv_album']").click()
                    time.sleep(3)
                    driver.find_element_by_xpath("//android.widget.GridView[@resource-id='ai.zuoye.app:id/grid']/android.widget.FrameLayout[1]/android.widget.TextView[1]").click()
                    driver.find_element_by_xpath("//android.widget.Button[@resource-id='ai.zuoye.app:id/commit']").click()
                except:
                    continue

                time.sleep(10)

                img_folder = os.getcwd() + '\\questionScreenshot\\'
                nowtime = datetime.datetime.now()
                gettime = nowtime + datetime.timedelta(days=-2)
                timer = gettime.strftime('%m-%d')
                screen_save_path =  files[i] + "_lovezuoye" + "_"+ timer +'.png'
                print("STEP4 : SCREENSHOT IN "+ img_folder)
                print("NO." + str(counter) + "FINISHED")
                driver.get_screenshot_as_file(img_folder + screen_save_path)
               # driver.reset()
                counter=counter+1
                try:
                    driver.find_element_by_xpath("//android.widget.TextView[@resource-id='ai.zuoye.app:id/tv_confirm']").click()
                except:
                    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='ai.zuoye.app:id/iv_back']").click()

    driver.quit()






