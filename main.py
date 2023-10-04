import configparser
import os
from flask import Flask, request
from flask import render_template
from configparser import ConfigParser
import shutil
import asyncio
import requests
import urllib.request

app=Flask(__name__)

def getStatusCode(dirlist):
    pth = "./ini/"
    statusCodes={}
    for sta in dirlist:
        fname = pth + sta+ "/seisview_imp.ini"
        config = ConfigParser()
        config.read(fname)
        #statusCodes[sta]=f"http://{config.get('NET', 'ETH_IP')}/status"
        try:
            r=requests.get(f"http://{config.get('NET', 'ETH_IP')}/status", timeout=0.1).status_code == 200
        except:
            r=False
        if r:
            statusCodes[sta] = "green"
        else:
            statusCodes[sta] = "green"
    return statusCodes

@app.route('/')
def index():
    pth="./ini/"
    dirlist=os.listdir(pth)
    statusCodes=getStatusCode(dirlist)
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
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5,ch6=ch6, version_list=flist, statusCodes=statusCodes)

@app.route('/newsta')
def newStation():
    pth="./ini/"
    dirlist=os.listdir(pth)
    statusCodes=getStatusCode(dirlist)
    chooseSta = ""
    return render_template('newsta.html',  station=dirlist, statusCodes=statusCodes, chooseSta=chooseSta)



