#!/usr/bin/env python
import ConfigParser
import sys
import logg


log = logg.Log()




# Todo make file opener handler and log the message for No option 'radius_server' in section: 'globals'

# Default location of Asterisk ini files extensions.con and managers.conf

extensionsconf = '/etc/asterisk/extensions.conf'
managersconf = '/etc/asterisk/manager.conf'
asterisk_amihost = "192.168.55.254"


confdir = [extensionsconf, managersconf]


class ConfigOpener():
    """Class which parse configs"""
    global confdir, asterisk_amihost

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



    def radius_config(self, afconfigs=extensionsconf):
        self.configfiles = self.config.readfp(open(afconfigs))
        log.logger.info(" -- Start reading config settings from file %s " % afconfigs)

        self.radius_addr = self.config.get('globals', 'RADIUS_Server')
        self.radius_acct_port = self.config.get('globals', 'RAIUS_Acct_Port')
        self.rnas_addr = self.config.get('globals', 'NAS_IP_Address')
        log.logger.info(' -- Radius client settings are Radius address %s and Radius Accounting Ports %s'
                        % (self.radius_addr, self.radius_acct_port))
        self.radius_secret = self.config.get('globals', 'RADIUS_Secret')
        log.logger.info(' -- NAS IP address %s ' % self.radius_addr)
        self.raddict = {'radius_addr': self.radius_addr, 'radius_acct_port': self.radius_acct_port,
                        'rnas_addr': self.rnas_addr, 'radius_secret': self.radius_secret}
        return self.raddict

    def ami_config(self, afconfig=managersconf):
        log.logger.info(" -- Start reading config settings from file %s " % afconfig)
        self.configfiles = self.config.readfp(open(afconfig))
        self.amiport = self.config.get('general', 'port')
        self.amienables = self.config.get('general', 'enabled')
        self.amihost = asterisk_amihost
        log.logger.info("Reading AMI manager config")
        for managers in ['test', 'lbamimanager']:
            if managers in self.config.sections():
                # logger.setLevel(lg.DEBUG)
                log.logger.debug("-m- %s" % managers)
                self.amimanager = managers
                self.amisecret = self.config.get(managers, 'secret')
                log.logger.info("AMI manager login credentials:%s " % managers)
                break
            else:
                log.logger.critical('AMI manager couldn\'t be found')
                log.logger.critical('Please set one in /etc/asterisk/manager.conf')
                sys.exit(1)
        self.amimdict = {'ami_port': self.amiport, 'ami_enabled': self.amienables, 'ami_host': self.amihost,
                         'ami_manager': self.amimanager, 'ami_secret': self.amisecret}
        return self.amimdict

