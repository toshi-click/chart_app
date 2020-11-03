from django.urls import path
from . import views

urlpatterns = [
    path('chart/', views.IndexView.as_view()),
    path('chart/chart', views.ChartView.as_view()),
]
