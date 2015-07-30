# Accounting script for Asterisk
<hr> </hr>
## Description

Accounting script which connects to [Asterisk](https://www.digium.com/products/asterisk/software) through [AMI](https://wiki.asterisk.org/wiki/display/AST/AMI+Event+Documentation)
 interface monitors all events and sends Radius Accounting to Billing Server (BS) for account charging. 
 
## Requirements

OS CentOS/5x or 6x Debian 6 or 7

Python 2.6 or Python 3.2 or later.



## Installation

1. Unzip / Untar the following archive with the script 
<pre> tar -zxvf asteracct.tar.gz </pre>
2. Copy the content to /opt/ folder
<pre> cp -r ./asteracct/* /opt </pre>

3. Edit asterisk dialplan __extensions.conf__ set the following global variables in general section of ini file
    <pre>RADIUS_Server=Ip_of_your_Radius_Server</pre>
    <pre>RADIUS_Secret=secret</pre>
    <pre>RADIUS_Auth_Port=1812</pre>
    <pre>RAIUS_Acct_Port=1813</pre>
    <pre>Acct_Update_Timeout=30</pre>
    <pre>NAS_IP_Address=Ip_of_your_asterisk</pre>

4. Enable and set asterisk AMI manager im <i>managers.conf</i> according the fol lowing example
    * For enabling ami interface asterisk at the top of <i>manageres.conf</i> set :
<pre> [general] </pre>
<pre>enabled = yes</pre>
<pre>port = 5038 </pre>
    * Setup manager (in same file) just add the following manager
<pre> [test] </pre> 
<pre> secret = test</pre>
<pre> permit= 127.0.0.1/255.255.255.0 </pre>
<pre> read = system,cdr,call,log,verbose,command,user </pre>
<pre> write = system,cdr,call,log,verbose,command,user </pre> 
5. Enable CDR output event to AMI console.Set in cdr _manager.conf_ 
<pre> [general]</pre>
<pre>  enabled = yes </pre>

6. Copy init (start,stop) scripts to /etc/init.d directory
<pre>cp /opt/asteracct/init/aster* /etc/init.d/ </pre>

7. Install [pyrad](https://pypi.python.org/pypi/pyrad) library required for that script either from
    * Pypi
        Download and unzip\untar.
    <pre> cd pyrad-2.0 </pre>
    and then inside the above directory
    <pre>sudo python setup.py install</pre>
    * From local folder (bundled)
    <pre> cd /opt/asteracct/libs/pyrad-2.0 </pre>
    and then 
    <pre> sudo python setup.py install</pre>
7. Start the script 
<pre> service asteramiacct start </pre>

8. Make some test calls and observe results.You should see Accounting-Start and Accounting-Stop packets to arrive at Radius



## Troubleshooting

For errors and troubleshooting please check log file asteracct.log of which located in /var/log/ directory.
If still in trouble contact me.



