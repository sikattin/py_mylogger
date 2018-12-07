#-------------------------------------------------------------------------------
# Name:        logger.py
# Purpose:     ロガー生成用モジュール.
#
# Author:      shikano.takeki
#
# Created:     13/12/2017
# Copyright:   (c) shikano.takeki 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
from logging import getLogger, StreamHandler, FileHandler, Formatter, WARNING
from logging.handlers import RotatingFileHandler
import os, time

class Logger(object):
    """ロガーを生成するクラス.

    このクラスは直接インスタンス化しません。
    """
    ##==============================##
    # loglevel:
    #          CRITICAL... 50
    #          ERROR   ... 40
    #          WARNING ... 30
    #          INFO    ... 20
    #          DEBUG   ... 10
    ##==============================##
    loglevel = WARNING

    def __init__(self, logger_name: str, handler):
        """コンストラクタ

        Args:
            param1 logger_name: ロガーの名前.
            param2 handler: Handler instance.

        Returns:
        """
        # ロガー作成.
        self._logger = getLogger(str(logger_name))
        self._logger.setLevel(self.loglevel)
        # ハンドラの作成.
        self.h = handler
        self.h.setLevel(self.loglevel)
        # フォーマッターの作成.
        formatter = Formatter(
            '%(asctime)s-%(name)s [%(levelname)s] : %(message)s')
        self.h.setFormatter(formatter)
        # ロガーにハンドラを追加.
        self._logger.addHandler(self.h)
        # ログを親に伝播させない.
        self._logger.propagate = False

    def info(self, msg: str):
        """infoレベルのログメッセージを送信する.

        Args:
            param1 msg:送信したいメッセージ.

        Returns:
            Not returns value.
        """
        self._logger.info(msg)

    def debug(self, msg: str):
        """DEBUGレベルのログメッセージを送信する.

        Args:
            param1 msg: 送信したいメッセージ.

        Returns:
            Not returns value.
        """
        self._logger.debug(msg)

    def warning(self, msg: str):
        """WARNINGレベルのログメッセージを送信する.

        Args:
            param1 msg: 送信したいメッセージ.

        Returns:
            Not returns value.
        """
        self._logger.warning(msg)

    def error(self, msg: str):
        """send error level log.
        Args:
            param1 msg: 送信したいメッセージ.

        Returns:
            Not returns value.
        """
        self._logger.error(msg)

    def exception(self, msg: str):
        """send message to logger.

        please use in except clause.
        Args:
            param1 msg: 送信したいメッセージ

        Returns:
            Not returns value.
        """
        self._logger.exception(msg)

    def set_loglevel(self, level: int):
        """set log level.

        Args:
            param1 level: log level
                CRITICAL... 50
                ERROR... 40
                WARNING... 30
                INFO... 20
                DEBUG... 10
        """
        self.loglevel = level
        self._logger.setLevel(self.loglevel)
        self.h.setLevel(self.loglevel)
        self._logger.addHandler(self.h)

    def add_handler(self, handler):
        """add handler to root logger."""
        self._logger.addHandler(handler)

    def close(self):
        """close handling"""
        self.h.close()


class StreamLogger(Logger):
    """標準出力、エラー出力にログを出力するロガーを提供するクラス."""

    def __init__(self, logger_name: str):
        if logger_name is None:
            logger_name = str(self)
        Logger.__init__(self, logger_name=str(self), handler=StreamHandler())


class FileLogger(Logger):

    """ディスク上のファイルにログを出力するロガーを提供するクラス."""
    def __init__(self, filename: str, logger_name: str):
        if logger_name is None:
            logger_name = str(self)
        self.handler = FileHandler(filename=filename, mode='a+')
        Logger.__init__(self, logger_name=logger_name, handler=self.handler)

    def close(self):
        """close current stream."""
        self.handler.close()
        super(FileLogger, self).close()

class RotationLogger(Logger):
    """ディスク上のファイルにログを出力するロガーを提供するクラス.
    ローテーション機能を持つ.
    """
    # backup generation count.
    # use set_backupCount() to change this variable.
    backupCount = 3

    def __init__(self, filename: str, logger_name: str, bcount=None, max_bytes=0):
        """constructor
            Args:
                param1 filename: log file name.
                param2 bcount: generation control count for backup log files.
                    default is 3 gen. for example, <basefilename>.1 ~ .3
        """
        if bcount is None:
            bcount = self.backupCount
        if logger_name is None:
            logger_name = str(self)
        self.filename = filename
        self.handler = RotatingFileHandler(filename=filename,
                                           mode='a+',
                                           backupCount=bcount,
                                           maxBytes=max_bytes)
        self.handler.namer = self.namer
        Logger.__init__(self, logger_name=logger_name, handler=self.handler)

    def namer(self, path):
        """override method of RotationFileHandler.rotation_filename"""
        # prefixにdatetimeを付与する処理
        lt = time.localtime()
        tm_yaer, tm_mon, tm_mday = str(lt.tm_year), str(lt.tm_mon), str(lt.tm_mday)
        if len(str(lt.tm_mon)) == 1:
            tm_mon = "0" + str(lt.tm_mon)
        if len(str(lt.tm_mday)) == 1:
            tm_mday = "0" + str(lt.tm_mday)
        datestr = tm_yaer + tm_mon + tm_mday
        filename = datestr + "_" + os.path.split(path)[1]
        result = os.path.join(os.path.split(path)[0], filename)
        return result
    '''
    def do_rotation(self):
        """execute log file rotation.
        """
        self.handler.emit('Rollover the log file')
        super(RotationLogger, self).add_handler(self.handler)
    '''

    def set_backupCount(self, v: int):
        """backupCount setter."""
        self.backupCount = v
        self.handler.backupCount = self.backupCount

    def close(self):
        self.handler.close()
        super(RotationLogger, self).close()


