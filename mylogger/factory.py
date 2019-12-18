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
from mylogger.logger import Logger
from logging import WARNING
import os


ROLLOVER_SIZE = 100 * 1024 * 1024


class Factory(metaclass=ABCMeta):
    """this class is abstrct class."""

    def __init__(self, logger_name=None, loglevel=WARNING):
        self._logger_name = logger_name
        self._loglevel = loglevel

    @abstractmethod
    def create(self):
        pass

class StdoutLoggerFactory(Factory):
    """this class is a StreamLogger Factory."""

    def __init__(self, logger_name=None, loglevel=WARNING):
        super(StdoutLoggerFactory, self).__init__(
            logger_name=logger_name,
            loglevel=loglevel)

    def create(self):
        from mylogger.logger import StreamLogger
        return StreamLogger(self._logger_name, loglevel=self._loglevel)

class FileLoggerFactory(Factory):

    def __init__(self, logger_name=None, loglevel=WARNING):
        super(FileLoggerFactory, self).__init__(
            logger_name=logger_name,
            loglevel=loglevel
        )

    def create(self, filename):
        """
        create FileLogger instance.
        if file param is unset, log is outputed in current directory named 'log.log'

        Args:
            param1 filename: log file path.

        Return:
            FileLogger instance.
        """
        from mylogger.logger import FileLogger
        # if there is no the log file directory, make the directory.
        split_path = os.path.split(filename)
        if not split_path[0] != '':
            if not os.path.exists(split_path[0]):
                os.makedirs(split_path[0])
        return FileLogger(
            filename=filename,
            logger_name=self._logger_name,
            loglevel=self._loglevel)

class RotationLoggerFactory(Factory):
    """this class is a RotationLoggerFactory."""
    def __init__(self, logger_name=None, loglevel=None):
        self._logger_name = logger_name
        super(RotationLoggerFactory, self).__init__(
            logger_name=logger_name,
            loglevel=loglevel
        )

    def create(
        self,
        filename,
        bcount=None,
        max_bytes=None,
        is_change_fname=False):
        """
        create RotationLogger instance.
        if file param is unset, log is outputed in current directory named 'log.log'

        Args:
            param1 file: log file path. defulat is written in 'log.log'
            param2 bcount: backup generation count. default is 3.
            param3 max_bytes: max limit of file byte size to rollover log.

        Return:
            RotationLogger instance.
        """
        from mylogger.logger import RotationLogger
        # if there is no the log file directory, make the directory.
        split_path = os.path.split(filename)
        if not split_path[0] == '':
            if not os.path.exists(split_path[0]):
                os.makedirs(split_path[0])
        return RotationLogger(
            filename=filename,
            logger_name=self._logger_name,
            bcount=bcount,
            max_bytes=max_bytes,
            loglevel=self._loglevel,
            is_change_fname=is_change_fname
        )

