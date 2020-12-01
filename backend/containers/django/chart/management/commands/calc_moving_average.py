from django.core.management.base import BaseCommand
from django.db.models import Avg
from chart.models import Company, RawPrices

import logging

import datetime as dt
from django.utils.timezone import make_aware

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger('django')
        # DBから対象の株価コードを取得する
        companies = Company.objects.all()

        # 登録株価コード分回す
        for company in companies:
            # 株価コードに紐付いた株価時系列データ取得
            raw_prices = RawPrices.objects.filter(code=company.code).order_by('date').all()
            # 株価時系列データ分繰り返す
            for raw_price in raw_prices:
                # 5日分
                count = RawPrices.objects.filter(code=company.code, date__lte=raw_price.date).order_by('date').all()[:200].count()
                avg_query_set = RawPrices.objects.filter(code=company.code, date__lte=raw_price.date).order_by('date').reverse()
                raw_price = RawPrices.objects.filter(code=raw_price.code, date=raw_price.date).first()
                logger.info("code:" + str(company.code) + "   date: " + str(raw_price.date))
                if count >= 5:
                    avg = avg_query_set.all()[:5].aggregate(Avg('close_price'))
                    raw_price.moving_averages5 = avg['close_price__avg']
                # 25日分
                if count >= 25:
                    avg = avg_query_set.all()[:25].aggregate(Avg('close_price'))
                    raw_price.moving_averages25 = avg['close_price__avg']
                # 75日分
                if count >= 75:
                    avg = avg_query_set.all()[:75].aggregate(Avg('close_price'))
                    raw_price.moving_averages75 = avg['close_price__avg']
                # 100日分
                if count >= 100:
                    avg = avg_query_set.all()[:100].aggregate(Avg('close_price'))
                    raw_price.moving_averages100 = avg['close_price__avg']
                # 200日分
                if count >= 200:
                    avg = avg_query_set.all()[:200].aggregate(Avg('close_price'))
                    raw_price.moving_averages200 = avg['close_price__avg']

                raw_price.save()

