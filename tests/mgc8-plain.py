#!/usr/bin/env python
import sys, md5
import asterisk.manager


# from asterisk.manager import Manager

def main():
    k = asterisk.manager.Manager()
    la = []
    if not k.connected():
        k.connect('192.168.6.254')
        k.login('test', 'test')
        ll = k.command('sip show registry')
        for i in ll.response:
            la.append(i.strip())
        monitlst = la[4:-1]
        print (monitlst)
        for i in monitlst:
            if '201' in i:
                print (i)
                print(i.split())


""""


A1 = "<DA_username>:<DA_realm>:<plain password from DB>"
A2 = "<DA_method>:<DA_uri>"
d = "MD5(A1):<DA_nonce>:MD5(A2)"
digest = MD5( d )


"""
#A1 = '100:asterisk:100100'
#A2 = 'REGISTER:sip:101@10.0.0.20'
#d = md5.update(A1).diget+":4b1c2367:"+md5.update(A2)
#
#
#m = md5.new()
#m.update("")
#m.digest()
if __name__ == '__main__':
    main()