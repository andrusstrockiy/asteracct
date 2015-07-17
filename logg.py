#!/usr/bin/env python

__author__ = 'andruss'

import logging


class Loggable(object):
    """Loggable class."""

    def __init__(self, alog_file_name='log.txt', alog_level=logging.INFO, alog_name="radiusclient"):
        self.log_file_name = alog_file_name
        self.log_level = alog_level
        self.log_name = alog_name
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.log_level)
        handler = logging.FileHandler(self.log_file_name)
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

