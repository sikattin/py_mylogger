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
from logging import getLogger, StreamHandler, Formatter, WARNING, DEBUG, INFO


class Logger(object):
    """ロガーを生成するクラス."""

    loglevel = WARNING

    def __new__(cls, logger_name: str):
        """コンストラクタ

        Args:
            param1 logger_name: ロガーの名前.

        Returns:
            作成したロガー.
        """
        self = super().__new__(cls)
        # ロガー作成.
        self._logger = getLogger(logger_name)
        self._logger.setLevel(self.loglevel)
        # ハンドラの作成.
        ch = StreamHandler()
        ch.setLevel(self.loglevel)
        # フォーマッターの作成.
        formatter = Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        # ロガーにコンソールハンドラを追加.
        self._logger.addHandler(ch)
        # ログを他の名前空間に伝播させないように.
        self._logger.propagate = False
        return self

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
