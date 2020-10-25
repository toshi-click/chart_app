from django.test import TestCase
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

    def test_saving_and_retrieving_post(self):
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
