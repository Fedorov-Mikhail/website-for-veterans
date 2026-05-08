# your_app/context_processors.py
from .models import ContactInfo, SiteContent

def global_context(request):
    """Глобальные данные для всех шаблонов"""
    return {
        'contacts': ContactInfo.objects.first(),
    }

def site_content(request):
    return {'site_content': SiteContent.objects.first()}