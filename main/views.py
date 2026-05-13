# your_app/views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import IssueReportForm
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


@require_POST
def submit_issue_report(request):
    """Сохраняет сообщение о некорректных данных из формы на главной"""
    redirect_url = f'{reverse("main:home")}#feedback'

    if request.POST.get('website'):
        return redirect(redirect_url)

    form = IssueReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.page_url = request.META.get('HTTP_REFERER', '')[:500]
        report.user_agent = request.META.get('HTTP_USER_AGENT', '')[:300]
        report.save()
        messages.success(request, 'Спасибо, сообщение отправлено администратору.')
    else:
        messages.error(request, 'Проверьте форму: описание должно быть подробным, а согласие отмечено.')

    return redirect(redirect_url)
