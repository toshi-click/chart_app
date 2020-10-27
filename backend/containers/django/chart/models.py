from django.db import models

# Create your models here.
class Company(models.Model):
    code = models.IntegerField("銘柄コード", primary_key=True)
    name = models.CharField("会社名", max_length=200)

class RawPrices(models.Model):
    code = models.IntegerField("銘柄コード")
    date = models.DateField("日付")
    datetime = models.DateTimeField("日時")
    open_price = models.IntegerField("始値")
    close_price = models.IntegerField("終値")
    high_price = models.IntegerField("高値")
    low_price = models.IntegerField("安値")
    volume = models.IntegerField("出来高")
    adjustment_close_price = models.FloatField("調整後終値")
    moving_averages25 = models.FloatField("25日移動平均線")
    moving_averages75 = models.FloatField("75日移動平均線")
