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

    def __init__(self, logger_name: str, handler, loglevel=None):
        """コンストラクタ

        Args:
            param1 logger_name: ロガーの名前.
            param2 handler: Handler instance.

        Returns:
        """
        self.name = logger_name
        self.loglevel = loglevel
        if self.loglevel is None:
            self.loglevel = Logger.loglevel
        elif self.loglevel not in {10, 20, 30, 40, 50}:
            raise TypeError("set a valid loglevel between 10 and 50")
        # ロガー作成.
        self._logger = getLogger(str(logger_name))
        self._logger.setLevel(self.loglevel)
        # ハンドラの作成.
        self.h = list()
        handler.setLevel(self.loglevel)
        # フォーマッターの作成.
        formatter = Formatter(
            '%(asctime)s-%(name)s [%(levelname)s] : %(message)s')
        handler.setFormatter(formatter)
        self.h.append(handler)

        # ロガーにハンドラを追加.
        self._logger.addHandler(handler)
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
        [h.setLevel(self.loglevel) for h in self.h]

    def add_handler(self, handler):
        """add handler to root logger."""
        # set handler
        # set loglevel
        handler.setLevel(self.loglevel)
        # set formatter
        formatter = Formatter(
            '%(asctime)s-%(name)s [%(levelname)s] : %(message)s')
        handler.setFormatter(formatter)
        # add handler to logger
        self.h.append(handler)
        self._logger.addHandler(handler)

    def __remove_handler(self, handler):
        """remove the specified handler from logger.
        
        Args:
            handler ([type]): logging.Handler()
        """
        self.h.remove(handler)
        self._logger.removeHandler(handler)


    def close(self):
        """close handling"""
        self.__close_handlers()

    def close_handler(self, handler):
        handler.close()
        self.__remove_handler(handler)

    def __close_handlers(self):
        [h.close() for h in self.h]


class StreamLogger(Logger):
    """標準出力、エラー出力にログを出力するロガーを提供するクラス."""

    def __init__(self, logger_name: str, loglevel=None):
        if logger_name is None:
            logger_name = str(self)
        self.__handler = StreamHandler()
        Logger.__init__(
            self,
            logger_name=logger_name,
            handler=self.__handler,
            loglevel=loglevel
        )

    def close(self):
        self.__handler.close()
        super(StreamLogger, self).close_handler(self.__handler)


class FileLogger(Logger):

    """ディスク上のファイルにログを出力するロガーを提供するクラス."""
    def __init__(self, filename: str, logger_name: str, loglevel=None):
        if logger_name is None:
            logger_name = str(self)
        self.filename = filename
        self.__handler = FileHandler(filename=self.filename, mode='a+')
        Logger.__init__(
            self,
            logger_name=logger_name,
            handler=self.__handler,
            loglevel=loglevel)

    def close(self):
        self.__handler.close()
        super(FileLogger, self).close_handler(self.__handler)


class RotationLogger(Logger):
    """ディスク上のファイルにログを出力するロガーを提供するクラス.
    ローテーション機能を持つ.
    """
    # backup generation count.
    # use set_backupCount() to change this variable.
    backupCount = 3

    def __init__(
        self,
        filename: str,
        logger_name: str=None,
        bcount=None,
        max_bytes=0,
        loglevel=None,
        is_change_fname=False
    ):
        """constructor
        Args:
            positional:
                filename[str]: log file name.
            optional:
                bcount[int]: generation control count for backup log files.
                    default is 3 gen. for example, <basefilename>.1 ~ .3
                logger_name[str]: logger name. instance repl by default.
                max_bytes[int]: done the rotation by using file size(bytes)
                loglevel[int]: log level of the this logger.
                    the default value, dependent on the parent class.
                is_change_fname[bool]: enable namer() function which is called
                    when be rotated the log file.
        """
        self.bcount = bcount
        self.filename = filename
        self.max_bytes = max_bytes
        self.is_change_fname = is_change_fname

        if logger_name is None:
            logger_name = str(self)
        if self.bcount is None:
            self.bcount = RotationLogger.backupCount

        self.__handler = RotatingFileHandler(filename=filename,
                                        mode='a+',
                                        backupCount=self.bcount,
                                        maxBytes=self.max_bytes)
        if self.is_change_fname:
            self.__handler.namer = self.namer
        Logger.__init__(
            self,
            logger_name=logger_name,
            handler=self.__handler,
            loglevel=loglevel
        )

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

    def close(self):
        self.__handler.close()
        super(RotationLogger, self).close_handler(self.__handler)
