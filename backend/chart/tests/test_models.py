from django.test import TestCase
from datetime import datetime, date
from django.utils.timezone import make_aware
from ..models import Company, RawPrices


class CompanyModelTests(TestCase):
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_companys = Company.objects.all()
        self.assertEqual(saved_companys.count(), 0)

    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        company = Company(code=1, name='test_text')
        company.save()
        saved_companys = Company.objects.all()
        self.assertEqual(saved_companys.count(), 1)

    def test_saving_and_retrieving_company(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        company = Company()
        code = 2
        name = 'test_text2'
        company.code = code
        company.name = name
        company.save()

        saved_companys = Company.objects.all()
        actual_company = saved_companys[0]

        self.assertEqual(actual_company.code, code)
        self.assertEqual(actual_company.name, name)


class RawPricesModelTests(TestCase):
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_raw_prices = RawPrices.objects.all()
        self.assertEqual(saved_raw_prices.count(), 0)

    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        raw_prices = RawPrices(code=1, date=date.today(), datetime=make_aware(datetime.now()), open_price=1,
                               close_price=2, high_price=3, low_price=1,
                               volume=100, adjustment_close_price=2, moving_averages25=0.0, moving_averages75=0.0)
        raw_prices.save()
        saved_raw_prices = RawPrices.objects.all()
        self.assertEqual(saved_raw_prices.count(), 1)

    def test_saving_and_retrieving_raw_prices(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        raw_prices = RawPrices()
        code = 2
        dated = date.today()
        datetimed = make_aware(datetime.now())
        open_price = 2
        close_price = 6
        high_price = 10
        low_price = 1
        volume = 1000
        adjustment_close_price = 6
        moving_averages25 = 1.0
        moving_averages75 = 2.0
        raw_prices.code = code
        raw_prices.date = dated
        raw_prices.datetime = datetimed
        raw_prices.open_price = open_price
        raw_prices.close_price = close_price
        raw_prices.high_price = high_price
        raw_prices.low_price = low_price
        raw_prices.volume = volume
        raw_prices.adjustment_close_price = adjustment_close_price
        raw_prices.moving_averages25 = moving_averages25
        raw_prices.moving_averages75 = moving_averages75
        raw_prices.save()

        saved_raw_prices = RawPrices.objects.all()
        actual_raw_prices = saved_raw_prices[0]

        self.assertEqual(actual_raw_prices.code, code)
        self.assertEqual(actual_raw_prices.date, dated)
        self.assertEqual(actual_raw_prices.datetime, datetimed)
        self.assertEqual(actual_raw_prices.open_price, open_price)
        self.assertEqual(actual_raw_prices.close_price, close_price)
        self.assertEqual(actual_raw_prices.high_price, high_price)
        self.assertEqual(actual_raw_prices.low_price, low_price)
        self.assertEqual(actual_raw_prices.volume, volume)
        self.assertEqual(actual_raw_prices.adjustment_close_price, adjustment_close_price)
        self.assertEqual(actual_raw_prices.moving_averages25, moving_averages25)
        self.assertEqual(actual_raw_prices.moving_averages75, moving_averages75)
