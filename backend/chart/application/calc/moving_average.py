# 移動平均を計算するクラスです。
from chart.application.calc.calc_base import CalcBase
import logging
from django.db.models import Avg
from chart.models import RawPrices
from concurrent.futures import ThreadPoolExecutor

class MovingAverageCalc(CalcBase):
    def __init__(self):
        super().__init__()

    def create_moving_average_date(code, date):
        count = RawPrices.objects.filter(code=code, date__lte=date).order_by('date').all()[:200].count()
        avg_query_set = RawPrices.objects.filter(code=code, date__lte=date).order_by('date').reverse()
        raw_price = RawPrices.objects.filter(code=code, date=date).first()
        logger = logging.getLogger('django')
        logger.info("code:" + str(code) + "   date: " + str(raw_price.date))
        # 5日分
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

    def create_moving_average(code):
        """
        それぞれの移動平均を計算する
        """
        # calc = MovingAverageCalc()

        # DBから対象の株価コードを取得する
        # companies = Company.objects.all()

        logger = logging.getLogger('django')
        logger.info("killing_time code:" + str(code))
        # 株価コードに紐付いた株価時系列データ取得
        raw_prices = RawPrices.objects.filter(code=code).order_by('date').all()
        with ThreadPoolExecutor(max_workers=50) as executor:
            # 株価時系列データ分繰り返す
            for raw_price in raw_prices:
                executor.submit(MovingAverageCalc.create_moving_average_date(code, raw_price.date))


