import unittest

from wrapper import LoggerWrapper

class TestLoggerWrapper(unittest.TestCase):


    def test_valid_args(self):
        args = (
            'my_logger',
            'logger_config.json',
            'C:/tmp/log.log',
            'localhost',
            'debug',
            'debug',
            'debug'
        )
        self.assertTrue(LoggerWrapper(*args))

    def test_invalid_name_type(self):
        args = (
            101,
            'logger_config.json',
            'C:/tmp/log.log',
            'localhost',
        )
        with self.assertRaises(AssertionError):
            LoggerWrapper(*args)

    def test_invalid_logging_level(self):
        args = (
            'my_logger',
            'logger_config.json',
            'C:/tmp/log.log',
            'localhost',
            'no_such',
        )
        with self.assertRaises(AssertionError):
            LoggerWrapper(*args)

    def test_logging_level_assignment(self):

        '''
        Syslog -> Python logger level
        NOTSET = 0
        DEBUG = 10
        INFO = 20
        WARN = 30
        ERROR = 40
        CRITICAL = 50
        '''


        args = (
            'my_logger',
            'logger_config.json',
            'C:/tmp/log.log',
            'localhost',
        )

        kwargs = {
            'console_log_level': 'error',
            'file_log_level': 'Warning',
            'syslog_log_level': 'DEBUG'
        }

        lw = LoggerWrapper(*args, **kwargs)

        self.assertEqual(40, lw.logger.handlers[0].level) # Console handler.
        self.assertEqual(30, lw.logger.handlers[1].level) # File handler.
        self.assertEqual(10, lw.logger.handlers[2].level) # Syslog handler.

    def test_syslog_host_assignment(self):

        args = (
            'my_logger',
            'logger_config.json',
            'C:/tmp/log.log',
            'test-host.com',
        )

        kwargs = {
            'console_log_level': 'error',
            'file_log_level': 'Warning',
            'syslog_log_level': 'DEBUG'
        }

        lw = LoggerWrapper(*args, **kwargs)

        self.assertEqual(args[3], lw.logger.handlers[2].host) # Syslog handler.