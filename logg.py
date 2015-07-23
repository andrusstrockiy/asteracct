#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'andruss'

import logging
import logging.handlers

lvl = logging.INFO

class Loggable(object):
    """Loggable class."""

    def __init__(self, alog_file_name=__name__ + '.log', alog_level=logging.DEBUG, alog_name="radiusclient"):
        self.log_file_name = alog_file_name
        self.log_level = alog_level
        self.log_name = alog_name
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.log_level)
        # Log rotation
        handler = logging.handlers.TimedRotatingFileHandler(self.log_file_name, when="midnight", backupCount=14)
        # handler = logging.FileHandler(self.log_file_name)
        logger.addHandler(handler)
        formater = logging.Formatter('%(asctime)s  %(name)s -%(thread)s %(threadName)s '
                                     ' %(module)s - [%(levelname)s] - %(message)s')
        handler.setFormatter(formater)
        return logger

    def log(self, log_line, severity=None):
        self.logger.log(severity or self.log_level, log_line)

    def info(self, log_line):
        self.logger.info(log_line)

    def debug(self, log_line):
        self.logger.debug(log_line)

    def critical(self, log_line):
        self.logger.critical(log_line)

    def error(self, log_line):
        self.logger.error(log_line)

