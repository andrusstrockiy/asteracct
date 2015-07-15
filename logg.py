#!/usr/bin/env python

import logging as lg


class Log():
    def __init__(self):
        self.logger = lg.getLogger(__name__)

        # create a file handler
        self.handler = lg.FileHandler('astradclient.log')

        # create a logging format
        self.formatter = lg.Formatter('%(asctime)s  %(name)s -%(thread)s %(threadName)s '
                                      ' %(module)s- [%(levelname)s] - %(message)s')
        self.handler.setFormatter(self.formatter)
        # add the handlers to the logger
        self.logger.addHandler(self.handler)

