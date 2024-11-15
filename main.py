import os
from flask import Flask, request, redirect, send_file
from flask import render_template
from configparser import ConfigParser
import configparser
import shutil
import requests
import urllib
import tftpy
from bs4 import BeautifulSoup
import threading
from threading import Event
import time
import datetime

app=Flask(__name__)

def LogAppend(msg):
    now = datetime.datetime.now()
    try:
        with open("log.txt","a") as f:
            f.write(f"{now.strftime('%d-%m-%Y %H:%M:%S')} - {msg} \n")
            print(f"{now.strftime('%d-%m-%Y %H:%M:%S')} - {msg} \n")
    except:
        with open("log.txt","w") as f:
            f.write(f"{now.strftime('%d-%m-%Y %H:%M:%S')} - {msg} \n")
            print(f"{now.strftime('%d-%m-%Y %H:%M:%S')} - {msg} \n")

def ReadDocStatus():
    pth="./ini/"
    dirlist=os.listdir(pth)
    dirlist.sort()
    fname="status_sta.txt"
    statusCodes = {}
    with open(fname,'r') as f:
        data=f.readlines()
    for line in data:
        sta=line.strip().split("=")
        if int(sta[1]) == 1:
            statusCodes[sta[0]] = "green"
        else:
            statusCodes[sta[0]]="red"

    for sta in dirlist:
        if sta in statusCodes:
            pass
        else:
            statusCodes[sta]="red"
    return statusCodes

def CreateDocStatus(dirlist, isFirst):
    pth = "./ini/"
    statusCodes = {}
    dirlist.sort()
    if isFirst:
        with open("status_sta.txt","w") as f:
            for sta in dirlist:
                f.write(sta+"="+"0"+"\n")
    else:
        for sta in dirlist:
            fname = pth + sta + "/seisview_imp.ini"
            config = ConfigParser()
            readErr = False
            r=False
            try:
                config.read(fname)
            except:
                readErr = True
            if not readErr:
                try:
                    LogAppend(f"{sta}: start connect")
                    r = requests.get(f"http://{config.get('NET', 'ETH_IP')}/").status_code == 200
                    LogAppend(f"{sta}: success connect")
                except Exception as e:
                    LogAppend(f"{sta}: fail connect! {e}")
                    pass

                if r:
                    statusCodes[sta] = 1
                else:
                    statusCodes[sta] = 0
            else:
                statusCodes[sta] = 0
                LogAppend(f"{sta}: ini-file is not correct")

        with open("status_sta.txt","w") as f:
            for sta in dirlist:
                f.write(sta+"="+str(statusCodes[sta])+"\n")
    return statusCodes

