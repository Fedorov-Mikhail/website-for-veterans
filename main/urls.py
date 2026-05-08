# your_app/urls.py
from django.urls import path
from . import views

app_name = 'main' 

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Детальная страница новости (по slug)
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('videos/', views.video_list, name='video_list'),
]