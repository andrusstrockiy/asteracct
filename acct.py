#!/usr/bin/env python

# Todo create parse function to parse radius settings from extensions.conf

import random, socket, sys
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from time import sleep

radiusaddr = '192.168.6.254'
radiusscrt = 'secret'

#print("---Sending accounting start packet")


srv = Client(server=radiusaddr, secret=radiusscrt,
             dict=Dictionary("./dicts/dictionary", "./dicts/dictionary.cisco", "./dicts/dictionary.rfc2866"))
req = srv.CreateAcctPacket(User_Name="624")


def SendPacket(srv, req):
    """

    :param srv:
    :param req:
    """
    try:
        srv.SendPacket(req)
    except pyrad.client.Timeout:
        print("RADIUS server does not reply")
        sys.exit(1)
    except socket.error, error:
        print("Network error: " + error[1])
        sys.exit(1)


# req["NAS-IP-Address"]="127.0.0.1"
# req["NAS-Port"]=0
# req["NAS-Identifier"]="asterisk"
# req["Called-Station-Id"]="89295139104"
# req["Calling-Station-Id"]="624"
# req['h323-conf-id'] = '704593A5 7301CCB2 186D581D FADCA9B1'
# req['h323-setup-time'] = '16:07:21.000 UTC Wed Mar 18 2015'
# req['h323-connect-time'] = '16:07:22.000 UTC Wed Mar 18 2015'
# req['h323-call-origin'] = 'h323-call-origin=originate'
#req["Framed-IP-Address"]="10.0.0.100"
# 'h323-conf-id', vendor Cisco, value: "704593A5 7301CCB2 186D581D FADCA9BB"



def accountingStart(aani, adni, aconfid, asetuptime, aconnectime, acallorig='h323-call-origin=originate',
                    anassip='127.0.0.1', anasport=0, anasidentifier='asterisk'):
    """
    Function to send Accounting Start

    :rtype : string
    :type anassip: string
    """

    srv = Client(server=radiusaddr,
                 secret=radiusscrt,
                 dict=Dictionary("./dicts/dictionary", "./dicts/dictionary.cisco"))
    req = srv.CreateAcctPacket(User_Name=aani)
    req["Acct-Status-Type"] = "Start"
    req["NAS-IP-Address"] = anassip
    req["NAS-Port"] = anasport
    req["NAS-Identifier"] = anasidentifier
    req["Called-Station-Id"] = aani
    req["Calling-Station-Id"] = adni
    req['h323-conf-id'] = aconfid
    req['h323-setup-time'] = 'h323-setup-time=' + asetuptime
    req['h323-connect-time'] = 'h323-connect-time=' + aconnectime
    req['h323-call-origin'] = acallorig
    SendPacket(srv, req)
    print("--- Sending accounting START packet")


sleep(5)


def accountingStop(aani, aconfid, acause,
                   adni, asetuptime, acalltype,
                   aconnectime, adisconectime, agwid,
                   acallorig='originate',
                   aacountsessiontime=0):
    """
    Function to send Accounting stop
    :rtype : str
    :return:
    """

    global srv
    req = srv.CreateAcctPacket(User_Name=aani)
    req["Acct-Status-Type"] = "Stop"
    req['h323-conf-id'] = aconfid
    #req['Acct-Session-Time'] = 120
    #req["Acct-Input-Octets"] = random.randrange(2**10, 2**30)
    #req["Acct-Output-Octets"] = random.randrange(2**10, 2**30)
    #req["Acct-Session-Time"] = random.randrange(120, 3600)
    req["Acct-Terminate-Cause"] = int(acause)
    req["Called-Station-Id"] = adni
    req["Calling-Station-Id"] = aani
    req['h323-setup-time'] = 'h323-setup-time=' + asetuptime
    req["h323-connect-time"] = "h323-connect-time=" + aconnectime
    req["h323-disconnect-time"] = "h323-disconnect-time=" + adisconectime
    req['h323-disconnect-cause'] = 'h323-disconnect-cause=' + str(acause)
    req['h323-gw-id'] = 'h323-gw-id=' + agwid
    req['h323-call-origin'] = 'h323-call-origin=' + acallorig
    req['Acct-Session-Time'] = int(aacountsessiontime)
    if acalltype == 'SIP' or acalltype == 'IAX':
        req['h323-call-type'] = 'h323-call-type=' + 'VoIP'
    else:
        req['h323-call-type'] = 'h323-call-type=' + 'Telephony'
    SendPacket(srv, req)
    print(" --- Accounting STOP packet have been sent")

