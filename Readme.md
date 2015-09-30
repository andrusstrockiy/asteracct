# Radius Accounting script for Asterisk
<hr> </hr>
## Description

Accounting script which connects to [Asterisk](https://www.digium.com/products/asterisk/software) through [AMI](https://wiki.asterisk.org/wiki/display/AST/AMI+Event+Documentation)
 interface monitors all events and sends Radius Accounting to Billing Server (BS) for account charging. 
 
## Requirements

OS CentOS/5x or 6x Debian 6 or 7

Python 2.6 or Python 3.2 or later

Asterisk version starting from 1.8 and later



## Installation

1. Get the source either by downloading an archive file or by cloning
   1. For Archive.Download as zip file archive
      + Download the script with :
        <pre> wget https://github.com/andrusstrockiy/asteracct/archive/master.zip -O asteramiacct.zip </pre>
        + Then Unzip / Untar the following archive with the script
        <pre>sudo tar -zxvf asteramiacct.tar.gz -C /opt/</pre>
        + For unzip run the following:
        <pre>sudo unzip asteramiacct.zip -d /opt/ </pre>
   2. To clone the repository
      + cd to opt directory:
        <pre> cd /opt </pre>
      + and clone it:
        <pre>sudo git clone https://github.com/andrusstrockiy/asteracct.git</pre>
2. Change permissions for installation folder in case you not planning of  running that script as a root:
    <pre> chown _your_login_username_ /opt/asteracct/* </pre>
3. Edit asterisk dialplan __extensions.conf__ set the following global variables in _general_ section of that file
    <pre>
    [general]
    ....
    RADIUS_Server=Ip_of_your_Radius_Server
    RADIUS_Secret=secret
    RADIUS_Auth_Port=1812
    RAIUS_Acct_Port=1813
    Acct_Update_Timeout=30
    NAS_IP_Address=Ip_of_your_asterisk
    ...
    </pre>

4. Enable and set asterisk AMI manager in <i>managers.conf</i> according the following example
    * To  enable AMI interface on asterisk at the top of <i>manageres.conf</i> set :
      <pre>
      [general] 
      enabled = yes 
      port = 5038 
      </pre>
    * Then add manager (in same  _managers.conf_ file) by adding the following 
<pre>[test]
 secret = test
 permit= 127.0.0.1/255.255.255.0 
 read = system,cdr,call,log,verbose,command,user
 write = system,cdr,call,log,verbose,command,user 
 </pre> 
5. Enable CDR output event to AMI console.Set in cdr _manager.conf_ 
<pre> [general]
      enabled = yes </pre>

6. Copy init (start,stop) scripts to /etc/init.d directory
<pre>cp /opt/asteramiacct/init/aster* /etc/init.d/ </pre>
7. Enable cell events by setting in _cel.conf_
    Activate cel event in general settings
    <pre>
    [general]
    
    ; CEL Activation
    ;
    ; Use the 'enable' keyword to turn CEL on or off.
    ;
    ; Accepted values: yes and no
    ; Default value:   no
    enable=yes
    </pre>
    Forward cell events in AMI console
    <pre>
    [manager]
    ; AMI Backend Activation
    ;
    ; Use the 'enable' keyword to turn CEL logging to the Asterisk Manager Interface
    ; on or off.
    ;
    ; Accepted values: yes and no
    ; Default value:   no
    enabled=yes
    </pre>
    and then add 
    <pre>
    events=ANSWER
    </pre>

7. Install [pyrad](https://pypi.python.org/pypi/pyrad) Radius library required for that script either from
    * Pypi
        Download and unzip\untar.
    <pre> cd pyrad-2.0 </pre>
    and then inside the above directory
    <pre>sudo python setup.py install</pre>
    * From local folder (bundled)
    <pre> cd /opt/asteracct/libs/pyrad-2.0 </pre>
    and then 
    <pre> sudo python setup.py install</pre>
7. Restart Asterisk through to apply new settings to asterisk
    <pre>
    service asterisk restart
    </pre>
7. Start the script 
<pre> service asteramiacct start </pre>

8. Make some test calls and observe results.You should see Accounting-Start and Accounting-Stop packets to arrive at Radius

10. Check that your script is actually running after making few telephone calls by doing in linux console
    <pre> ps aux | grep ast </pre>
    Should give output like the following 
    <pre> 
    [root@pbx-msk andruss]# ps aux | grep ast
    root      3514  0.0  0.0 106064   528 ?        S    Sep01   0:00 /bin/sh /usr/sbin/safe_asterisk -U asterisk -G asterisk
    asterisk  3517  0.4  1.4 1530376 31128 ?       Sl   Sep01 168:58 /usr/sbin/asterisk -f -U asterisk -G asterisk -vvvg -c
    root      5526  0.0  0.4  82880  8524 ?        S    15:11   0:00 /usr/bin/python2.6 /opt/asteracct/asteramiacct.py
    </pre>

## Troubleshooting

For errors and troubleshooting please check log file asteracct.log of which located in __/opt/asteracct/__ directory.
If still in trouble contact me.



## Author, copyright, availability


asteramiacct was written by Andrew Tkachenko <trockiy4@hotmail.com> and is licensed
under a BSD license. 

Copyright and license information can be found in the LICENSE.txt file.

The current version and documentation can be found on github:
[source] (https://github.com/andrusstrockiy/asteracct)

Bugs and wishes can be submitted in the issue tracker on github:
[issues] (https://github.com/andrusstrockiy/asteracct/issues)