def readini(fname):
    config = ConfigParser()
    readErr=False
    try:
        config.read(fname)
    except:
        readErr=True

    stat = {}
    try:
        stat['device_name'] = config.get('SYSTEM', 'DEVICE_NAME')
    except:
        stat['device_name'] = "LAB PTS"
        readErr = True

    try:
        stat['samprate'] = config.get('SYSTEM', 'SAMPRATE')
    except:
        stat['samprate'] = "500"
        readErr = True

    try:
        stat['LCD_ON_TIME'] = config.get('SYSTEM', 'LCD_ON_TIME')
    except:
        stat['LCD_ON_TIME'] = "255"
        readErr = True

    try:
        stat['TEMP_MES_INT'] = config.get('SYSTEM', 'TEMP_MES_INT')
    except:
        stat['TEMP_MES_INT'] = "3600"
        readErr = True

    try:
        stat['SENS_POW'] = int(config.get('SYSTEM', 'SENS_POW'))
    except:
        stat['SENS_POW'] = 0
        readErr = True
    try:
        stat['SLOW_REC_INTERVAL'] = config.get('SYSTEM', 'SLOW_REC_INTERVAL')
    except:
        stat['SLOW_REC_INTERVAL'] = 0
        readErr = True

    try:
        stat['GAIN'] = int(config.get('SYSTEM', 'GAIN'))
    except:
        stat['GAIN'] = 1
        readErr = True

    try:
        stat['AUTO'] = int(config.get('SYSTEM', 'AUTO'))
    except:
        stat['AUTO'] = 1
        readErr = True

    try:
        stat['LEN'] = config.get('SYSTEM', 'LEN')
    except:
        stat['LEN'] = "3600"
        readErr = True

    net = {}
    try:
        net['ETH_POW'] = int(config.get('NET', 'ETH_POW'))
    except:
        net['ETH_POW'] = 0
        readErr = True

    try:
        net['DSL_POW'] = int(config.get('NET', 'DSL_POW'))
    except:
        net['DSL_POW'] = 1
        readErr = True

    try:
        net['ETH_IP'] = config.get('NET', 'ETH_IP')
    except:
        net['ETH_IP'] = "192.168.192.168"
        readErr = True

    try:
        net['ETH_MASK'] = config.get('NET', 'ETH_MASK')
    except:
        net['ETH_MASK'] = "255.255.255.0"
        readErr = True

    try:
        net['ETH_GW'] = config.get('NET', 'ETH_GW')
    except:
        net['ETH_GW'] = "192.168.192.1"
        readErr = True

    time = {}
    try:
        time['SOURCE'] = config.get('TIME', 'SOURCE')
    except:
        time['SOURCE'] = "3"
        readErr = True

    try:
        time['NTP_IP'] = config.get('TIME', 'NTP_IP')
    except:
        time['NTP_IP'] = "192.168.192.1"
        readErr = True

    try:
        time['NTP_PORT'] = config.get('TIME', 'NTP_PORT')
    except:
        time['NTP_PORT'] = "123"
        readErr = True

    try:
        time['GPS_SLEEP_TIME'] = config.get('TIME', 'GPS_SLEEP_TIME')
    except:
        time['GPS_SLEEP_TIME'] = "0"
        readErr = True

    socket0 = {}
    try:
        socket0['SERVICE'] = config.get('SOCKET0', 'SERVICE')
    except:
        socket0['SERVICE'] = "0"
        readErr = True

    if int(socket0['SERVICE']) == 7:
        socket0['SERVICE'] = 5

    try:
        socket0['PORT'] = config.get('SOCKET0', 'PORT')
    except:
        socket0['PORT'] = "80"
    socket1 = {}
    try:
        socket1['SERVICE'] = config.get('SOCKET1', 'SERVICE')
        readErr = True

        if (socket1['SERVICE'] == ""):
            socket1['SERVICE'] = "0"
    except:
        socket1['SERVICE'] = "0"
        readErr = True

    if int(socket1['SERVICE']) == 7:
        socket1['SERVICE'] = 5

    try:
        socket1['PORT'] = config.get('SOCKET1', 'PORT')
    except:
        socket1['PORT'] = "18000"
        readErr = True

    socket2 = {}
    try:
        socket2['SERVICE'] = config.get('SOCKET2', 'SERVICE')
        if (socket2['SERVICE'] == ""):
            socket2['SERVICE'] = "0"
    except:
        socket2['SERVICE'] = "0"
        readErr = True

    if int(socket2['SERVICE']) == 7:
        socket2['SERVICE'] = 5

    try:
        socket2['PORT'] = config.get('SOCKET2', 'PORT')
    except:
        socket2['PORT'] = "123"
        readErr = True

    socket3 = {}
    try:
        socket3['SERVICE'] = config.get('SOCKET3', 'SERVICE')
        if (socket3['SERVICE'] == ""):
            socket3['SERVICE'] = "0"
    except:
        socket3['SERVICE'] = "0"
        readErr = True

    if int(socket3['SERVICE']) == 7:
        socket3['SERVICE'] = 5

    try:
        socket3['PORT'] = config.get('SOCKET3', 'PORT')
    except:
        socket3['PORT'] = "69"
        readErr = True

    ch0 = {}
    try:
        ch0['NET'] = config.get('CH0', 'NET')
    except:
        ch0['NET'] = "PR"
        readErr = True

    try:
        ch0['STATION'] = config.get('CH0', 'STATION')
    except:
        ch0['STATION'] = "PTSLB"
        readErr = True

    try:
        ch0['LOC'] = config.get('CH0', 'LOC')
    except:
        ch0['LOC'] = "00"
    try:
        ch0['NAME'] = config.get('CH0', 'NAME')
    except:
        ch0['NAME'] = "CH0"
        readErr = True

    try:
        ch0['TO_DISK'] = int(config.get('CH0', 'TO_DISK'))
    except:
        ch0['TO_DISK'] = 1
        readErr = True

    try:
        ch0['TO_NET'] = int(config.get('CH0', 'TO_NET'))
    except:
        ch0['TO_NET'] = 1
        readErr = True

    try:
        ch0['TO_DISP'] = int(config.get('CH0', 'TO_DISP'))
    except:
        ch0['TO_DISP'] = 1
        readErr = True

    ch1 = {}
    try:
        ch1['NET'] = config.get('CH1', 'NET')
    except:
        ch1['NET'] = "PR"
        readErr = True

    try:
        ch1['STATION'] = config.get('CH1', 'STATION')
    except:
        ch1['STATION'] = "PTSLB"
        readErr = True

    try:
        ch1['LOC'] = config.get('CH1', 'LOC')
    except:
        ch1['LOC'] = "00"
        readErr = True

    try:
        ch1['NAME'] = config.get('CH1', 'NAME')
    except:
        ch1['NAME'] = "CH1"
        readErr = True

    try:
        ch1['TO_DISK'] = int(config.get('CH1', 'TO_DISK'))
    except:
        ch1['TO_DISK'] = 1
        readErr = True

    try:
        ch1['TO_NET'] = int(config.get('CH1', 'TO_NET'))
    except:
        ch1['TO_NET'] = 1
        readErr = True

    try:
        ch1['TO_DISP'] = int(config.get('CH1', 'TO_DISP'))
    except:
        ch1['TO_DISP'] = 1
        readErr = True

    ch2 = {}
    try:
        ch2['NET'] = config.get('CH2', 'NET')
    except:
        ch2['NET'] = "PR"
        readErr = True

    try:
        ch2['STATION'] = config.get('CH2', 'STATION')
    except:
        ch2['STATION'] = "PTSLB"
        readErr = True

    try:
        ch2['LOC'] = config.get('CH2', 'LOC')
    except:
        ch2['LOC'] = "00"
        readErr = True

    try:
        ch2['NAME'] = config.get('CH2', 'NAME')
    except:
        ch2['NAME'] = "CH2"
        readErr = True

    try:
        ch2['TO_DISK'] = int(config.get('CH2', 'TO_DISK'))
    except:
        ch2['TO_DISK'] = 1
        readErr = True

    try:
        ch2['TO_NET'] = int(config.get('CH2', 'TO_NET'))
    except:
        ch2['TO_NET'] = 1
        readErr = True

    try:
        ch2['TO_DISP'] = int(config.get('CH2', 'TO_DISP'))
    except:
        ch2['TO_DISP'] = 1
        readErr = True

    ch3 = {}
    try:
        ch3['NET'] = config.get('CH3', 'NET')
    except:
        ch3['NET'] = "PR"
        readErr = True

    try:
        ch3['STATION'] = config.get('CH3', 'STATION')
    except:
        ch3['STATION'] = "PTSLB"
        readErr = True

    try:
        ch3['LOC'] = config.get('CH3', 'LOC')
    except:
        ch3['LOC'] = "00"
        readErr = True

    try:
        ch3['NAME'] = config.get('CH3', 'NAME')
    except:
        ch3['NAME'] = "CH3"
        readErr = True

    try:
        ch3['TO_DISK'] = int(config.get('CH3', 'TO_DISK'))
    except:
        ch3['TO_DISK'] = 1
        readErr = True

    try:
        ch3['TO_NET'] = int(config.get('CH3', 'TO_NET'))
    except:
        ch3['TO_NET'] = 1
        readErr = True

    try:
        ch3['TO_DISP'] = int(config.get('CH3', 'TO_DISP'))
    except:
        ch3['TO_DISP'] = 1
        readErr = True

    ch4 = {}
    try:
        ch4['NET'] = config.get('CH4', 'NET')
    except:
        ch4['NET'] = "PR"
        readErr = True

    try:
        ch4['STATION'] = config.get('CH4', 'STATION')
    except:
        ch4['STATION'] = "PTSLB"
        readErr = True

    try:
        ch4['LOC'] = config.get('CH4', 'LOC')
    except:
        ch4['LOC'] = "00"
        readErr = True

    try:
        ch4['NAME'] = config.get('CH4', 'NAME')
    except:
        ch4['NAME'] = "CH4"
        readErr = True

    try:
        ch4['TO_DISK'] = int(config.get('CH4', 'TO_DISK'))
    except:
        ch4['TO_DISK'] = 1
        readErr = True

    try:
        ch4['TO_NET'] = int(config.get('CH4', 'TO_NET'))
    except:
        ch4['TO_NET'] = 1
        readErr = True

    try:
        ch4['TO_DISP'] = int(config.get('CH4', 'TO_DISP'))
    except:
        ch4['TO_DISP'] = 1
        readErr = True

    ch5 = {}
    try:
        ch5['NET'] = config.get('CH5', 'NET')
    except:
        ch5['NET'] = "PR"
        readErr = True

    try:
        ch5['STATION'] = config.get('CH5', 'STATION')
    except:
        ch5['STATION'] = "PTSLB"
        readErr = True

    try:
        ch5['LOC'] = config.get('CH5', 'LOC')
    except:
        ch5['LOC'] = "00"
        readErr = True

    try:
        ch5['NAME'] = config.get('CH5', 'NAME')
    except:
        ch5['NAME'] = "CH5"
        readErr = True

    try:
        ch5['TO_DISK'] = int(config.get('CH5', 'TO_DISK'))
    except:
        ch5['TO_DISK'] = 1
        readErr = True

    try:
        ch5['TO_NET'] = int(config.get('CH5', 'TO_NET'))
    except:
        ch5['TO_NET'] = 1
        readErr = True

    try:
        ch5['TO_DISP'] = int(config.get('CH5', 'TO_DISP'))
    except:
        ch5['TO_DISP'] = 1
        readErr = True

    ch6 = {}
    ch6['HAS_SECTION']=config.has_section('CH6')
    if ch6['HAS_SECTION']:
        try:
            ch6['NET'] = config.get('CH6', 'NET')
        except:
            ch6['NET'] = "PR"
            readErr = True

        try:
            ch6['STATION'] = config.get('CH6', 'STATION')
        except:
            ch6['STATION'] = "PTSLB"
            readErr = True

        try:
            ch6['LOC'] = config.get('CH6', 'LOC')
        except:
            ch6['LOC'] = "--"
            readErr = True

        try:
            ch6['NAME'] = config.get('CH6', 'NAME')
        except:
            ch6['NAME'] = "LOG"
            readErr = True

        try:
            ch6['TO_DISK'] = int(config.get('CH6', 'TO_DISK'))
        except:
            ch6['TO_DISK'] = 1
            readErr = True

        try:
            ch6['TO_NET'] = int(config.get('CH6', 'TO_NET'))
        except:
            ch6['TO_NET'] = 1
            readErr = True

        try:
            ch6['TO_DISP'] = int(config.get('CH6', 'TO_DISP'))
        except:
            ch6['TO_DISP'] = 1
            readErr = True

    reboot = {}
    try:
        reboot['DAILY_REBOOT'] = int(config.get('REBOOT', 'DAILY_REBOOT'))
    except:
        reboot['DAILY_REBOOT'] = 0
        readErr = True

    try:
        reboot['REBOOT_TIME'] = config.get('REBOOT', 'REBOOT_TIME')
    except:
        reboot['REBOOT_TIME'] = "00:00"
        readErr = True

    return stat, time, net, socket0, socket1, socket2, socket3,ch0,ch1,ch2,ch3,ch4,ch5,ch6,reboot, readErr


