# coding:utf-8

import logging
import re

from django.utils.translation import gettext

class StringHelper:

    @staticmethod
    def convert_string_to_float(text):
        """
        文字列を数値(float)に変換する
        """
        try:
            num = float(text)
        except ValueError as e:
            logging.warning(gettext("W800"), text, "-", e)
            raise e
        return num

    @staticmethod
    def convert_string_to_int(text):
        """
        文字列を数値(int)に変換する
        """
        try:
            num = int(text)
        except ValueError as e:
            raise e
        return num

    @staticmethod
    def re_space(text):
        """
        全角を含む空白文字を除去する
        """
        text = re.sub('　', '', text)
        text = re.sub(' ', '', text)
        return text
