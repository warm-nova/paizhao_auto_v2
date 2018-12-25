import datetime
import time
import datetime
import paramiko
import os
import sys
from shutil import copyfile
import baseFunction_paizuoye
import baseFunction_lovezuoye
import optimizeProcess


def get_remote_date():
    nowtime = datetime.datetime.now()
    gettime = nowtime + datetime.timedelta(days=-2)
    timer = gettime.strftime('%Y-%m-%d')
    return timer

#服务器信息
host_name = "10.200.2.235"
username = "stf"
password = "stf"
port = 22

#文件夹信息
localdir_orig = "E:\\PycharmProjects\\paizhao_auto_v2\\questionPic"
localdir_labe = "E:\\PycharmProjects\\paizhao_auto_v2\\questionPic_17zuoye"
localdir_screenshot = "E:\\PycharmProjects\\paizhao_auto_v2\\questionScreenshot"



def auto_rename_17zuoye(dateCount):
    filekey = os.listdir(localdir_labe)
    #手动跑需要修改成手动日期
    #datecount = get_remote_date()
    #datecount = "2018-11-24"
    n = 0
    for i in filekey:
        oldname = "E:\\PycharmProjects\\paizhao_auto_v2\\questionPic_17zuoye\\" + filekey[n]
        timer = time.strftime('%m%d', time.localtime(time.time()))
        newname = "E:\\PycharmProjects\\paizhao_auto_v2" + '\\questionScreenshot\\' + filekey[n] + "_17zuoye" + "_" + dateCount + '.png'
        # print(newname)
        n = n + 1
        os.rename(oldname, newname)

#参数:服务器下载的日期
def autoMovFile_from_serv(datecount):
    #远程路径
    remote_orig = "/home/stf/arithmetic_check/pics/" + datecount + "/comp_orig/"
    remote_labe = "/home/stf/arithmetic_check/pics/" + datecount + "/comp_labe/"
    conn = paramiko.Transport(host_name, port)
    conn.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(conn)

    pic_files = sftp.listdir(remote_orig)
    for f in pic_files:
        print("Downloading pic files in:" + remote_orig)
        print("NOW IS:" + (remote_orig + "/" + f))
        sftp.get(remote_orig + "/" + f, os.path.join(localdir_orig, f))
        print("SUCCESS!")

    pic_lable_files = sftp.listdir(remote_labe)
    for f in pic_lable_files:
        print("Downloading pic files in:" + remote_labe)
        print("NOW IS:" + (remote_labe + "/" + f))
        sftp.get(remote_labe + "/" + f, os.path.join(localdir_labe, f))
        print("SUCCESS!")
    sftp.close()

#复制文件
def copyFiles(sourceDir,  targetDir):
    for file in os.listdir(sourceDir):
         sourceFile = os.path.join(sourceDir,  file)
         targetFile = os.path.join(targetDir,  file)
         if os.path.isfile(sourceFile):
             if not os.path.exists(targetDir):
                 os.makedirs(targetDir)
             if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                     open(targetFile, "wb").write(open(sourceFile, "rb").read())
         if os.path.isdir(sourceFile):
             First_Directory = False
             copyFiles(sourceFile, targetFile)

def auto_generate_result(dateCount):
    dst_folder= "E:\\PycharmProjects\\paizhao_auto_v2\\outputResult\\"+ dateCount
    if not os.path.isdir("E:\\PycharmProjects\\paizhao_auto_v2\\outputResult\\"+ dateCount):
        os.mkdir("E:\\PycharmProjects\\paizhao_auto_v2\\outputResult\\"+dateCount)
    copyFiles(localdir_screenshot,dst_folder)
    copyFiles(localdir_orig,dst_folder)

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def run(str):
        autoMovFile_from_serv(str)
        auto_rename_17zuoye(str)
        optimizeProcess.fullProcessPic(str)
        #baseFunction_lovezuoye.syncpic_lovezuoye()
        #baseFunction_paizuoye.syncpic_paizuoye()
        auto_generate_result(str)
        del_file(localdir_orig)
        del_file(localdir_labe)
        del_file(localdir_screenshot)


if __name__ == '__main__':
    run("2018-12-20")
    run("2018-12-21")
    run("2018-12-22")
    run("2018-12-23")

    #
    # while True:
    #        now = datetime.datetime.now()
    #        if now.hour == 17:
    #            run(get_remote_date())
    #        else:
    #            time.sleep(1000)
    #

