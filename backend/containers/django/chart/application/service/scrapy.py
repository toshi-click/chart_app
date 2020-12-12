import logging

from bs4 import BeautifulSoup
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import localtime

from app_pypeach_django.application.helper.date import DateHelper
from app_pypeach_django.application.helper.scrapy import ScrapyHelper
from app_pypeach_django.application.service.app_logic_base import AppLogicBaseService
from app_pypeach_django.models import ScrapyHtml

"""
Scrapyを行うクラスです。
"""

class ScrapyService(AppLogicBaseService):
    def __init__(self):
        super().__init__()

    # URLの定数
    url = 'http://mocjax.com/example/scrape/'

    @staticmethod
    @transaction.atomic()
    def create_scrapy_html():
        """
        Webページにアクセスしてデータを作成する
        """
        service = ScrapyService()
        service._regist_scrapy_html(service.url)

    @staticmethod
    @transaction.atomic()
    def parse_scrapy_html():
        """
        Webページの結果から要素を抽出する
        """
        service = ScrapyService()

        for item_scrapy_html in ScrapyHtml.objects.filter(request_url=service.url, delete_flag=0):
            # html→lxmlに変換して構文解析を行う
            html_text = item_scrapy_html.html_text
            html_lxml = BeautifulSoup(html_text, 'lxml')
            # selectを使用してheadingをすべて抽出する
            for item_header in html_lxml.select('div.card-header > h4'):
                logging.debug("header_text={}".format(item_header.text))

            # select_oneを使用してbody内のタイトルを先頭1件のみ抽出する
            first_body = html_lxml.select_one('div.card-body > h1')
            logging.debug("item_header_text={}".format(first_body.text))

            # ボタンのクラス有無を判定する
            if ScrapyHelper.is_exists_class_name(html_lxml.select_one('a.btn.btn-primary'), 'btn-lg'):
                logging.debug("exists class:btn-lg")

            # アンカーのパラメータを取得する
            for item_anchor in html_lxml.select('a'):
                href = item_anchor.get('href')
                logging.debug("item_href={}".format(href))
                # アンカー内のパラメータ(id)の値を取得する。パラメータがない場合はNoneになる
                logging.debug("id={}".format(ScrapyHelper.get_url_parameter(href, 'id')))

    def _regist_scrapy_html(self, url):
        """
        Webスクレイピングした結果をテーブルに登録する
        """
        # 同一URLが存在する場合はレコードを削除する
        if ScrapyHtml.objects.filter(request_url=url).count() > 0:
            ScrapyHtml.objects.filter(request_url=url).delete()
        self.regist_model = ScrapyHtml()
        self.regist_model.execute_dt = DateHelper.get_today(DateHelper.format_ymd)
        self.regist_model.request_url = url
        self.regist_model.html_text = ScrapyHelper.get_html(url)
        self.regist_model.delete_flag = 0
        self.regist_model.regist_dt = localtime(timezone.now())
        self.regist_model.update_dt = localtime(timezone.now())
        self.regist_model.save()
        return self.regist_model.id
