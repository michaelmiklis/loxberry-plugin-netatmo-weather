#!/usr/bin/python3
# encoding=utf-8

# 2017-07-29 Michael Miklis (michaelmiklis.de)


import time
import configparser
import urllib.parse
import requests
import json
import sys
import socket
import time
from lxml import html


def main():
    # ---------------------------------------------
    # Global variables
    # ---------------------------------------------
    separator = ";"

    # ---------------------------------------------
    # Parse PlugIn config file
    # ---------------------------------------------
    pluginconfig = configparser.ConfigParser()
    pluginconfig.read(
        "REPLACEBYBASEFOLDER/config/plugins/REPLACEBYSUBFOLDER/netatmo.cfg")

    username = pluginconfig.get('NETATMO', 'USERNAME')
    password = pluginconfig.get('NETATMO', 'PASSWORD')
    enabled = pluginconfig.get('NETATMO', 'ENABLED')
    localtime = pluginconfig.get('NETATMO', 'ENABLED')
    miniservername = pluginconfig.get('NETATMO', 'MINISERVER')
    virtualUDPPort = int(pluginconfig.get('NETATMO', 'UDPPORT'))

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
    # set User-Agent to emulate Windows 10 / IE 11
    # ---------------------------------------------
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}

    # ---------------------------------------------
    # connect to netatmo website and grab a session cookie
    # ---------------------------------------------
    req = session.get("https://auth.netatmo.com/en-us/access/login")

    if req.status_code != 200:
        log("Unable to contact https://auth.netatmo.com/en-us/access/login", "ERROR")
        log("Error: {0}".format(req.status_code), "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # check if we got a valid session cookie
    # ---------------------------------------------
    loginpage = html.fromstring(req.text)
    token = loginpage.xpath('//input[@name="_token"]/@value')

    if token is None:
        log("No _token value found in response from https://auth.netatmo.com/en-us/access/login", "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # build the payload for authentication
    # ---------------------------------------------
    payload = {'email': username,
               'password': password,
               '_token': token}

    # ---------------------------------------------
    # login and grab an access token
    # ---------------------------------------------
    req = session.post(
        "https://auth.netatmo.com/access/postlogin", data=payload)

    if req.status_code != 200:
        log("Unable to contact https://auth.netatmo.com/access/postlogin", "ERROR")
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
    payload = {'access_token': urllib.parse.unquote(
        session.cookies.get("netatmocomaccess_token"))}

    # ---------------------------------------------
    # query device list to get current measurements
    # ---------------------------------------------
    req = session.post(
        "https://api.netatmo.com/api/getstationsdata", data=payload)

    if req.status_code != 200:
        log("Unable to contact https://api.netatmo.com/api/getstationsdata", "ERROR")
        log("Status-Code {0} {1}".format(req.status_code, req.text), "ERROR")
        sys.exit(-1)

    # ---------------------------------------------
    # check if we got a valid access token
    # ---------------------------------------------
    if req.text.startswith("{\"body\":{\"") == False:
        log("Response from https://api.netatmo.com/api/getstationsdata has wrong format", "ERROR")
        log("Error: {0}".format(req.text), "ERROR")
        sys.exit(-1)

    print(req.text)
    sys.exit(0)
# _______________________________________________________________________________________


main()
