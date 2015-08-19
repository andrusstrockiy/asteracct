#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logg
import ConfigParser


log = logg.Loggable(alog_name=__name__)


# Todo make file opener handler and log the message for No option 'radius_server' in section: 'globals'

# Default location of Asterisk ini files extensions.con and managers.conf
confdir = '/etc/asterisk/'
extensionsconf = confdir + 'extensions.conf'
managersconf = confdir + 'manager.conf'
celconf = confdir + 'cel.conf'
cdrconf = confdir + 'cdr_manager.conf'
asterisk_amihost = "127.0.0.1"


class ConfigOpener:
    """Class which parse configs"""
    global confdir, asterisk_amihost, log

    def __init__(self):
        """Initializing the following attributes"""
        self.config = ConfigParser.ConfigParser()
        self.configfiles = None
        self.radius_addr = None
        self.radius_secret = ""
        self.radius_acct_port = None
        self.rnas_addr = None
        self.raddict = {}
        # Ami Manager settings:
        self.amiport = None
        self.amienables = ''
        self.amihost = None
        self.amimanager = ''
        self.amisecret = ''
        self.amimdict = {}
        self.cdr_enabled = None
        self.amirw = ''
        # CEL settings:
        self.cel_enable = ''
        self.cel_answer = ''
        self.ami_backend = ''

    def radius_config(self, afconfig=extensionsconf):
        self.configfiles = self.config.readfp(open(afconfig))
        log.info(" -- Start reading config settings from file %s " % afconfig)
        try:
            self.radius_addr = self.config.get('globals', 'RADIUS_Server')
        except ConfigParser.NoOptionError:
            log.critical('Please set RADIUS_Server in [general] section of %s ini file' % afconfig)
            sys.stderr.write('Please set RADIUS_Server in [general] section of %s ini file' % afconfig)
            sys.exit(1)
        try:
            self.radius_acct_port = self.config.get('globals', 'RADIUS_Acct_Port')
        except ConfigParser.NoOptionError:
            log.critical('Please set RADIUS_Acct_Port in [general] section of %s ini file' % afconfig)
            sys.stderr.write('Please set  RADIUS_Acct_Port in [general] section of %s ini file' % afconfig)
            sys.exit(1)
        try:
            self.rnas_addr = self.config.get('globals', 'NAS_IP_Address')
        except ConfigParser.NoOptionError:
            log.critical('Please set NAS_IP_Address in [general] section of %s ini file' % afconfig)
            sys.stderr.write('Please set  NAS_IP_Address in [general] section of %s ini file' % afconfig)
            sys.exit(1)
        log.info(' -- Radius client settings are Radius address %s and Radius Accounting Ports %s'
                 % (self.radius_addr, self.radius_acct_port))
        try:
            self.radius_secret = self.config.get('globals', 'RADIUS_Secret')
        except ConfigParser.NoOptionError:
            log.critical('Please set RADIUS_Secret in [general] section of %s ini file' % afconfig)
            sys.stderr.write('Please set  RADIUS_Secret in [general] section of %s ini file' % afconfig)
            sys.exit(1)
        log.info(' -- NAS IP address %s ' % self.rnas_addr)
        self.raddict = {'radius_addr': self.radius_addr, 'radius_acct_port': self.radius_acct_port,
                        'rnas_addr': self.rnas_addr, 'radius_secret': self.radius_secret}
        return self.raddict

    def ami_config(self, afconfig=managersconf, ):
        log.info(" -- Start reading config settings from files %s " % afconfig)
        self.configfiles = self.config.readfp(open(afconfig))
        self.amiport = self.config.get('general', 'port')
        self.amienables = self.config.get('general', 'enabled')

        self.amihost = asterisk_amihost
        log.info("Reading AMI manager config")
        for managers in ['test', 'lbamimanager']:
            if managers in self.config.sections():
                # logger.setLevel(lg.DEBUG)
                log.debug("-managers- %s" % managers)
                self.amimanager = managers
                self.amisecret = self.config.get(managers, 'secret')
                log.info("AMI manager login credentials:%s " % managers)
                try:
                    self.amirw = self.config.get(managers, 'read')
                except ConfigParser.NoOptionError:
                    log.critical('Please set read = system,log,cdr,agent,call,user '
                                 ' in %s file ' % afconfig)
                    sys.exit(1)
                if self.amirw.find('cdr') == -1:
                    log.critical('Please set read = system,log,cdr,agent,call,user '
                                 ' in %s file ' % afconfig)
                    sys.exit(1)
                else:
                    log.info('AMI manager read settings are %s' % self.amirw)
                break
            else:
                log.critical('AMI manager couldn\'t be found')
                log.critical('Please set one in /etc/asterisk/manager.conf')
                sys.exit(1)

        self.amimdict = {'ami_port': self.amiport, 'ami_enabled': self.amienables, 'ami_host': self.amihost,
                         'ami_manager': self.amimanager, 'ami_secret': self.amisecret}
        return self.amimdict

    def cdr_config(self, afconfig=cdrconf):
        log.info(' --Start reading CDR  config from ini file : %s' % afconfig)
        self.configfiles = self.config.readfp(open(afconfig))
        self.cdr_enabled = self.config.get('general', 'enabled')
        if self.cdr_enabled == 'yes':
            return True
        else:
            log.critical('Please set enabled=yes in [general] section of %s ini file' % afconfig)
            log.critical('Now value is set to %s' % self.cdr_enabled)
            sys.stderr.write('Please set enabled=yes in [general] section of %s ini file' % afconfig)
            sys.stderr.write("\n \t Exiting ...")
            sys.exit(1)

    def cel_config(self, afconfig=celconf):
        log.info('-- Start reading config from  %s file ' % afconfig)
        self.configfiles = self.config.readfp(open(afconfig))
        try:
            self.cel_enable = self.config.get('general', 'enable')
            if 'yes' != self.cel_enable:
                log.critical('Please set enable=yes in [general] section of %s ini file' % afconfig)
                sys.exit(1)
            self.cel_answer = self.config.get('general', 'events')
            if self.cel_answer.find('ANSWER') == -1:
                sys.stderr.write('Please set events=ANSWER in [general] section of %s ini file' % afconfig)
                log.critical('Please set events=ANSWER in [general] section of %s ini file' % afconfig)
                sys.exit(1)
        except ConfigParser.NoOptionError:
            sys.stderr.write('Please set enable=yes in [general] section of %s ini file' % afconfig)
            sys.exit(1)
            # print(afconfig+"Please set enable=yes in [general] section of  ini file", file=sys.stderr)
        try:
            self.ami_backend = self.config.get('manager', 'enabled')
            if 'yes' != self.ami_backend:
                log.critical('Please set enabled=yes in [manager] section of %s ini file' % afconfig)
                sys.exit(1)
        except ConfigParser.NoOptionError:
            sys.stderr.write('Please set enabled=yes in [manager] section of %s ini file' % afconfig)
            sys.exit(1)
        return True
