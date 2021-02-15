from django.test import TestCase
from django.urls import reverse, resolve
from ..views import IndexView

class TestUrls(TestCase):

    """index ページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_post_index_url(self):
        view = resolve('/chart/')
        self.assertEqual(view.func.view_class, IndexView)
