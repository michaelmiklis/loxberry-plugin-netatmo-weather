#!/usr/bin/python3
# encoding=utf-8

# 2017-03-01 Michael Miklis (michaelmiklis.de)


import time
import configparser
import urllib.parse
import requests
import json
import sys
import socket

def main():
    # ---------------------------------------------
    # Global variables
    # ---------------------------------------------
    separator = ";"

    # ---------------------------------------------
    # Parse PlugIn config file
    # ---------------------------------------------
    pluginconfig = configparser.ConfigParser()
    pluginconfig.read("/opt/loxberry/config/plugins/netatmo/netatmo.cfg")

    username = pluginconfig.get('NETATMO', 'USERNAME')
    password = pluginconfig.get('NETATMO', 'PASSWORD')
    enabled = pluginconfig.get('NETATMO', 'ENABLED')
    miniservername = pluginconfig.get('NETATMO', 'MINISERVER')
    virtualUDPPort = int(pluginconfig.get('NETATMO', 'UDPPORT'))

    # ---------------------------------------------
    # Parse Loxberry config file
    # ---------------------------------------------
    loxberryconfig = configparser.ConfigParser()
    loxberryconfig.read("/opt/loxberry/config/system/general.cfg")

    miniserverIP = loxberryconfig.get(miniservername, 'IPADDRESS')


    # ---------------------------------------------
    # exit if PlugIn is not enabled
    # ---------------------------------------------
    if enabled != "1":
        sys.exit(-1)


    # ---------------------------------------------
    # start new request session
    # ---------------------------------------------
    session = requests.Session()

    # ---------------------------------------------
    # connect to netatmo website and grab a session cookie
    # ---------------------------------------------
    req = session.get("https://auth.netatmo.com/de-DE/access/login")

    if req.status_code != 200:
        log("Unable to contact https://auth.netatmo.com/de-E/access/login", "ERROR")
        log("Error: {0}".format(req.status_code), "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # check if we got a valid session cookie
    # ---------------------------------------------
    if session.cookies.get("netatmocomci_csrf_cookie_na") is None:
        log("No netatmocomci_csrf_cookie_na value found in session cookie", "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # build the payload for authentication
    # ---------------------------------------------
    payload = {'ci_csrf_netatmo': session.cookies.get("netatmocomci_csrf_cookie_na"),
               'mail': username,
               'pass': password,
               'log_submit': "LOGIN"}

    # ---------------------------------------------
    # login and grab an access token
    # ---------------------------------------------
    req = session.post("https://auth.netatmo.com/de-DE/access/login", data=payload)

    if req.status_code != 200:
        log("Unable to contact https://auth.netatmo.com/de-E/access/login", "ERROR")
        log("Error: {0}".format(req.status_code), "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # check if we got a valid access token
    # ---------------------------------------------
    if session.cookies.get("netatmocomaccess_token") is None:
        log("No netatmocomaccess_token value found in session cookie - probably wrong username/password", "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # build the payload for reading data
    # ---------------------------------------------
    payload = {'access_token': urllib.parse.unquote(session.cookies.get("netatmocomaccess_token"))}

    # ---------------------------------------------
    # query device list to get current measurements
    # ---------------------------------------------
    req = session.post("https://my.netatmo.com/api/devicelist", data=payload)

    if req.status_code != 200:
        log("Unable to contact https://my.netatmo.com/api/devicelist", "ERROR")
        log("Status-Code {0} {1}".format(req.status_code, req.text), "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # check if we got a valid access token
    # ---------------------------------------------
    if req.text.startswith("{\"body\":{\"") == False:
        log("Response from https://my.netatmo.com/api/devicelist has wrong format", "ERROR")
        log("Error: {0}".format(req.text), "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # convert the response into json
    # ---------------------------------------------
    netatmodata = json.loads(req.text)
    stationdict = {}

    # ---------------------------------------------
    # Loop for each station
    # ---------------------------------------------
    for device in netatmodata["body"]["devices"]:

        # Loop for each sensor in station
        for sensor in device["dashboard_data"].keys():
            value = "{0}.{1}.{2}={3}".format(device["station_name"], device["module_name"], sensor, str(device["dashboard_data"][sensor]))

            # send udp datagram
            sendudp(value, miniserverIP, virtualUDPPort);

        # add station to dictionary
        stationdict.update({device["_id"] :  device["station_name"]})

    # ---------------------------------------------
    # Loop for each module
    # ---------------------------------------------
    for module in netatmodata["body"]["modules"]:

        # Loop for each sensor in module
        for sensor in module["dashboard_data"].keys():
            value = "{0}.{1}.{2}={3}".format(stationdict[module["main_device"]], module["module_name"], sensor, str(module["dashboard_data"][sensor]))

            # send udp datagram
            sendudp(value, miniserverIP, virtualUDPPort);

    # exit with errorlevel 0
    sys.exit(0)

# _______________________________________________________________________________________


def sendudp(data, destip, destport):
    # start a new connection udp connection
    connection = socket.socket(socket.AF_INET,     # Internet
                               socket.SOCK_DGRAM)  # UDP

    # send udp datagram
    res = connection.sendto(data.encode(), (destip, destport))

    # close udp connection
    connection.close()

    # check if all bytes in resultstr were sent
    if res != data.__len__():
        log("Sent bytes do not match - expected {0} : got {1}".format(data.__len__(), res), "ERROR")
        log("Packet-Payload {0}".format(data), "ERROR")
        sys.exit(-1)

# _______________________________________________________________________________________


def log(message, level="INFO"):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(time.time()))

    print("{0}  {1} {2}".format(timestamp, level, message))
# _______________________________________________________________________________________

main()
