from rest_framework import generics, permissions
from .models import Snippet
from django.contrib.auth.models import User
from .serializers import SnippetSerializer, UserSerializer, StockSerializer
from .permissions import IsOwnerOrReadOnly

from chart.models import RawPrices
from chart.models import Company

class StockList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    # 一旦1306固定で最新30件取得する
    queryset = RawPrices.objects.filter(code=1306).order_by('date').reverse().all()[:30]
    serializer_class = StockSerializer

class SnippetList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
