from django.test import TestCase
from django.urls import reverse
import logging

class IndexTests(TestCase):
    """IndexViewのテストクラス"""

    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        logger = logging.getLogger('development')
        logger.error(reverse('chart:'))
        response = self.client.get(reverse('chart:'))
        self.assertEqual(response.status_code, 200)
