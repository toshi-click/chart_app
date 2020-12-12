from django.shortcuts import render
from django.views import generic, View
import logging

# 株価描画
from chart.models import RawPrices
import pandas as pd
import mplfinance as mpf

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
index_page = IndexView.as_view()

class ChartView(View):
    def get(self, request, *args, **kwargs):
        l = logging.getLogger('django.db.backends')
        l.setLevel(logging.DEBUG)
        l.addHandler(logging.StreamHandler())
        chart = RawPrices.objects.filter(code=1306).order_by('date').reverse().all()[:30]
        chart[:30]
        #df = pd.DataFrame(list(RawPrices.objects.filter(code=1306).order_by('date').values()))
        return render(request, 'chart.html', {'chart': chart})