@app.route('/<station>/<version>', methods=["GET","POST"])
def stationProp(station,version):

    pth = "./ini/"
    dirlist = os.listdir(pth)
    config = ConfigParser()
    if version!="last":
        fname=pth+station+"/seisview_imp_"+version+".ini"
    else:
        fname=pth+station+"/seisview_imp.ini"

    config.read(fname)
    flist=os.listdir(pth+station+"/")

    flist=sorted([x.replace("seisview_imp","last").replace(".ini","").replace("last_","") for x in flist], key=len)
    flist=flist[::-1]
    stat= {}
    try:
        stat['device_name']=config.get('SYSTEM','DEVICE_NAME')
    except:
        stat['device_name'] = "LAB PTS"
    try:
        stat['samprate']=config.get('SYSTEM','SAMPRATE')
    except:
        stat['samprate'] = "500"
    try:
        stat['LCD_ON_TIME'] = config.get('SYSTEM', 'LCD_ON_TIME')
    except:
        stat['LCD_ON_TIME'] = "255"
    try:
        stat['TEMP_MES_INT'] = config.get('SYSTEM', 'TEMP_MES_INT')
    except:
        stat['TEMP_MES_INT'] = "3600"
    try:
        stat['SENS_POW'] = int(config.get('SYSTEM', 'SENS_POW'))
    except:
        stat['SENS_POW'] = 0
    try:
        stat['SLOW_REC_INTERVAL'] = config.get('SYSTEM', 'SLOW_REC_INTERVAL')
    except:
        stat['SLOW_REC_INTERVAL'] = 0
    try:
        stat['GAIN'] = int(config.get('SYSTEM', 'GAIN'))
    except:
        stat['GAIN'] = 1
    try:
        stat['AUTO'] = int(config.get('SYSTEM', 'AUTO'))
    except:
        stat['AUTO'] = 1
    try:
        stat['LEN'] = config.get('SYSTEM', 'LEN')
    except:
        stat['LEN'] = "3600"

    net={}
    try:
        net['ETH_POW']=int(config.get('NET','ETH_POW'))
    except:
        net['ETH_POW'] = 0
    try:
        net['DSL_POW'] = int(config.get('NET', 'DSL_POW'))
    except:
        net['DSL_POW'] = 1
    try:
        net['ETH_IP']=config.get('NET','ETH_IP')
    except:
        net['ETH_IP'] = "192.168.192.168"
    try:
        net['ETH_MASK'] = config.get('NET', 'ETH_MASK')
    except:
        net['ETH_MASK'] = "255.255.255.0"
    try:
        net['ETH_GW'] = config.get('NET', 'ETH_GW')
    except:
        net['ETH_GW'] = "192.168.192.1"

    time={}
    try:
        time['SOURCE']=config.get('TIME','SOURCE')
    except:
        time['SOURCE'] = "3"
    try:
        time['NTP_IP'] = config.get('TIME', 'NTP_IP')
    except:
        time['NTP_IP'] = "192.168.192.1"
    try:
        time['NTP_PORT'] = config.get('TIME', 'NTP_PORT')
    except:
        time['NTP_PORT'] = "123"
    try:
        time['GPS_SLEEP_TIME'] = config.get('TIME', 'GPS_SLEEP_TIME')
    except:
        time['GPS_SLEEP_TIME'] = "0"

    socket0={}
    try:
        socket0['SERVICE']=config.get('SOCKET0','SERVICE')
    except:
        socket0['SERVICE'] = "1"
    if int(socket0['SERVICE'])==7:
        socket0['SERVICE']=5
    try:
        socket0['PORT'] = config.get('SOCKET0', 'PORT')
    except:
        socket0['PORT'] = "80"

    socket1 = {}
    try:
        socket1['SERVICE'] = config.get('SOCKET1', 'SERVICE')
    except:
        socket1['SERVICE'] = "1"
    if int(socket1['SERVICE'])==7:
        socket1['SERVICE']=5
    try:
        socket1['PORT'] = config.get('SOCKET1', 'PORT')
    except:
        socket1['PORT'] = "80"

    socket2 = {}
    try:
        socket2['SERVICE'] = config.get('SOCKET2', 'SERVICE')
    except:
        socket2['SERVICE'] = "1"
    if int(socket2['SERVICE'])==7:
        socket2['SERVICE']=5
    try:
        socket2['PORT'] = config.get('SOCKET2', 'PORT')
    except:
        socket2['PORT'] = "80"

    socket3 = {}
    try:
        socket3['SERVICE'] = config.get('SOCKET3', 'SERVICE')
    except:
        socket3['SERVICE'] = "1"
    if int(socket3['SERVICE'])==7:
        socket3['SERVICE']=5
    try:
        socket3['PORT'] = config.get('SOCKET3', 'PORT')
    except:
        socket3['PORT'] = "80"

    ch0={}
    try:
        ch0['NET']=config.get('CH0','NET')
    except:
        ch0['NET'] = "PR"
    try:
        ch0['STATION'] = config.get('CH0', 'STATION')
    except:
        ch0['STATION'] = "PTSLB"
    try:
        ch0['LOC'] = config.get('CH0', 'LOC')
    except:
        ch0['LOC'] = "00"
    try:
        ch0['NAME'] = config.get('CH0', 'NAME')
    except:
        ch0['NAME'] = "CH0"
    try:
        ch0['TO_DISK'] = int(config.get('CH0', 'TO_DISK'))
    except:
        ch0['TO_DISK'] = 1
    try:
        ch0['TO_NET'] = int(config.get('CH0', 'TO_NET'))
    except:
        ch0['TO_NET'] = 1
    try:
        ch0['TO_DISP'] = int(config.get('CH0', 'TO_DISP'))
    except:
        ch0['TO_DISP'] = 1

    ch1 = {}
    try:
        ch1['NET'] = config.get('CH1', 'NET')
    except:
        ch1['NET'] = "PR"
    try:
        ch1['STATION'] = config.get('CH1', 'STATION')
    except:
        ch1['STATION'] = "PTSLB"
    try:
        ch1['LOC'] = config.get('CH1', 'LOC')
    except:
        ch1['LOC'] = "00"
    try:
        ch1['NAME'] = config.get('CH1', 'NAME')
    except:
        ch1['NAME'] = "CH1"
    try:
        ch1['TO_DISK'] = int(config.get('CH1', 'TO_DISK'))
    except:
        ch1['TO_DISK'] = 1
    try:
        ch1['TO_NET'] = int(config.get('CH1', 'TO_NET'))
    except:
        ch1['TO_NET'] = 1
    try:
        ch1['TO_DISP'] = int(config.get('CH1', 'TO_DISP'))
    except:
        ch1['TO_DISP'] = 1

    ch2 = {}
    try:
        ch2['NET'] = config.get('CH2', 'NET')
    except:
        ch2['NET'] = "PR"
    try:
        ch2['STATION'] = config.get('CH2', 'STATION')
    except:
        ch2['STATION'] = "PTSLB"
    try:
        ch2['LOC'] = config.get('CH2', 'LOC')
    except:
        ch2['LOC'] = "00"
    try:
        ch2['NAME'] = config.get('CH2', 'NAME')
    except:
        ch2['NAME'] = "CH2"
    try:
        ch2['TO_DISK'] = int(config.get('CH2', 'TO_DISK'))
    except:
        ch2['TO_DISK'] = 1
    try:
        ch2['TO_NET'] = int(config.get('CH2', 'TO_NET'))
    except:
        ch2['TO_NET'] = 1
    try:
        ch2['TO_DISP'] = int(config.get('CH2', 'TO_DISP'))
    except:
        ch2['TO_DISP'] = 1

    ch3 = {}
    try:
        ch3['NET'] = config.get('CH3', 'NET')
    except:
        ch3['NET'] = "PR"
    try:
        ch3['STATION'] = config.get('CH3', 'STATION')
    except:
        ch3['STATION'] = "PTSLB"
    try:
        ch3['LOC'] = config.get('CH3', 'LOC')
    except:
        ch3['LOC'] = "00"
    try:
        ch3['NAME'] = config.get('CH3', 'NAME')
    except:
        ch3['NAME'] = "CH3"
    try:
        ch3['TO_DISK'] = int(config.get('CH3', 'TO_DISK'))
    except:
        ch3['TO_DISK'] = 1
    try:
        ch3['TO_NET'] = int(config.get('CH3', 'TO_NET'))
    except:
        ch3['TO_NET'] = 1
    try:
        ch3['TO_DISP'] = int(config.get('CH3', 'TO_DISP'))
    except:
        ch3['TO_DISP'] = 1

    ch4 = {}
    try:
        ch4['NET'] = config.get('CH4', 'NET')
    except:
        ch4['NET'] = "PR"
    try:
        ch4['STATION'] = config.get('CH4', 'STATION')
    except:
        ch4['STATION'] = "PTSLB"
    try:
        ch4['LOC'] = config.get('CH4', 'LOC')
    except:
        ch4['LOC'] = "00"
    try:
        ch4['NAME'] = config.get('CH4', 'NAME')
    except:
        ch4['NAME'] = "CH4"
    try:
        ch4['TO_DISK'] = int(config.get('CH4', 'TO_DISK'))
    except:
        ch4['TO_DISK'] = 1
    try:
        ch4['TO_NET'] = int(config.get('CH4', 'TO_NET'))
    except:
        ch4['TO_NET'] = 1
    try:
        ch4['TO_DISP'] = int(config.get('CH4', 'TO_DISP'))
    except:
        ch4['TO_DISP'] = 1

    ch5 = {}
    try:
        ch5['NET'] = config.get('CH5', 'NET')
    except:
        ch5['NET'] = "PR"
    try:
        ch5['STATION'] = config.get('CH5', 'STATION')
    except:
        ch5['STATION'] = "PTSLB"
    try:
        ch5['LOC'] = config.get('CH5', 'LOC')
    except:
        ch5['LOC'] = "00"
    try:
        ch5['NAME'] = config.get('CH5', 'NAME')
    except:
        ch5['NAME'] = "CH5"
    try:
        ch5['TO_DISK'] = int(config.get('CH5', 'TO_DISK'))
    except:
        ch5['TO_DISK'] = 1
    try:
        ch5['TO_NET'] = int(config.get('CH5', 'TO_NET'))
    except:
        ch5['TO_NET'] = 1
    try:
        ch5['TO_DISP'] = int(config.get('CH5', 'TO_DISP'))
    except:
        ch5['TO_DISP'] = 1

    ch6 = {}
    try:
        ch6['NET'] = config.get('CH6', 'NET')
    except:
        ch6['NET'] = "PR"
    try:
        ch6['STATION'] = config.get('CH6', 'STATION')
    except:
        ch6['STATION'] = "PTSLB"
    try:
        ch6['LOC'] = config.get('CH6', 'LOC')
    except:
        ch6['LOC'] = "--"
    try:
        ch6['NAME'] = config.get('CH6', 'NAME')
    except:
        ch6['NAME'] = "LOG"
    try:
        ch6['TO_DISK'] = int(config.get('CH6', 'TO_DISK'))
    except:
        ch6['TO_DISK'] = 1
    try:
        ch6['TO_NET'] = int(config.get('CH6', 'TO_NET'))
    except:
        ch6['TO_NET'] = 1
    try:
        ch6['TO_DISP'] = int(config.get('CH6', 'TO_DISP'))
    except:
        ch6['TO_DISP'] = 1

    reboot={}
    try:
        reboot['DAILY_REBOOT']=int(config.get('REBOOT', 'DAILY_REBOOT'))
    except:
        reboot['DAILY_REBOOT'] = 0
    try:
        reboot['REBOOT_TIME'] = config.get('REBOOT', 'REBOOT_TIME')
    except:
        reboot['REBOOT_TIME'] = "00:00"

    chooseSta=station
    chooseVersion = version
    statusCodes = getStatusCode(dirlist)
    if request.method=="POST":
        pth = "./ini/"
        dirlist = os.listdir(pth)
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
        new_inifile['TIME']=time
        new_inifile['NET']=net
        new_inifile['SOCKET0']=socket0
        new_inifile['SOCKET1'] = socket1
        new_inifile['SOCKET2'] = socket2
        new_inifile['SOCKET3'] = socket3
        new_inifile['REBOOT'] = socket3
        ver=len(flist)

        if int(bool(request.form.get("isSend")))==1:
            shutil.copy2(pth+station+"/seisview_imp.ini", pth+station+"/seisview_imp_v"+str(ver)+".ini")
            with open(pth + station + "/seisview_imp.ini", "w") as file_object:
                new_inifile.write(file_object)

            #cmd=f"tftp.exe -i -v {net['ETH_IP']} put {pth+station+'/seisview_imp.ini'}"
            #os.system(cmd)

            if int(socket0['SERVICE']) == 7:
                socket0['SERVICE'] = 5
            if int(socket1['SERVICE']) == 7:
                socket1['SERVICE'] = 5
            if int(socket2['SERVICE']) == 7:
                socket2['SERVICE'] = 5
            if int(socket3['SERVICE']) == 7:
                socket3['SERVICE'] = 5
            flist = os.listdir(pth + station + "/")
            flist = sorted([x.replace("seisview_imp", "last").replace(".ini", "").replace("last_", "") for x in flist],
                           key=len)
            flist = flist[::-1]
            return render_template('index.html', station=dirlist, chooseSta=chooseSta, chooseVersion=chooseVersion,
                                   stat=stat, net=net, time=time,
                                   soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                                   ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, ch6=ch6, version_list=flist,
                                   statusCodes=statusCodes)
        elif int(bool(request.form.get("isAdd")))==1:
            return request.form.get("newStationIp")

        elif int(bool(request.form.get("isDelete")))==1:
            pth = "./ini/"
            shutil.rmtree(pth + station)
            dirlist = os.listdir(pth)
            statusCodes = getStatusCode(dirlist)
            stat = {}
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
            reboot = {}
            chooseSta = ""
            chooseVersion = ""
            flist = {}
            return render_template('index.html', station=dirlist, chooseSta=chooseSta, chooseVersion=chooseVersion,
                                   stat=stat, net=net, time=time,
                                   soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                                   ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, ch6=ch6, version_list=flist,
                                   statusCodes=statusCodes)


        else:
            #shutil.copy2(pth + station + "/seisview_imp.ini", pth + station + "/seisview_imp_v" + str(ver) + ".ini")
            with open(pth + station + "/seisview_imp_v" + str(ver) + ".ini", "w") as file_object:
                new_inifile.write(file_object)
            try:
                cmd = f"tftp.exe -i -v {net['ETH_IP']} get {pth + station + '/seisview_imp.ini'}"
                os.system(cmd)
                #destination = pth + station + "/seisview_imp.ini"
                #url = f"http://{net['ETH_IP']}/seisview_imp.ini"
                #urllib.request.urlretrieve(url, destination)
                pth = "./ini/"
                dirlist = os.listdir(pth)
                config = ConfigParser()
                if version != "last":
                    fname = pth + station + "/seisview_imp_" + version + ".ini"
                else:
                    fname = pth + station + "/seisview_imp.ini"

                config.read(fname)
                flist = os.listdir(pth + station + "/")

                flist = sorted([x.replace("seisview_imp", "last").replace(".ini", "").replace("last_", "") for x in flist],
                               key=len)
                flist = flist[::-1]
                stat = {}
                try:
                    stat['device_name'] = config.get('SYSTEM', 'DEVICE_NAME')
                except:
                    stat['device_name'] = "LAB PTS"
                try:
                    stat['samprate'] = config.get('SYSTEM', 'SAMPRATE')
                except:
                    stat['samprate'] = "500"
                try:
                    stat['LCD_ON_TIME'] = config.get('SYSTEM', 'LCD_ON_TIME')
                except:
                    stat['LCD_ON_TIME'] = "255"
                try:
                    stat['TEMP_MES_INT'] = config.get('SYSTEM', 'TEMP_MES_INT')
                except:
                    stat['TEMP_MES_INT'] = "3600"
                try:
                    stat['SENS_POW'] = int(config.get('SYSTEM', 'SENS_POW'))
                except:
                    stat['SENS_POW'] = 0
                try:
                    stat['SLOW_REC_INTERVAL'] = config.get('SYSTEM', 'SLOW_REC_INTERVAL')
                except:
                    stat['SLOW_REC_INTERVAL'] = 0
                try:
                    stat['GAIN'] = int(config.get('SYSTEM', 'GAIN'))
                except:
                    stat['GAIN'] = 1
                try:
                    stat['AUTO'] = int(config.get('SYSTEM', 'AUTO'))
                except:
                    stat['AUTO'] = 1
                try:
                    stat['LEN'] = config.get('SYSTEM', 'LEN')
                except:
                    stat['LEN'] = "3600"

                net = {}
                try:
                    net['ETH_POW'] = int(config.get('NET', 'ETH_POW'))
                except:
                    net['ETH_POW'] = 0
                try:
                    net['DSL_POW'] = int(config.get('NET', 'DSL_POW'))
                except:
                    net['DSL_POW'] = 1
                try:
                    net['ETH_IP'] = config.get('NET', 'ETH_IP')
                except:
                    net['ETH_IP'] = "192.168.192.168"
                try:
                    net['ETH_MASK'] = config.get('NET', 'ETH_MASK')
                except:
                    net['ETH_MASK'] = "255.255.255.0"
                try:
                    net['ETH_GW'] = config.get('NET', 'ETH_GW')
                except:
                    net['ETH_GW'] = "192.168.192.1"

                time = {}
                try:
                    time['SOURCE'] = config.get('TIME', 'SOURCE')
                except:
                    time['SOURCE'] = "3"
                try:
                    time['NTP_IP'] = config.get('TIME', 'NTP_IP')
                except:
                    time['NTP_IP'] = "192.168.192.1"
                try:
                    time['NTP_PORT'] = config.get('TIME', 'NTP_PORT')
                except:
                    time['NTP_PORT'] = "123"
                try:
                    time['GPS_SLEEP_TIME'] = config.get('TIME', 'GPS_SLEEP_TIME')
                except:
                    time['GPS_SLEEP_TIME'] = "0"

                socket0 = {}
                try:
                    socket0['SERVICE'] = config.get('SOCKET0', 'SERVICE')
                except:
                    socket0['SERVICE'] = "1"
                if int(socket0['SERVICE']) == 7:
                    socket0['SERVICE'] = 5
                try:
                    socket0['PORT'] = config.get('SOCKET0', 'PORT')
                except:
                    socket0['PORT'] = "80"

                socket1 = {}
                try:
                    socket1['SERVICE'] = config.get('SOCKET1', 'SERVICE')
                except:
                    socket1['SERVICE'] = "1"
                if int(socket1['SERVICE']) == 7:
                    socket1['SERVICE'] = 5
                try:
                    socket1['PORT'] = config.get('SOCKET1', 'PORT')
                except:
                    socket1['PORT'] = "80"

                socket2 = {}
                try:
                    socket2['SERVICE'] = config.get('SOCKET2', 'SERVICE')
                except:
                    socket2['SERVICE'] = "1"
                if int(socket2['SERVICE']) == 7:
                    socket2['SERVICE'] = 5
                try:
                    socket2['PORT'] = config.get('SOCKET2', 'PORT')
                except:
                    socket2['PORT'] = "80"

                socket3 = {}
                try:
                    socket3['SERVICE'] = config.get('SOCKET3', 'SERVICE')
                except:
                    socket3['SERVICE'] = "1"
                if int(socket3['SERVICE']) == 7:
                    socket3['SERVICE'] = 5
                try:
                    socket3['PORT'] = config.get('SOCKET3', 'PORT')
                except:
                    socket3['PORT'] = "80"

                ch0 = {}
                try:
                    ch0['NET'] = config.get('CH0', 'NET')
                except:
                    ch0['NET'] = "PR"
                try:
                    ch0['STATION'] = config.get('CH0', 'STATION')
                except:
                    ch0['STATION'] = "PTSLB"
                try:
                    ch0['LOC'] = config.get('CH0', 'LOC')
                except:
                    ch0['LOC'] = "00"
                try:
                    ch0['NAME'] = config.get('CH0', 'NAME')
                except:
                    ch0['NAME'] = "CH0"
                try:
                    ch0['TO_DISK'] = int(config.get('CH0', 'TO_DISK'))
                except:
                    ch0['TO_DISK'] = 1
                try:
                    ch0['TO_NET'] = int(config.get('CH0', 'TO_NET'))
                except:
                    ch0['TO_NET'] = 1
                try:
                    ch0['TO_DISP'] = int(config.get('CH0', 'TO_DISP'))
                except:
                    ch0['TO_DISP'] = 1

                ch1 = {}
                try:
                    ch1['NET'] = config.get('CH1', 'NET')
                except:
                    ch1['NET'] = "PR"
                try:
                    ch1['STATION'] = config.get('CH1', 'STATION')
                except:
                    ch1['STATION'] = "PTSLB"
                try:
                    ch1['LOC'] = config.get('CH1', 'LOC')
                except:
                    ch1['LOC'] = "00"
                try:
                    ch1['NAME'] = config.get('CH1', 'NAME')
                except:
                    ch1['NAME'] = "CH1"
                try:
                    ch1['TO_DISK'] = int(config.get('CH1', 'TO_DISK'))
                except:
                    ch1['TO_DISK'] = 1
                try:
                    ch1['TO_NET'] = int(config.get('CH1', 'TO_NET'))
                except:
                    ch1['TO_NET'] = 1
                try:
                    ch1['TO_DISP'] = int(config.get('CH1', 'TO_DISP'))
                except:
                    ch1['TO_DISP'] = 1

                ch2 = {}
                try:
                    ch2['NET'] = config.get('CH2', 'NET')
                except:
                    ch2['NET'] = "PR"
                try:
                    ch2['STATION'] = config.get('CH2', 'STATION')
                except:
                    ch2['STATION'] = "PTSLB"
                try:
                    ch2['LOC'] = config.get('CH2', 'LOC')
                except:
                    ch2['LOC'] = "00"
                try:
                    ch2['NAME'] = config.get('CH2', 'NAME')
                except:
                    ch2['NAME'] = "CH2"
                try:
                    ch2['TO_DISK'] = int(config.get('CH2', 'TO_DISK'))
                except:
                    ch2['TO_DISK'] = 1
                try:
                    ch2['TO_NET'] = int(config.get('CH2', 'TO_NET'))
                except:
                    ch2['TO_NET'] = 1
                try:
                    ch2['TO_DISP'] = int(config.get('CH2', 'TO_DISP'))
                except:
                    ch2['TO_DISP'] = 1

                ch3 = {}
                try:
                    ch3['NET'] = config.get('CH3', 'NET')
                except:
                    ch3['NET'] = "PR"
                try:
                    ch3['STATION'] = config.get('CH3', 'STATION')
                except:
                    ch3['STATION'] = "PTSLB"
                try:
                    ch3['LOC'] = config.get('CH3', 'LOC')
                except:
                    ch3['LOC'] = "00"
                try:
                    ch3['NAME'] = config.get('CH3', 'NAME')
                except:
                    ch3['NAME'] = "CH3"
                try:
                    ch3['TO_DISK'] = int(config.get('CH3', 'TO_DISK'))
                except:
                    ch3['TO_DISK'] = 1
                try:
                    ch3['TO_NET'] = int(config.get('CH3', 'TO_NET'))
                except:
                    ch3['TO_NET'] = 1
                try:
                    ch3['TO_DISP'] = int(config.get('CH3', 'TO_DISP'))
                except:
                    ch3['TO_DISP'] = 1

                ch4 = {}
                try:
                    ch4['NET'] = config.get('CH4', 'NET')
                except:
                    ch4['NET'] = "PR"
                try:
                    ch4['STATION'] = config.get('CH4', 'STATION')
                except:
                    ch4['STATION'] = "PTSLB"
                try:
                    ch4['LOC'] = config.get('CH4', 'LOC')
                except:
                    ch4['LOC'] = "00"
                try:
                    ch4['NAME'] = config.get('CH4', 'NAME')
                except:
                    ch4['NAME'] = "CH4"
                try:
                    ch4['TO_DISK'] = int(config.get('CH4', 'TO_DISK'))
                except:
                    ch4['TO_DISK'] = 1
                try:
                    ch4['TO_NET'] = int(config.get('CH4', 'TO_NET'))
                except:
                    ch4['TO_NET'] = 1
                try:
                    ch4['TO_DISP'] = int(config.get('CH4', 'TO_DISP'))
                except:
                    ch4['TO_DISP'] = 1

                ch5 = {}
                try:
                    ch5['NET'] = config.get('CH5', 'NET')
                except:
                    ch5['NET'] = "PR"
                try:
                    ch5['STATION'] = config.get('CH5', 'STATION')
                except:
                    ch5['STATION'] = "PTSLB"
                try:
                    ch5['LOC'] = config.get('CH5', 'LOC')
                except:
                    ch5['LOC'] = "00"
                try:
                    ch5['NAME'] = config.get('CH5', 'NAME')
                except:
                    ch5['NAME'] = "CH5"
                try:
                    ch5['TO_DISK'] = int(config.get('CH5', 'TO_DISK'))
                except:
                    ch5['TO_DISK'] = 1
                try:
                    ch5['TO_NET'] = int(config.get('CH5', 'TO_NET'))
                except:
                    ch5['TO_NET'] = 1
                try:
                    ch5['TO_DISP'] = int(config.get('CH5', 'TO_DISP'))
                except:
                    ch5['TO_DISP'] = 1

                ch6 = {}
                try:
                    ch6['NET'] = config.get('CH6', 'NET')
                except:
                    ch6['NET'] = "PR"
                try:
                    ch6['STATION'] = config.get('CH6', 'STATION')
                except:
                    ch6['STATION'] = "PTSLB"
                try:
                    ch6['LOC'] = config.get('CH6', 'LOC')
                except:
                    ch6['LOC'] = "--"
                try:
                    ch6['NAME'] = config.get('CH6', 'NAME')
                except:
                    ch6['NAME'] = "LOG"
                try:
                    ch6['TO_DISK'] = int(config.get('CH6', 'TO_DISK'))
                except:
                    ch6['TO_DISK'] = 1
                try:
                    ch6['TO_NET'] = int(config.get('CH6', 'TO_NET'))
                except:
                    ch6['TO_NET'] = 1
                try:
                    ch6['TO_DISP'] = int(config.get('CH6', 'TO_DISP'))
                except:
                    ch6['TO_DISP'] = 1

                reboot = {}
                try:
                    reboot['DAILY_REBOOT'] = int(config.get('REBOOT', 'DAILY_REBOOT'))
                except:
                    reboot['DAILY_REBOOT'] = 0
                try:
                    reboot['REBOOT_TIME'] = config.get('REBOOT', 'REBOOT_TIME')
                except:
                    reboot['REBOOT_TIME'] = "00:00"

                chooseSta = station
                chooseVersion = version
                return render_template('index.html', station=dirlist, chooseSta=chooseSta, chooseVersion=chooseVersion,
                                       stat=stat, net=net, time=time,
                                       soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                                       ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, ch6=ch6, version_list=flist,
                                       statusCodes=statusCodes)
            except:
                return "Sorry! The station is off-line."

    return render_template('index.html', station=dirlist, chooseSta=chooseSta,chooseVersion=chooseVersion, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5,ch6=ch6, version_list=flist, statusCodes=statusCodes)



app.run(host='0.0.0.0', port=81)