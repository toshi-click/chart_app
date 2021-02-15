from rest_framework import serializers
from .models import Snippet
from django.contrib.auth.models import User

from chart.models import RawPrices
from chart.models import Company

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawPrices
        fields = ('code', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume', 'moving_averages5', 'moving_averages25', 'moving_averages75', 'moving_averages100', 'moving_averages200')

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