def getYearFirmware(ip):
    #print(f"http://{ip}/status")
    LogAppend(f"http://{ip}/status")
    r = requests.get(f"http://{ip}/status", timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.find('td', text='Firmware').find_next_sibling("td")
    item = int(str(item).split(" ")[1].split("-")[0])
    LogAppend(f"bs4 res:{item}")
    return item


def getStatusCode(dirlist):
    pth = "./ini/"
    statusCodes={}
    for sta in dirlist:
        fname = pth + sta+ "/seisview_imp.ini"
        config = ConfigParser()
        readErr= False
        try:
            config.read(fname)
        except:
            readErr=True
        try:
            r=requests.get(f"http://{config.get('NET', 'ETH_IP')}/status", timeout=0.1).status_code == 200
        except:
            r=False
        if not readErr:
            statusCodes[sta] = "green"
        else:
            statusCodes[sta] = "red"
    return statusCodes

@app.route('/')
def index():
    pth="./ini/"
    dirlist=os.listdir(pth)
    dirlist.sort()
    statusCodes=ReadDocStatus()
    stat={}
    net = {}
    time = {}
    socket0 = {}
    socket1 = {}
    socket2 = {}
    socket3 = {}
    ch0 = {}
    ch1 = {}
    ch2 = {}
    ch3 = {}
    ch4 = {}
    ch5 = {}
    ch6 = {}
    reboot={}
    chooseSta = ""
    chooseVersion = ""
    flist={}
    return render_template('index.html',  station=dirlist, chooseSta=chooseSta,chooseVersion=chooseVersion, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot, hasSta=False,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5,ch6=ch6, version_list=flist, statusCodes=statusCodes)

@app.route('/newsta', methods=["GET","POST"])
def newStation():
    pth="./ini/"
    dirlist=os.listdir(pth)
    dirlist.sort()
    statusCodes=ReadDocStatus()
    chooseSta = ""
    if request.method == "POST":
        if int(bool(request.form.get("isErmak")))==1:
            newName=request.form.get("newName")
            newIP=request.form.get("newIP")
            try:
                os.mkdir(pth + newName)
                #client = tftpy.TftpClient(newIP, 69)
                #client.download('seisview_imp.ini', f"{pth+newName+'/seisview_imp.ini'}", timeout=60)
                destination = pth + newName + "/seisview_imp.ini"
                url = f"http://{newIP}/seisview_imp.ini"
                try:
                    urllib.request.urlretrieve(url, destination)
                except:
                    shutil.rmtree(pth + newName)
                    return "Sorry! The station is off-line."


                stat, time, net, socket0, socket1, socket2, socket3, ch0, ch1, ch2, ch3, ch4, ch5, ch6, reboot, readErr = readini(destination)
                #if readErr:
                #    shutil.rmtree(pth + newName)
                #    return "Sorry! INI file is incorrect."

                #cmd = f"tftp.exe -i -v {newIP} get seisview_imp.ini"
                #os.system(cmd)
                #shutil.move("seisview_imp.ini",f"{pth+newName+'/seisview_imp.ini'}")
                return redirect(f'/{newName}/last')
            except:
                return "Sorry! The station is off-line."
        else:
            newName = request.form.get("newName")
            fileINI = request.files.get('file', None)
            os.mkdir(pth + newName)
            fileINI.save(f"{pth + newName}/seisview_imp.ini")
            stat, time, net, socket0, socket1, socket2, socket3, ch0, ch1, ch2, ch3, ch4, ch5, ch6, reboot, readErr = readini(f"{pth + newName}/seisview_imp.ini")
            if readErr:
                shutil.rmtree(pth + newName)
                return "Sorry! INI file is incorrect."
            return redirect(f"/{newName}/last")

    return render_template('newsta.html',  station=dirlist, statusCodes=statusCodes, chooseSta=chooseSta, hasSta=False)



@app.route('/<station>/<version>', methods=["GET","POST"])
def stationProp(station,version):

    pth = "./ini/"
    dirlist = os.listdir(pth)
    dirlist.sort()
    if version!="last":
        fname=pth+station+"/seisview_imp_"+version+".ini"
    else:
        fname=pth+station+"/seisview_imp.ini"

    flist = os.listdir(pth + station + "/")
    flist = sorted([x.replace("seisview_imp", "last").replace(".ini", "").replace("last_", "") for x in flist], key=len)
    flist = flist[::-1]
    stat, time, net, socket0, socket1, socket2, socket3, ch0, ch1, ch2, ch3, ch4, ch5, ch6, reboot, readErr = readini(fname)
    chooseSta=station
    chooseVersion = version
    statusCodes = ReadDocStatus()
    if request.method=="POST":
        if int(bool(request.form.get("isDelete")))==1:
            pth = "./ini/"
            shutil.rmtree(pth + station)
            dirlist = os.listdir(pth)
            dirlist.sort()
            return redirect("/")

        elif int(bool(request.form.get("isRename")))==1:
            newName=request.form.get("newNameSta")
            pth = "./ini/"
            try:
                shutil.move(f"{pth}/{chooseSta}",f"{pth}/{newName}")
                return redirect(f"/{newName}/last")
            except Exception as e:
                LogAppend(f"Rename error: {e}")
                return "Sorry! New name station is incorrect."

        elif int(bool(request.form.get("isExport")))==1:

            pth = "./ini/"
            fname=""
            if chooseVersion == 'last':
                fname="seisview_imp.ini"
            else:
                fname="seisview_imp_" + chooseVersion + ".ini"

            try:
                #return f"{pth}/{chooseSta}/{fname}"
                return send_file(f"{pth}/{chooseSta}/{fname}", as_attachment=True,  download_name="seisview_imp.ini", mimetype='text/csv')
            except Exception as e:
                LogAppend(e)
                return "Sorry! Refresh page and try again."

        elif int(bool(request.form.get("isReset")))==1:
            addr = f"http://{net['ETH_IP']}/reset"
            try:
                r = requests.get(addr, timeout=15)
                if r.status_code == 200:
                    return "Reset station is done!"
                else:
                    return "Sorry! Station is off-line."
                return send_file(f"{pth}/{chooseSta}/{fname}", as_attachment=True,  download_name="seisview_imp.ini", mimetype='text/csv')
            except:
                return "Sorry! Station is off-line."

        pth = "./ini/"
        dirlist = os.listdir(pth)
        dirlist.sort()
        config = ConfigParser()
        fname = pth + station + "/seisview_imp.ini"
        config.read(fname)
        flist = os.listdir(pth + station + "/")

        flist = [x.replace("seisview_imp", "last").replace(".ini", "") for x in flist]
        stat = {}

        stat['device_name'] = request.form.get("deviceInput")
        stat['samprate'] = request.form.get("samprateInput")
        stat['LCD_ON_TIME'] = request.form.get("lcdInput")
        stat['TEMP_MES_INT'] = request.form.get("tempInput")
        stat['SENS_POW'] = int(bool(request.form.get("senspowInput")))
        stat['SLOW_REC_INTERVAL'] = request.form.get("slowrecInput")
        stat['GAIN'] = int(bool(request.form.get("gainInput")))
        stat['AUTO'] = int(bool(request.form.get("autoInput")))
        stat['LEN'] = request.form.get("lenInput")


        net = {}
        net['ETH_POW'] = int(bool(request.form.get("ethpowInput")))
        net['DSL_POW'] = int(bool(request.form.get("dslpowInput")))
        net['ETH_IP'] = request.form.get("ethipInput")
        net['ETH_MASK'] = request.form.get("ethmaskInput")
        net['ETH_GW'] = request.form.get("ethgwInput")

        time = {}
        time['SOURCE'] = request.form.get("sourceInput")
        time['NTP_IP'] = request.form.get("ntpipInput")
        time['NTP_PORT'] = request.form.get("ntpportInput")
        time['GPS_SLEEP_TIME'] = request.form.get("gpssleepInput")

        socket0 = {}
        socket0['SERVICE'] = request.form.get("service0Input")
        if int(socket0['SERVICE'])==5:
            socket0['SERVICE']=7
        socket0['PORT'] = request.form.get("port0Input")

        socket1 = {}
        socket1['SERVICE'] = request.form.get("service1Input")
        if int(socket1['SERVICE'])==5:
            socket1['SERVICE']=7
        socket1['PORT'] = request.form.get("port1Input")

        socket2 = {}
        socket2['SERVICE'] = request.form.get("service2Input")
        if int(socket2['SERVICE'])==5:
            socket2['SERVICE']=7
        socket2['PORT'] = request.form.get("port2Input")

        socket3 = {}
        socket3['SERVICE'] = request.form.get("service3Input")

        if int(socket3['SERVICE'])==5:
            socket3['SERVICE']=7
        socket3['PORT'] = request.form.get("port3Input")

        ch0 = {}
        ch0['NET'] = request.form.get("net0Input")
        ch0['STATION'] = request.form.get("station0Input")
        ch0['LOC'] = request.form.get("loc0Input")
        ch0['NAME'] = request.form.get("name0Input")
        ch0['TO_DISK'] = int(bool(request.form.get("todisk0Input")))
        ch0['TO_NET'] = int(bool(request.form.get("tonet0Input")))
        ch0['TO_DISP'] = int(bool(request.form.get("todisp0Input")))

        ch1 = {}
        ch1['NET'] = request.form.get("net1Input")
        ch1['STATION'] = request.form.get("station1Input")
        ch1['LOC'] = request.form.get("loc1Input")
        ch1['NAME'] = request.form.get("name1Input")
        ch1['TO_DISK'] = int(bool(request.form.get("todisk1Input")))
        ch1['TO_NET'] = int(bool(request.form.get("tonet1Input")))
        ch1['TO_DISP'] = int(bool(request.form.get("todisp1Input")))

        ch2 = {}
        ch2['NET'] = request.form.get("net2Input")
        ch2['STATION'] = request.form.get("station2Input")
        ch2['LOC'] = request.form.get("loc2Input")
        ch2['NAME'] = request.form.get("name2Input")
        ch2['TO_DISK'] = int(bool(request.form.get("todisk2Input")))
        ch2['TO_NET'] = int(bool(request.form.get("tonet2Input")))
        ch2['TO_DISP'] = int(bool(request.form.get("todisp2Input")))

        ch3 = {}
        ch3['NET'] = request.form.get("net3Input")
        ch3['STATION'] = request.form.get("station3Input")
        ch3['LOC'] = request.form.get("loc3Input")
        ch3['NAME'] = request.form.get("name3Input")
        ch3['TO_DISK'] = int(bool(request.form.get("todisk3Input")))
        ch3['TO_NET'] = int(bool(request.form.get("tonet3Input")))
        ch3['TO_DISP'] = int(bool(request.form.get("todisp3Input")))

        ch4 = {}
        ch4['NET'] = request.form.get("net4Input")
        ch4['STATION'] = request.form.get("station4Input")
        ch4['LOC'] = request.form.get("loc4Input")
        ch4['NAME'] = request.form.get("name4Input")
        ch4['TO_DISK'] = int(bool(request.form.get("todisk4Input")))
        ch4['TO_NET'] = int(bool(request.form.get("tonet4Input")))
        ch4['TO_DISP'] = int(bool(request.form.get("todisp4Input")))

        ch5 = {}
        ch5['NET'] = request.form.get("net5Input")
        ch5['STATION'] = request.form.get("station5Input")
        ch5['LOC'] = request.form.get("loc5Input")
        ch5['NAME'] = request.form.get("name5Input")
        ch5['TO_DISK'] = int(bool(request.form.get("todisk5Input")))
        ch5['TO_NET'] = int(bool(request.form.get("tonet5Input")))
        ch5['TO_DISP'] = int(bool(request.form.get("todisp5Input")))

        ch6 = {}
        try:
            ch6['NET'] = request.form.get("net6Input")
            ch6['STATION'] = request.form.get("station6Input")
            ch6['LOC'] = request.form.get("loc6Input")
            ch6['NAME'] = request.form.get("name6Input")
            ch6['TO_DISK'] = int(bool(request.form.get("todisk6Input")))
            ch6['TO_NET'] = int(bool(request.form.get("tonet6Input")))
            ch6['TO_DISP'] = int(bool(request.form.get("todisp6Input")))
        except:
            pass

        reboot['DAILY_REBOOT'] = int(bool(request.form.get("dailyrebootInput")))
        reboot['REBOOT_TIME'] = request.form.get("reboottimeInput")

        chooseSta = station
        new_inifile=configparser.ConfigParser()
        new_inifile['SYSTEM']=stat
        new_inifile['CH0']=ch0

        new_inifile['CH1'] = ch1
        new_inifile['CH2'] = ch2
        new_inifile['CH3'] = ch3
        new_inifile['CH4'] = ch4
        new_inifile['CH5'] = ch5
        try:
            yearFirm = int(getYearFirmware(net['ETH_IP']))
            LogAppend(f"year firm: {yearFirm}")
            if yearFirm>2022:
                LogAppend(f"ch6: {ch6}")
                new_inifile['CH6'] = ch6
        except Exception as e:
            LogAppend(f"Except with year firmware: {e}")
            return "Oops! Refresh and try again."
        new_inifile['TIME']=time
        new_inifile['NET']=net
        new_inifile['SOCKET0']=socket0
        new_inifile['SOCKET1'] = socket1
        new_inifile['SOCKET2'] = socket2
        new_inifile['SOCKET3'] = socket3
        new_inifile['REBOOT'] = reboot
        ver=len(flist)

        if int(bool(request.form.get("isSend")))==1:
            countTry = 5
            shutil.copy2(pth+station+"/seisview_imp.ini", pth+station+"/seisview_imp_v"+str(ver)+".ini")
            with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                new_inifile.write(file_object)

            with open(pth + station + "/seisview_imp.ini", "r") as file_object:
                text=file_object.read()
            text=text.replace(" ","").upper()

            with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                file_object.write(text)

            while countTry!=0:
                with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                    new_inifile.write(file_object)
                with open(pth + station + "/seisview_imp.ini", "r") as file_object:
                    text = file_object.read()
                text = text.replace(" ", "").upper()

                with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                    file_object.write(text)

                file_size = os.path.getsize(pth + station + "/seisview_imp.ini")
                emptyCount = 128 - file_size % 128
                with open(pth + station + "/seisview_imp.ini", "a") as f:
                    for i in range(emptyCount):
                        f.write("#")

                try:
                    client = tftpy.TftpClient(net['ETH_IP'], 69,options={"blksize":128})

                    try:
                        client.upload('seisview_imp.ini', f"{pth + station + '/seisview_imp.ini'}", timeout=30)
                    except:
                        pass
                    destination = pth + station + "/seisview_imp.ini"
                    url = f"http://{net['ETH_IP']}/seisview_imp.ini"
                    try:
                        urllib.request.urlretrieve(url, destination)
                    except:
                        pass
                    stat, time, net, socket0, socket1, socket2, socket3, ch0, ch1, ch2, ch3, ch4, ch5, ch6, reboot, readErr = readini(destination)

                    countTry = countTry - 1
                    #readErr=False

                    if readErr:
                        if countTry == 0:
                            with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                                new_inifile.write(file_object)
                            with open(pth + station + "/seisview_imp.ini", "r") as file_object:
                                text1 = file_object.readlines()
                            with open(pth+station+"/seisview_imp_v"+str(ver)+".ini", "r") as file_object:
                                text2 = file_object.readlines()
                            if text1 == text2:
                                os.remove(pth + station + "/seisview_imp_v" + str(ver) + ".ini")
                            return "Sorry! INI file is only partially downloaded."
                    else:
                        break
                except:
                    return "Sorry! INI file is not downloaded. Station is off-line."

            #cmd=f"tftp.exe -i -v {net['ETH_IP']} put {pth+station+'/seisview_imp.ini'}"
            #os.system(cmd)
            return redirect(f"/{chooseSta}/last")


        elif int(bool(request.form.get("isGet")))==1:
            LogAppend("start get")
            #shutil.copy2(pth + station + "/seisview_imp.ini", pth + station + "/seisview_imp_v" + str(ver) + ".ini")
            with open(pth + station + "/seisview_imp_v" + str(ver) + ".ini", "w") as file_object:
                new_inifile.write(file_object)

            with open(pth + station + "/seisview_imp.ini", "r") as file_object:
                text = file_object.read()
            text = text.replace(" ", "").upper()

            with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                file_object.write(text)

            try:
                #client = tftpy.TftpClient(net['ETH_IP'], 69)
                #client.download('seisview_imp.ini', f"{pth + station + '/seisview_imp.ini'}", timeout=30)
                #cmd = f"tftp.exe -i -v {net['ETH_IP']} get seisview_imp.ini"
                #os.system(cmd)
                #shutil.move("seisview_imp.ini",f"{pth + station + '/seisview_imp.ini'}")
                destination = pth + station + "/seisview_imp.ini"
                url = f"http://{net['ETH_IP']}/seisview_imp.ini"
                urllib.request.urlretrieve(url, destination)
                stat, time, net, socket0, socket1, socket2, socket3, ch0, ch1, ch2, ch3, ch4, ch5, ch6, reboot, readErr = readini(destination)
                #if readErr:
                    #shutil.copy2(pth + station + "/seisview_imp_v" + str(ver) + ".ini",pth + station + "/seisview_imp.ini")
                    #os.remove(pth + station + "/seisview_imp_v" + str(ver) + ".ini")
                    #return "Sorry! INI file is incorrect."
                return redirect(f"/{chooseSta}/last")
            except:
                return "Sorry! The station is off-line."

    return render_template('index.html', station=dirlist, chooseSta=chooseSta,chooseVersion=chooseVersion, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot, hasSta=True, haserr=False,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5,ch6=ch6, version_list=flist, statusCodes=statusCodes)



tmpl=os.listdir("templates")
with open("config.txt","r") as file:
    data = file.readlines()
    config_addr = data[0].strip()

for f in tmpl:
    # Read in the file
    with open("templates/"+f, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('192.168.35.94', config_addr)

    # Write the file out again
    with open("templates/"+f, 'w') as file:
        file.write(filedata)


def runApp():
    global app
    app.run(host='0.0.0.0', port=5081)

def CycleCreateDoc():
    pth = "./ini/"
    dirlist = os.listdir(pth)
    while True:
        try:
            CreateDocStatus(dirlist, False)
            time.sleep(10)
        except:
            pass
    return

pth="./ini/"
dirlist = os.listdir(pth)
CreateDocStatus(dirlist,True)

LogAppend("Start app")

p1 = threading.Thread(target=runApp, daemon=True)
p2 = threading.Thread(target=CycleCreateDoc, daemon=True)
p1.start()
p2.start()
p1.join()
p2.join()

#app.run(host='0.0.0.0', port=5081)