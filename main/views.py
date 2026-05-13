# your_app/views.py
import hashlib
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import BadHeaderError, send_mail
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


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def is_issue_report_rate_limited(request):
    limit = max(1, settings.ISSUE_REPORT_RATE_LIMIT)
    window = max(1, settings.ISSUE_REPORT_RATE_LIMIT_WINDOW)
    client_ip = get_client_ip(request) or 'unknown'
    ip_hash = hashlib.sha256(client_ip.encode('utf-8')).hexdigest()
    cache_key = f'issue-report-rate:{ip_hash}'

    if cache.add(cache_key, 1, timeout=window):
        return False

    try:
        attempts = cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, timeout=window)
        return False

    return attempts > limit


@require_POST
def submit_issue_report(request):
    """Отправляет сообщение о некорректных данных администратору на почту"""
    redirect_url = f'{reverse("main:home")}#feedback'

    if request.POST.get('website'):
        return redirect(redirect_url)

    if is_issue_report_rate_limited(request):
        messages.error(request, 'Слишком много отправок. Попробуйте позже.')
        return redirect(redirect_url)

    form = IssueReportForm(request.POST)
    if form.is_valid():
        problem_type = dict(IssueReportForm.PROBLEM_TYPES)[form.cleaned_data['problem_type']]
        page_url = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        contact = form.cleaned_data['contact'] or 'Не указан'
        body = (
            'На сайте отправлено сообщение о некорректных данных.\n\n'
            f'Тип проблемы: {problem_type}\n'
            f'Описание: {form.cleaned_data["message"]}\n'
            f'Контакт для уточнений: {contact}\n'
            f'Страница отправки: {page_url}\n'
            f'Браузер: {user_agent}\n'
        )

        try:
            send_mail(
                subject='Сообщение о некорректности данных на сайте',
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ISSUE_REPORT_RECIPIENT],
                fail_silently=False,
            )
            messages.success(request, 'Спасибо, сообщение отправлено администратору.')
        except (BadHeaderError, SMTPException, OSError):
            messages.error(request, 'Не удалось отправить сообщение. Попробуйте позже.')
    else:
        messages.error(request, 'Проверьте форму: описание должно быть подробным, а согласие отмечено.')

    return redirect(redirect_url)
