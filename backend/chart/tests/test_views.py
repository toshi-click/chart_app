# from django.test import TestCase
# from django.urls import reverse
# import logging
#
# class IndexTests(TestCase):
#     """IndexViewのテストクラス"""
#
#     def test_get(self):
#         """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
#         # ロガーインスタンスを取得
#         logger = logging.getLogger('django')
#         # エラーメッセージをログ出力
#         logger.info(reverse('chart:'))
#
#         response = self.client.get(reverse('chart:'))
#         self.assertEqual(response.status_code, 200)
