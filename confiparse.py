#!/usr/bin/env python
import ConfigParser, logging as lg
# Todo make file opener handler and log the message for No option 'radius_server' in section: 'globals'

# Default location of Asterisk ini files extensions.con and managers.conf
extensionsconf = '/etc/asterisk/extensions.conf'
managersconf = '/etc/asterisk/managers.conf'

logger = lg.getLogger('configparser')
logger.setLevel(lg.INFO)

fh = lg.FileHandler("astradclient.log")

formatter = lg.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

confdir = [extensionsconf, managersconf]




# radius_addr = config.get('globals', 'RADIUS_Server')
# radius_secret = config.get('globals', 'RADIUS_Secret')
# radius_acct_port = config.get('globals','RAIUS_Acct_Port')
# rnas_addr = config.get('globals','NAS_IP_Address')
#
#
# logger.info('Radius client settings Radius address %s Radius Accounting Ports %s' % (str(radius_addr), str(radius_addr)))
#

class ConfigOpener():
    """Class which parse configs"""
    global confdir

    def __init__(self, afconfigs=confdir):
        logger.info("--Start reading config settings from files %s %s"
                    % (afconfigs[0], afconfigs[1]))

        self.config = ConfigParser.ConfigParser()

        self.configfiles = self.config.read(afconfigs)
        self.radius_addr = self.config.get('globals', 'RADIUS_Server')

        self.radius_acct_port = self.config.get('globals', 'RAIUS_Acct_Port')
        self.rnas_addr = self.config.get('globals', 'NAS_IP_Address')

        logger.info('-- Radius client settings are Radius address %s and Radius Accounting Ports %s'
                    % (self.radius_addr, self.radius_acct_port))
        self.radius_secret = self.config.get('globals', 'RADIUS_Secret')

        self.rnas_addr = self.config.get('globals', 'NAS_IP_Address')
        logger.info('-- NAS IP address %s '
                    % (self.radius_addr))
