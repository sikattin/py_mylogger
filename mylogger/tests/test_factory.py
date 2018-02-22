# -*- coding: utf-8 -*-
import unittest
from mylogger.factory import StdoutLoggerFactory, FileLoggerFactory, RotationLoggerFactory
from mylogger.logger import StreamLogger, FileLogger, RotationLogger


TEST_LOGFILE = r"C:\Users\shikano.takeki\Downloads\mylogger\mylogger\tests\test.log"


class TestStdoutLoggerFactory(unittest.TestCase):
    """stdoutloggerfactory class test class."""

    def setUp(self):
        """entering process."""
        self.stdlogger_fac = StdoutLoggerFactory()

    def tearDown(self):
        """exiting process"""
        self.stdlogger.close()
        del self.stdlogger_fac

    def test_create(self):
        self.stdlogger = self.stdlogger_fac.create()
        self.assertIsInstance(self.stdlogger, StreamLogger)

class TestFileLoggerFactory(unittest.TestCase):
    """fileloggerfactory class test class."""

    def setUp(self):
        """entering process."""
        self.filelogger_fac = FileLoggerFactory()

    def tearDown(self):
        """exiting process."""
        self.filelogger.close()
        del self.filelogger_fac

    def test_create(self):
        self.filelogger = self.filelogger_fac.create(file=r"{}".format(TEST_LOGFILE))
        self.assertIsInstance(self.filelogger, FileLogger)

class TestRotationLoggerFactory(unittest.TestCase):
    """rotationloggerfactory class test class."""

    def setUp(self):
        """entering process."""
        self.rotlogger_fac = RotationLoggerFactory()

    def tearDown(self):
        self.rotlogger.close()
        del self.rotlogger_fac

    def test_create(self):
        self.rotlogger = self.rotlogger_fac.create(file=r"{}".format(TEST_LOGFILE))
        self.assertIsInstance(self.rotlogger, RotationLogger)

if __name__ == '__main__':
    unittest.main()