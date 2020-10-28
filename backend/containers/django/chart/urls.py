from django.urls import path
from . import views

urlpatterns = [
    path('chart/', views.IndexView.as_view()),
]
