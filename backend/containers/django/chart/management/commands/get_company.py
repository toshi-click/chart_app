# 東証から銘柄を取得する
from django.core.management.base import BaseCommand
import datetime as dt
from django.utils.timezone import make_aware
import logging
from chart.models import Company
import pandas as pd
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        # df_t = get_price_time_designation('20200620', '20200625', '3769.jp')
        # ロガーインスタンスを取得
        logger = logging.getLogger('django')
        # エラーメッセージをログ出力
        # logger.info(df_t)
        # JPXの東証上場一覧のページへのアクセス
        dls = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
        resp = requests.get(dls)

        output = open('company.xls', 'wb')
        output.write(resp.content)
        output.close()

        # pandasでexcelファイルの読み込みとdf整形など
        df = pd.read_excel('company.xls')
        df = df.drop(1, axis=0)
        df.columns = ['date','code','name','market_products_kubun','industries_code','industries_kubun', 'detailed_industries_code', 'detailed_industries_kubun', 'scale_code', 'scale_kubun']
        company = Company()

        for index, item in df.iterrows():
            company.code = item['code']
            company.name = item['name']
            company.market_products_kubun = item['market_products_kubun']
            if item['industries_code'] != '-':
                company.industries_code = item['industries_code']
            company.industries_kubun = item['industries_kubun']
            if item['detailed_industries_code'] != '-':
                company.detailed_industries_code = item['detailed_industries_code']
            company.detailed_industries_kubun = item['detailed_industries_kubun']
            if item['scale_code'] != '-':
                company.scale_code = item['scale_code']
            company.scale_kubun = item['scale_kubun']
            company.created = make_aware(dt.datetime.now())
            company.updated = make_aware(dt.datetime.now())
            company.save()
