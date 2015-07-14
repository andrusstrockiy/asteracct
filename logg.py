#!/usr/bin/env python

import logging as lg


class log():
    def __init__(self):
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.INFO)
        # create a file handler
        self.handler = lg.FileHandler('hello.log')
        self.handler.setLevel(lg.INFO)
        # create a logging format
        self.formatter = lg.Formatter('%(asctime)s  %(name)s -%(thread)s %(threadName)s '
                                      ' %(module)s- [%(levelname)s] - %(message)s')
        self.handler.setFormatter(self.formatter)
        # add the handlers to the logger
        self.logger.addHandler(self.handler)


a = log()
a.logger.info("Starting to log")
a.logger.debug('1111')
a.logger.setLevel(lg.DEBUG)
a.logger.debug('Debug leve -  level to debug')
a.logger.setLevel(lg.INFO)
a.logger.info("back to info")
