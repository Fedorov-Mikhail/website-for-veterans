# your_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import (
    HeroBlock, GovernorBlock, AboutBlock, ContactInfo,
    TeamMember, Goal, FAQ, Project, Event, Video, News
)

# Контекстный процессор для глобальных данных (чтобы хедер был на всех страницах)
def global_context(request):
    """Данные, которые нужны на всех страницах (хедер)"""
    return {
        'contacts': ContactInfo.objects.first(),
    }

def home(request):
    """Главная страница"""
    context = {
        'hero': HeroBlock.objects.first(),
        'governor': GovernorBlock.objects.first(),
        'about': AboutBlock.objects.first(),
        'team': TeamMember.objects.all(),
        'goals': Goal.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True),
        'projects': Project.objects.all(),
        'events': Event.objects.all(),
        'videos': Video.objects.all(),
        'news': News.objects.all()[:6],  # последние 6 новостей
        'contacts': ContactInfo.objects.first(),  # для контактов на главной
    }
    return render(request, 'main/home.html', context)

def news_detail(request, slug):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, slug=slug)
    context = {
        'news': news_item,
        'contacts': ContactInfo.objects.first(),
    }
    return render(request, 'main/news_detail.html', context)

def video_list(request):
    """Страница со всеми видео"""
    videos = Video.objects.all().order_by('-id')
    return render(request, 'main/video_list.html', {'videos': videos})