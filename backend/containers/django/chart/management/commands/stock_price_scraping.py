from django.core.management.base import BaseCommand
from ..get_price import *
import logging

class Command(BaseCommand):
    def handle(self, *args, **options):
        df_t = get_price_time_designation('20200620', '20200625', '3769.jp')
        # ロガーインスタンスを取得
        logger = logging.getLogger('django')
        # エラーメッセージをログ出力
        logger.info(df_t)

