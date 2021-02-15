from django.core.management.base import BaseCommand
from django.conf import settings

import logging

from chart.models import RawPrices

import os
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_dir = settings.MEDIA_ROOT + '/stock'
        csv_files = os.listdir(csv_dir)
        logger = logging.getLogger('django')

        # csvファイルの数だけfor分を回す.
        for i in range(len(csv_files)):
            # i個目のファイルの読み込み
            csv_file = pd.read_csv(csv_dir + '/' + str(csv_files[i]), engine='python')
            # 1行目はカラムがあるので除去する
            #df = csv_file.drop(1, axis=0)
            for index, item in csv_file.iterrows():
                logger.info("code:" + str(item['Code']) + "   date: " + str(item['Date']))
                if RawPrices.check_duplicate(code=item['Code'], date=item['Date']):
                    raw_price = RawPrices.objects.filter(code=item['Code'], date=item['Date']).first()
                else:
                    raw_price = RawPrices()
                    raw_price.code = item['Code']
                    raw_price.date = item['Date']

                raw_price.open_price = item['Open']
                raw_price.close_price = item['Close']
                raw_price.high_price = item['High']
                raw_price.low_price = item['Low']
                raw_price.volume = item['Volume']

                # ここで移動平均値を計算する

                raw_price.save()
