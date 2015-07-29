#!/usr/bin/python2.6
import sys, urllib2, urllib

from asterisk.agi import *

URL = 'https://hd.lanbilling.ru'


# agi = AGI()
# agi.verbose("python agi started")
# callerId = agi.env['agi_callerid']
# agi.verbose("call from %s" % callerId)
# print(agi.env.items())


# while True:
# agi.stream_file('vm-extension')
# result = agi.wait_for_digit(-1)
#   agi.verbose("got digit %s" % result)
#   if result.isdigit():
#     agi.say_number(result)
#   else:
#    agi.verbose("bye!")
#    agi.hangup()
#    sys.exit()

def main():
    agi = AGI()
    agi.verbose("Python agi started")
    callerId = agi.env['agi_callerid']
    agi.verbose("call from %s" % callerId)
    if agi.env['agi_arg_2'] == '':
        agicallerid = agi.env['agi_callerid']
    else:
        agicallerid = agi.env['agi_arg_2']


    # # Debug
    # env ={}
    # env['agi_arg_1'] = '2015-04-30T11:20:48'
    # env['agi_arg_2'] = '624'
    # env['agi_arg_3'] = '89295139104'
    # # env['agi_arg_2'] = '624624'
    # msg = mcall(adatetime=env['agi_arg_1'],anis=env['agi_arg_2'],adnis=env['agi_arg_3'])

    msg = mcall(adatetime=agi.env['agi_arg_1'], anis=agicallerid, adnis=agi.env['agi_arg_3'])
    # msg = scall(adatetime=agi.env['agi_arg_1'],aniquenum=agi.env['agi_arg_3'],
    #        adispositon=agi.env['agi_arg_4'],acallerid=agicallerid)
    print(agi.env.items())
    print(msg)
    # agi.verbose(msg)
    # agi.verbose("Bye",level=4)
    sys.exit(0)

    #print(agi.env.items())


def scall(adatetime, aniquenum, adispositon, acallerid='unknown'):
    global URL, agi
    # Prepate headers
    user_agent = "Curl API Agent"
    cookstr = 'c192f91b59f7b87b=asteriskstat:0:169a4941d1485e1c702b867b51a2770c2b6e12f7;language=en'
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    opener.addheaders = [('User-agent', user_agent), ('X-Requested-With', 'XMLHttpRequest'),
                         ('X-Sbss-Auth', 'asteriskstat'), ('Cookie', cookstr)]

    # Post data
    methd = "inc=callsmonitor&cmd=setcallsstat"
    clu = "&callunique=" + str(aniquenum)
    src = "&src=" + str(acallerid)
    cdt = "&calldate=" + str(adatetime)
    dsp = "&disposition=" + str(adispositon)

    payload = methd + clu + src + cdt + dsp
    response = opener.open(URL, data=payload)
    html = response.read()

    return html

    # if response:
    #     agi.verbose("Data of the call was sucessfully sent to SBSS")
    #     return None


def mcall(adatetime, anis, adnis):
    '''Function to send email in case of missed call'''

    global URL, agi
    user_agent = "Curl API Agent"
    cookstr = 'c192f91b59f7b87b=asteriskstat:0:169a4941d1485e1c702b867b51a2770c2b6e12f7;language=en'
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    opener.addheaders = [('User-agent', user_agent), ('X-Requested-With', 'XMLHttpRequest'),
                         ('X-Sbss-Auth', 'asteriskstat'), ('Cookie', cookstr)]
    # Post data
    methd = "inc=callsmonitor&cmd=setmissedcallnotify"
    ani = "&src=" + str(anis)
    dnis = "&dst=" + str(adnis)
    cdt = "&calldate=" + str(adatetime)

    payload = methd + ani + dnis + cdt
    response = opener.open(URL, data=payload)
    html = response.read()
    return html


if __name__ == '__main__':
    main()
