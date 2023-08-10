import unittest

from wrapper import LoggerWrapper

class TestLoggerWrapper(unittest.TestCase):

    def setUp(self):
        self.lw = LoggerWrapper(
                    'test_logger',
                    'config.json',
                    'C:/io/io.log'
                )

    def test_invalid_logging_level(self):
        with self.assertRaises(AttributeError):
            self.lw.logger.invalid('This a is debug message.')
