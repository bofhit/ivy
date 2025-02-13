__doc__ = """Wrapper for Python logger.
    Will pull values from a configuration file.
    Main logger has separate handers for console and file logging.
    Logging levels for them can be defined separately.
    Caller will need to provide a config file path and a destination path
    for the file output."""

import json
import logging
import logging.config

import graypy

LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'critical')

class LoggerWrapper():
    def __init__(self,
        name:str,
        config:str,
        log_file:str,
        syslog_host:str,
        file_log_level:str='info',
        console_log_level:str='debug',
        syslog_log_level:str='info'
    ):
        """
        Attrs:
            name: Logger name, will appear in log files.
            config: Filepath for logger config.
            log_file: Filepath where the logger file handler will write files.
            file_log_level: Logging level for file output.
            console_log_level: Logging level for console output.
            syslog_log_level: Logging level for console output.
        """
        assert type(name) == str, 'Argument "name" must be a string.'
        assert type(config) == str, 'Argument "config" must be a string.'
        assert type(log_file) == str, 'Argument "log_file" must be a string.'
        assert type(syslog_host) == str, 'Argument "syslog_host" must be a string.'

        assert console_log_level.lower() in LOG_LEVELS, f'{console_log_level} is not a valid logging level.'
        assert file_log_level.lower() in LOG_LEVELS, f'{file_log_level} is not a valid logging level.'
        assert syslog_log_level.lower() in LOG_LEVELS, f'{syslog_log_level} is not a valid logging level.'

        console_log_level= self.recast_log_level(console_log_level)
        file_log_level = self.recast_log_level(file_log_level)
        syslog_log_level= self.recast_log_level(syslog_log_level)

        with open(config) as f:
            json_obj = json.load(f)

        logging.config.dictConfig(json_obj)

        self.logger = logging.getLogger('main')
        self.logger.name = self.format_name(name)
        self.logger.handlers[0].level = console_log_level
        self.logger.handlers[1].level = file_log_level
        self.logger.handlers[2].level = syslog_log_level


    def recast_log_level(self, string):
        """
        Convert a string to a logging module flag.
        """
        if string.lower() == 'debug':
            return logging.DEBUG
        elif string.lower() == 'info':
            return logging.INFO
        elif string.lower() == 'warning':
            return logging.WARNING
        elif string.lower() == 'error':
            return logging.ERROR
        elif string.lower() == 'critical':
            return logging.CRITICAL

    def format_name(self, name):
        """
        Pad name with spaces, for log readability.
        """
        return name.ljust(20)

if __name__ == '__main__':
    import sys

    lw = LoggerWrapper('myLogger',
                        'logger_config.json',
                        'C:/tmp/log.log',
                        'localhost'
                        )

    print(lw.logger.handlers)