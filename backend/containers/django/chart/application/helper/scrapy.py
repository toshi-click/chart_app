# coding:utf-8
import logging
import socket
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
from django.utils.translation import gettext

from pypeach_django.app_config import AppConfig

"""
Scrapy関連の共通処理を定義する
"""


class ScrapyHelper:

    @staticmethod
    def get_html(url, parse_flag=None):
        """
        scrapyを行いhtmlを取得する
        """
        # User-Agentを定義する
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/55.0.2883.95 Safari/537.36 '
        # アクセスのリトライ回数を指定する
        retry_max_count = AppConfig.get_properties("url_request_retry_max_count")
        response_html = None
        for i in range(0, retry_max_count):
            try:
                # Webアクセス時のUser-Agentを指定する
                logging.debug("request settings")
                req = urllib.request.Request(url, headers={'User-Agent': ua})
                # Webアクセスの読み込みを行う
                logging.debug("request read start")
                with urllib.request.urlopen(req, timeout=AppConfig.get_properties("url_request_read_timeout")) as f:
                    html = f.read().decode('utf-8')
                logging.debug("request read end")

                # レスポンスをHTMLパーサーでパースする
                logging.debug("request parse start")
                if parse_flag is True:
                    response_html = BeautifulSoup(html, 'lxml')
                else:
                    response_html = html
                logging.debug("request parse end")

                if response_html is not None and len(response_html) > 0:
                    break
            except HTTPError as e:
                # HTTPError時のメッセージを出力する
                logging.info(gettext("I801"), url, e.code, e.msg)
            except URLError as error:
                # タイムアウトを判定する
                if isinstance(error.reason, socket.timeout):
                    logging.info(gettext("I802"), url)
                else:
                    logging.info(gettext("E991"), error.reason)
                    raise URLErrorException(gettext("E990") % url)
            except socket.timeout:
                logging.info(gettext("I802"), url)
            except ConnectionResetError as error:
                # [Errno 104] Connection reset by peerを回避する
                logging.info(gettext("I802"), url)
            except Exception as error:
                logging.info(gettext("E991"), error)
                raise ScrapyIllegalException(gettext("E990") % url)

        # レスポンスがない場合はExceptionにする
        if response_html is None:
            error_msg = "{}:{}".format(gettext("E803"), url)
            raise HttpErrorException(error_msg)
        return response_html

    @staticmethod
    def is_exists_class_name(html, class_name):
        """
        html内のクラス有無をチェックする
        """
        is_exists_flag = False
        try:
            # class有無を判定する
            if len(html.select('.' + class_name)) > 0 or class_name in html["class"]:
                is_exists_flag = True
        except (KeyError, AttributeError):
            # エラーの場合はfalseを返却する
            pass
        return is_exists_flag

    @staticmethod
    def get_url_parameter(url, parameter_name):
        """
        URLのパラメータ値を取得する
        """
        try:
            # URLをパースして指定されたパラメータ名を取得する
            url_parse = urlparse(url)
            url_query = parse_qs(url_parse.query)
            value = url_query[parameter_name][0]
        except KeyError as e:
            # エラーの場合はログを出力してNoneを返却する
            logging.debug(gettext("W801"), e)
            return None
        return value


class HttpErrorException(Exception):
    """
    Exception(httpエラー)を定義する
    """
    pass


class URLErrorException(Exception):
    """
    Exception(サーバ接続エラー)を定義する
    """
    pass


class ScrapyIllegalException(Exception):
    """
    Exception(その他エラー)を定義する
    """
    pass
