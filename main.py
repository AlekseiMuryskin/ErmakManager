import configparser
import os
from flask import Flask, request
from flask import render_template
from configparser import ConfigParser
import shutil
import asyncio
import requests

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
    reboot={}
    chooseSta = ""
    chooseVersion = ""
    flist={}
    return render_template('index.html',  station=dirlist, chooseSta=chooseSta,chooseVersion=chooseVersion, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, version_list=flist, statusCodes=statusCodes)

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
    stat['device_name']=config.get('SYSTEM','DEVICE_NAME')
    stat['samprate']=config.get('SYSTEM','SAMPRATE')
    stat['LCD_ON_TIME'] = config.get('SYSTEM', 'LCD_ON_TIME')
    stat['TEMP_MES_INT'] = config.get('SYSTEM', 'TEMP_MES_INT')
    stat['SENS_POW'] = config.get('SYSTEM', 'SENS_POW')
    stat['SLOW_REC_INTERVAL'] = config.get('SYSTEM', 'SLOW_REC_INTERVAL')
    stat['GAIN'] = config.get('SYSTEM', 'GAIN')
    stat['AUTO'] = int(config.get('SYSTEM', 'AUTO'))
    stat['LEN'] = config.get('SYSTEM', 'LEN')

    net={}
    net['ETH_POW']=int(config.get('NET','ETH_POW'))
    net['DSL_POW'] = int(config.get('NET', 'DSL_POW'))
    net['ETH_IP']=config.get('NET','ETH_IP')
    net['ETH_MASK'] = config.get('NET', 'ETH_MASK')
    net['ETH_GW'] = config.get('NET', 'ETH_GW')

    time={}
    time['SOURCE']=config.get('TIME','SOURCE')
    time['NTP_IP'] = config.get('TIME', 'NTP_IP')
    time['NTP_PORT'] = config.get('TIME', 'NTP_PORT')
    time['GPS_SLEEP_TIME'] = config.get('TIME', 'GPS_SLEEP_TIME')
    try:
        time['NTP_SERVER'] = config.get('TIME', 'NTP_SERVER')
    except:
        time['NTP_SERVER']=0

    socket0={}
    socket0['SERVICE']=config.get('SOCKET0','SERVICE')
    if int(socket0['SERVICE'])==7:
        socket0['SERVICE']=5
    socket0['PORT'] = config.get('SOCKET0', 'PORT')

    socket1 = {}
    socket1['SERVICE'] = config.get('SOCKET1', 'SERVICE')
    if int(socket1['SERVICE'])==7:
        socket1['SERVICE']=5
    socket1['PORT'] = config.get('SOCKET1', 'PORT')

    socket2 = {}
    socket2['SERVICE'] = config.get('SOCKET2', 'SERVICE')
    if int(socket2['SERVICE'])==7:
        socket2['SERVICE']=5
    socket2['PORT'] = config.get('SOCKET2', 'PORT')

    socket3 = {}
    socket3['SERVICE'] = config.get('SOCKET3', 'SERVICE')
    if int(socket3['SERVICE'])==7:
        socket3['SERVICE']=5
    socket3['PORT'] = config.get('SOCKET3', 'PORT')

    ch0={}
    ch0['NET']=config.get('CH0','NET')
    ch0['STATION'] = config.get('CH0', 'STATION')
    ch0['LOC'] = config.get('CH0', 'LOC')
    ch0['NAME'] = config.get('CH0', 'NAME')
    ch0['TO_DISK'] = int(config.get('CH0', 'TO_DISK'))
    ch0['TO_NET'] = int(config.get('CH0', 'TO_NET'))
    ch0['TO_DISP'] = int(config.get('CH0', 'TO_DISP'))

    ch1 = {}
    ch1['NET'] = config.get('CH1', 'NET')
    ch1['STATION'] = config.get('CH1', 'STATION')
    ch1['LOC'] = config.get('CH1', 'LOC')
    ch1['NAME'] = config.get('CH1', 'NAME')
    ch1['TO_DISK'] = int(config.get('CH1', 'TO_DISK'))
    ch1['TO_NET'] = int(config.get('CH1', 'TO_NET'))
    ch1['TO_DISP'] = int(config.get('CH1', 'TO_DISP'))

    ch2 = {}
    ch2['NET'] = config.get('CH2', 'NET')
    ch2['STATION'] = config.get('CH2', 'STATION')
    ch2['LOC'] = config.get('CH2', 'LOC')
    ch2['NAME'] = config.get('CH2', 'NAME')
    ch2['TO_DISK'] = int(config.get('CH2', 'TO_DISK'))
    ch2['TO_NET'] = int(config.get('CH2', 'TO_NET'))
    ch2['TO_DISP'] = int(config.get('CH2', 'TO_DISP'))

    ch3 = {}
    ch3['NET'] = config.get('CH3', 'NET')
    ch3['STATION'] = config.get('CH3', 'STATION')
    ch3['LOC'] = config.get('CH3', 'LOC')
    ch3['NAME'] = config.get('CH3', 'NAME')
    ch3['TO_DISK'] = int(config.get('CH3', 'TO_DISK'))
    ch3['TO_NET'] = int(config.get('CH3', 'TO_NET'))
    ch3['TO_DISP'] = int(config.get('CH3', 'TO_DISP'))

    ch4 = {}
    ch4['NET'] = config.get('CH4', 'NET')
    ch4['STATION'] = config.get('CH4', 'STATION')
    ch4['LOC'] = config.get('CH4', 'LOC')
    ch4['NAME'] = config.get('CH4', 'NAME')
    ch4['TO_DISK'] = int(config.get('CH4', 'TO_DISK'))
    ch4['TO_NET'] = int(config.get('CH4', 'TO_NET'))
    ch4['TO_DISP'] = int(config.get('CH4', 'TO_DISP'))

    ch5 = {}
    ch5['NET'] = config.get('CH5', 'NET')
    ch5['STATION'] = config.get('CH5', 'STATION')
    ch5['LOC'] = config.get('CH5', 'LOC')
    ch5['NAME'] = config.get('CH5', 'NAME')
    ch5['TO_DISK'] = int(config.get('CH5', 'TO_DISK'))
    ch5['TO_NET'] = int(config.get('CH5', 'TO_NET'))
    ch5['TO_DISP'] = int(config.get('CH5', 'TO_DISP'))

    reboot={}
    try:
        reboot['DAILY_REBOOT']=int(config.get('REBOOT', 'DAILY_REBOOT'))
        reboot['REBOOT_TIME'] = config.get('REBOOT', 'REBOOT_TIME')
    except:
        reboot['DAILY_REBOOT'] = 0
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
        stat['SENS_POW'] = request.form.get("senspowInput")
        stat['SLOW_REC_INTERVAL'] = request.form.get("slowrecInput")
        stat['GAIN'] = request.form.get("gainInput")
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
        time['NTP_SERVER'] = request.form.get("ntpserverInput")

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

        shutil.copy2(pth+station+"/seisview_imp.ini", pth+station+"/seisview_imp_v"+str(ver)+".ini")

        with open(pth+station+"/seisview_imp.ini", "w") as file_object:
            new_inifile.write(file_object)

        #cmd=f"tftp.exe -i -v {net['ETH_IP']} put {pth+station+'/seisview_imp.ini'}"
        #os.system(cmd)

        if int(socket0['SERVICE'])==7:
            socket0['SERVICE']=5
        if int(socket1['SERVICE'])==7:
            socket1['SERVICE']=5
        if int(socket2['SERVICE'])==7:
            socket2['SERVICE']=5
        if int(socket3['SERVICE'])==7:
            socket3['SERVICE']=5
        flist = os.listdir(pth + station + "/")
        flist = sorted([x.replace("seisview_imp", "last").replace(".ini", "").replace("last_","") for x in flist], key=len)
        flist=flist[::-1]
        return render_template('index.html', station=dirlist, chooseSta=chooseSta,chooseVersion=chooseVersion, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, version_list=flist, statusCodes=statusCodes)

    return render_template('index.html', station=dirlist, chooseSta=chooseSta,chooseVersion=chooseVersion, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3, reboot=reboot,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, version_list=flist, statusCodes=statusCodes)

app.run(host='0.0.0.0', port=81)