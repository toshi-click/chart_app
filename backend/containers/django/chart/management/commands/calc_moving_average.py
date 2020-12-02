from django.core.management.base import BaseCommand

from chart.models import Company

import logging
from concurrent.futures import ProcessPoolExecutor
import datetime as dt
from django.utils.timezone import make_aware

from chart.application.calc.moving_average import MovingAverageCalc

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger('django')

        # DBから対象の株価コードを取得する
        companies = Company.objects.all()
        with ProcessPoolExecutor(max_workers=5000) as excuter:
            for company in companies:
                # 登録株価コード分回す
                excuter.map(MovingAverageCalc.create_moving_average(company.code))
