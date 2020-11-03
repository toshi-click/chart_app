from django.core.management.base import BaseCommand
from ..get_price import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        df_t = get_price_time_designation('20200620', '20200625', '3769.jp')

