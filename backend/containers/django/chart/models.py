from django.db import models

# Create your models here.
class Company(models.Model):
    code = models.IntegerField("銘柄コード", primary_key=True)
    name = models.CharField("会社名", max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        # DB内で使用するテーブル名
        db_table = 'company_table'
        # Adminサイトで表示するテーブル名
        verbose_name_plural = 'company_table'

    # Company モデルが直接呼び出された時に返す値を定義
    def __str__(self):
        # 会社名を返す
        return self.name

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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
