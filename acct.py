#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logg
import confiparse
import socket
import sys
from os import getcwd as pwd
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

log = logg.Loggable(alog_name=__name__)


ch = confiparse.ConfigOpener()
ch = ch.radius_config()

radiusaddr = ch['radius_addr']
radiusscrt = ch['radius_secret']

getrdir = pwd()

srv = Client(server=radiusaddr, secret=radiusscrt,
             dict=Dictionary(getrdir + "/dicts/dictionary", getrdir + "/dicts/dictionary.cisco",
                             getrdir + "/dicts/dictionary.rfc2866"))


def SendPacket(srv, req):
    global log
    """
    :param srv:
    :param req:
    """

    try:
        srv.SendPacket(req)
    except pyrad.client.Timeout:
        log.critical("RADIUS server does not reply")
        sys.exit(1)
    except socket.error, error:
        log.critical("Network error: " + error[1])
        sys.exit(1)


def accountingStart(aani, adni, aconfid, asetuptime, aconnectime, acallorig='h323-call-origin=originate',
                    anassip=ch['rnas_addr'], anasport=0, anasidentifier='asterisk'):
    """
    Function to send Accounting Start
    :rtype : string
    :type anassip: string
    """
    srv = Client(server=radiusaddr, secret=radiusscrt, dict=Dictionary("./dicts/dictionary",
                                                                       "./dicts/dictionary.cisco"))
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
    log.debug("--- Accounting START packet have been sent")


def accountingStop(aani, aconfid, acause, adni, asetuptime, acalltype,
                   aconnectime, adisconectime, agwid, acallorig='originate', aacountsessiontime=0):
    """
    Function to send Accounting STOP packet
    :rtype : str
    :return:
    """

    req = srv.CreateAcctPacket(User_Name=aani)
    req["Acct-Status-Type"] = "Stop"
    req['h323-conf-id'] = aconfid
    # req['Acct-Session-Time'] = 120
    # req["Acct-Input-Octets"] = random.randrange(2**10, 2**30)
    # req["Acct-Output-Octets"] = random.randrange(2**10, 2**30)
    # req["Acct-Session-Time"] = random.randrange(120, 3600)
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
    log.debug(" --- Accounting STOP packet have been sent")