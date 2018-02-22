#-------------------------------------------------------------------------------
# Name:        LoggerFactory.py
# Purpose:     Logger factory.
#
# Author:      shikano.takeki
#
# Created:     19/02/2018
# Copyright:   (c) shikano.takeki 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod
from logger import Logger


LOG_FILE = "log.log"

class Factory(metaclass=ABCMeta):
    """this class is abstrct class."""

    loglevel = 0

    def __init__(self, loglevel=None):
        if loglevel is not None and \
                       not loglevel in {10, 20, 30, 40, 50}:
            raise TypeError("set valid loglevel in the range of 10 or 20 or 30 or 40 or 50")
        if loglevel is None:
            self.loglevel = 20
        # set loglevel.
        Logger.loglevel = self.loglevel

    @abstractmethod
    def create(self, loglevel: int):
        pass

class StdoutLoggerFactory(Factory):
    """this class is a StreamLogger Factory."""

    def __init__(self, loglevel=None):
        super(StdoutLoggerFactory, self).__init__(loglevel)

    def create(self):
        from mylogger.logger import StreamLogger
        return StreamLogger()

class FileLoggerFactory(Factory):

    def __init__(self, loglevel=None):
        super(FileLoggerFactory, self).__init__(loglevel)

    def create(self, file=LOG_FILE):
        """
        create FileLogger instance.
        if file param is unset, log is outputed in current directory named 'log.log'

        Args:
            param1 file: log file path. defulat is written in 'log.log'

        Return:
            FileLogger instance.
        """
        from mylogger.logger import FileLogger
        return FileLogger(filename=file)

class RotationLoggerFactory(Factory):
    """this class is a RotationLoggerFactory."""
    def __init__(self, loglevel=None):
        super(RotationLoggerFactory, self).__init__(loglevel)

    def create(self, file=LOG_FILE, bcount=None):
        """
        create RotationLogger instance.
        if file param is unset, log is outputed in current directory named 'log.log'

        Args:
            param1 file: log file path. defulat is written in 'log.log'
            param2 bcount: backup generation count. default is 3.

        Return:
            RotationLogger instance.
        """
        from mylogger.logger import RotationLogger
        return RotationLogger(filename=file, bcount=bcount)

