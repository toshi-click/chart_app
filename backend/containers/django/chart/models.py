from django.db import models
import datetime as dt


# Create your models here.
class Company(models.Model):
    data_date = models.CharField("データ作成日時", max_length=30)
    code = models.IntegerField("銘柄コード", primary_key=True)
    name = models.CharField("会社名", max_length=200)
    market_products_kubun = models.CharField("市場・商品区分", max_length=200)
    industries_code = models.IntegerField("業種コード", blank=True, null=True)
    industries_kubun = models.CharField("業種区分", max_length=200)
    detailed_industries_code = models.IntegerField("詳細業種コード", blank=True, null=True)
    detailed_industries_kubun = models.CharField("詳細業種区分", max_length=200)
    scale_code = models.IntegerField("規模コード", blank=True, null=True)
    scale_kubun = models.CharField("規模区分", max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    open_price = models.IntegerField("始値")
    close_price = models.IntegerField("終値")
    high_price = models.IntegerField("高値")
    low_price = models.IntegerField("安値")
    volume = models.IntegerField("出来高")
    moving_averages5 = models.FloatField("5日移動平均線", null=True)
    moving_averages25 = models.FloatField("25日移動平均線", null=True)
    moving_averages75 = models.FloatField("75日移動平均線", null=True)
    moving_averages100 = models.FloatField("100日移動平均線", null=True)
    moving_averages200 = models.FloatField("200日移動平均線", null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # 銘柄コードと日付で複合ユニーク成約
        # https://mizzsugar.hatenablog.com/?page=1561192506
        constraints = [
            # 同じ銘柄コードと日付を重複させない
            models.UniqueConstraint(fields=['code', 'date'], name='unique_booking'),
        ]

    @classmethod
    def check_duplicate(cls, code: int, date: dt.date) -> bool:
        # 同じ日に同じ銘柄コードがすでにDBに登録されているかどうかを判定します
        # 登録されていたらTrue, されていなかったらFalseを返します。
        return cls.objects.filter(code=code, date=date).exists()
