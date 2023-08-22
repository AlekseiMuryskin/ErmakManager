import os
from flask import Flask
from flask import render_template
from configparser import ConfigParser

app=Flask(__name__)

@app.route('/')
def index():
    pth="./ini/"
    dirlist=os.listdir(pth)
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
    chooseSta = ""
    flist={}
    return render_template('index.html',  station=dirlist, chooseSta=chooseSta, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, version_list=flist)

@app.route('/<station>')
def stationProp(station):
    pth = "./ini/"
    dirlist = os.listdir(pth)
    config = ConfigParser()
    fname=pth+station+"/seisview_imp.ini"
    config.read(fname)
    flist=os.listdir(pth+station+"/")
    stat= {}
    stat['device_name']=config.get('SYSTEM','DEVICE_NAME')
    stat['samprate']=config.get('SYSTEM','SAMPRATE')
    stat['LCD_ON_TIME'] = config.get('SYSTEM', 'LCD_ON_TIME')
    stat['TEMP_MES_INT'] = config.get('SYSTEM', 'TEMP_MES_INT')
    stat['SENS_POW'] = config.get('SYSTEM', 'SENS_POW')
    stat['SLOW_REC_INTERVAL'] = config.get('SYSTEM', 'SLOW_REC_INTERVAL')
    stat['GAIN'] = config.get('SYSTEM', 'GAIN')
    stat['AUTO'] = bool(int(config.get('SYSTEM', 'AUTO')))
    stat['LEN'] = config.get('SYSTEM', 'LEN')

    net={}
    net['ETH_POW']=bool(int(config.get('NET','ETH_POW')))
    net['DSL_POW'] = bool(int(config.get('NET', 'DSL_POW')))
    net['ETH_IP']=config.get('NET','ETH_IP')
    net['ETH_MASK'] = config.get('NET', 'ETH_MASK')
    net['ETH_GW'] = config.get('NET', 'ETH_GW')

    time={}
    time['SOURCE']=config.get('TIME','SOURCE')
    time['NTP_IP'] = config.get('TIME', 'NTP_IP')
    time['NTP_PORT'] = config.get('TIME', 'NTP_PORT')
    time['GPS_SLEEP_TIME'] = config.get('TIME', 'GPS_SLEEP_TIME')
    time['NTP_SERVER'] = config.get('TIME', 'NTP_SERVER')

    socket0={}
    socket0['SERVICE']=config.get('SOCKET0','SERVICE')
    socket0['PORT'] = config.get('SOCKET0', 'PORT')

    socket1 = {}
    socket1['SERVICE'] = config.get('SOCKET1', 'SERVICE')
    socket1['PORT'] = config.get('SOCKET1', 'PORT')

    socket2 = {}
    socket2['SERVICE'] = config.get('SOCKET2', 'SERVICE')
    socket2['PORT'] = config.get('SOCKET2', 'PORT')

    socket3 = {}
    socket3['SERVICE'] = config.get('SOCKET3', 'SERVICE')
    socket3['PORT'] = config.get('SOCKET3', 'PORT')

    ch0={}
    ch0['NET']=config.get('CH0','NET')
    ch0['STATION'] = config.get('CH0', 'STATION')
    ch0['LOC'] = config.get('CH0', 'LOC')
    ch0['NAME'] = config.get('CH0', 'NAME')
    ch0['TO_DISK'] = bool(int(config.get('CH0', 'TO_DISK')))
    ch0['TO_NET'] = bool(int(config.get('CH0', 'TO_NET')))
    ch0['TO_DISP'] = bool(int(config.get('CH0', 'TO_DISP')))

    ch1 = {}
    ch1['NET'] = config.get('CH1', 'NET')
    ch1['STATION'] = config.get('CH1', 'STATION')
    ch1['LOC'] = config.get('CH1', 'LOC')
    ch1['NAME'] = config.get('CH1', 'NAME')
    ch1['TO_DISK'] = bool(int(config.get('CH1', 'TO_DISK')))
    ch1['TO_NET'] = bool(int(config.get('CH1', 'TO_NET')))
    ch1['TO_DISP'] = bool(int(config.get('CH1', 'TO_DISP')))

    ch2 = {}
    ch2['NET'] = config.get('CH2', 'NET')
    ch2['STATION'] = config.get('CH2', 'STATION')
    ch2['LOC'] = config.get('CH2', 'LOC')
    ch2['NAME'] = config.get('CH2', 'NAME')
    ch2['TO_DISK'] = bool(int(config.get('CH2', 'TO_DISK')))
    ch2['TO_NET'] = bool(int(config.get('CH2', 'TO_NET')))
    ch2['TO_DISP'] = bool(int(config.get('CH2', 'TO_DISP')))

    ch3 = {}
    ch3['NET'] = config.get('CH3', 'NET')
    ch3['STATION'] = config.get('CH3', 'STATION')
    ch3['LOC'] = config.get('CH3', 'LOC')
    ch3['NAME'] = config.get('CH3', 'NAME')
    ch3['TO_DISK'] = bool(int(config.get('CH3', 'TO_DISK')))
    ch3['TO_NET'] = bool(int(config.get('CH3', 'TO_NET')))
    ch3['TO_DISP'] = bool(int(config.get('CH3', 'TO_DISP')))

    ch4 = {}
    ch4['NET'] = config.get('CH4', 'NET')
    ch4['STATION'] = config.get('CH4', 'STATION')
    ch4['LOC'] = config.get('CH4', 'LOC')
    ch4['NAME'] = config.get('CH4', 'NAME')
    ch4['TO_DISK'] = bool(int(config.get('CH4', 'TO_DISK')))
    ch4['TO_NET'] = bool(int(config.get('CH4', 'TO_NET')))
    ch4['TO_DISP'] = bool(int(config.get('CH4', 'TO_DISP')))

    ch5 = {}
    ch5['NET'] = config.get('CH5', 'NET')
    ch5['STATION'] = config.get('CH5', 'STATION')
    ch5['LOC'] = config.get('CH5', 'LOC')
    ch5['NAME'] = config.get('CH5', 'NAME')
    ch5['TO_DISK'] = bool(int(config.get('CH5', 'TO_DISK')))
    ch5['TO_NET'] = bool(int(config.get('CH5', 'TO_NET')))
    ch5['TO_DISP'] = bool(int(config.get('CH5', 'TO_DISP')))
    chooseSta=station
    return render_template('index.html', station=dirlist, chooseSta=chooseSta, stat=stat, net=net, time=time,
                           soc0=socket0, soc1=socket1, soc2=socket2, soc3=socket3,
                           ch0=ch0, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ch5=ch5, version_list=flist)

app.run(host='0.0.0.0', port=81)