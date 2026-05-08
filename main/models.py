from django.db import models
from django.utils import timezone
import re

# ============================================
# АБСТРАКТНЫЕ БАЗОВЫЕ МОДЕЛИ
# ============================================

class BaseContent(models.Model):
    """Абстрактная базовая модель с общими полями"""
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='images/', blank=True, null=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title


# ============================================
# БЛОКИ ГЛАВНОЙ СТРАНИЦЫ (ЕДИНСТВЕННЫЕ ЭКЗЕМПЛЯРЫ)
# ============================================

class HeroBlock(models.Model):
    """Главный экран с кнопками"""
    title = models.CharField('Заголовок', max_length=200, default='Вместе поможем')
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    background_image = models.ImageField('Фоновое изображение', upload_to='hero/')
    button1_text = models.CharField('Текст первой кнопки', max_length=50, default='Присоединиться')
    button1_link = models.CharField('Ссылка первой кнопки', max_length=200, default='#')
    button2_text = models.CharField('Текст второй кнопки', max_length=50, default='Связаться')
    button2_link = models.CharField('Ссылка второй кнопки', max_length=200, default='#contacts')
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Главный блок'
        verbose_name_plural = 'Главный блок'
    
    def __str__(self):
        return 'Главный экран'


class GovernorBlock(models.Model):
    """Блок с губернатором (можно включить/выключить)"""
    is_enabled = models.BooleanField('Показывать блок', default=False)
    name = models.CharField('ФИО', max_length=200, default='Андрей Воробьёв')
    position = models.CharField('Должность', max_length=200, default='Губернатор Московской области')
    quote = models.TextField('Цитата')
    image = models.ImageField('Фотография', upload_to='governor/')
    
    class Meta:
        verbose_name = 'Блок губернатора'
        verbose_name_plural = 'Блок губернатора'
    
    def __str__(self):
        return f'Блок губернатора ({ "включен" if self.is_enabled else "выключен" })'


class AboutBlock(models.Model):
    """Блок 'О нас'"""
    title = models.CharField('Заголовок', max_length=200, default='О нас')
    content = models.TextField('Текст')
    
    class Meta:
        verbose_name = 'Блок "О нас"'
        verbose_name_plural = 'Блок "О нас"'
    
    def __str__(self):
        return 'Блок "О нас"'


class ContactInfo(models.Model):
    """Контактная информация и карта"""
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=300)
    map_coordinates = models.CharField(
        'Координаты карты', 
        max_length=100, 
        blank=True,
        help_text='Например: 55.751244,37.618423'
    )
    map_zoom = models.PositiveSmallIntegerField('Масштаб карты', default=12)
    work_time = models.CharField('Время работы', max_length=200, default='Пн-Пт: 9:00-18:00')
    
    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'
    
    def __str__(self):
        return 'Контактная информация'


class Phone(models.Model):
    """Телефон для связи"""
    PHONE_TYPES = (
        ('main', 'Основной'),
        ('hotline', 'Горячая линия'),
        ('fax', 'Факс'),
        ('other', 'Дополнительный'),
    )
    
    contact_info = models.ForeignKey(
        ContactInfo, 
        on_delete=models.CASCADE,
        related_name='phones',
        verbose_name='Контактная информация'
    )
    number = models.CharField('Номер телефона', max_length=20)
    type = models.CharField('Тип', max_length=20, choices=PHONE_TYPES, default='other')
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.number}"


# ============================================
# КОЛЛЕКЦИОННЫЕ БЛОКИ (МНОГО ЭКЗЕМПЛЯРОВ)
# ============================================

class TeamMember(models.Model):
    """Член руководства"""
    name = models.CharField('ФИО', max_length=200)
    position = models.CharField('Должность', max_length=200)
    bio = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фотография', upload_to='team/')
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Член руководства'
        verbose_name_plural = 'Руководство'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Goal(models.Model):
    """Цель организации"""
    title = models.CharField('Название цели', max_length=200)
    description = models.TextField('Описание')
    icon = models.ImageField('Иконка', upload_to='goals/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Наши цели'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Вопрос-ответ"""
    question = models.CharField('Вопрос', max_length=300)
    answer = models.TextField('Ответ')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'FAQ'
        ordering = ['order']
    
    def __str__(self):
        return self.question


# ============================================
# ОСНОВНОЙ КОНТЕНТ (НОВОСТИ, ПРОЕКТЫ, МЕРОПРИЯТИЯ, ВИДЕО)
# ============================================

class Project(BaseContent):
    """Проект"""
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Event(BaseContent):
    """Мероприятие"""
    date = models.DateField('Дата проведения')
    description = models.TextField('Описание')
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-date']

class Video(models.Model):
    title = models.CharField('Название', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    video_url = models.URLField('Ссылка на видео')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.title

    def embed_url(self):
        url = self.video_url
        if not url:
            return ''

        # 1. VK Video (новый домен vkvideo.ru)
        vk_video_pattern = r'vkvideo\.ru/video-?(\d+)_(\d+)'
        match = re.search(vk_video_pattern, url)
        if match:
            oid = match.group(1)  # ID сообщества
            vid = match.group(2)  # ID видео
            return f'https://vkvideo.ru/video_ext.php?oid=-{oid}&id={vid}&hd=3'

        # 2. VK Video (старый домен vk.com)
        vk_com_pattern = r'vk\.com/video-?(\d+)_(\d+)'
        match = re.search(vk_com_pattern, url)
        if match:
            oid = match.group(1)
            vid = match.group(2)
            return f'https://vkvideo.ru/video_ext.php?oid=-{oid}&id={vid}&hd=3'

        # 3. YouTube (youtube.com/watch?v=... или youtu.be/...)
        yt_pattern = r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)'
        match = re.search(yt_pattern, url)
        if match:
            return f'https://www.youtube.com/embed/{match.group(1)}'

        # 4. RuTube
        rt_pattern = r'(?:rutube\.ru/video/)([\w-]+)'
        match = re.search(rt_pattern, url)
        if match:
            return f'https://rutube.ru/play/embed/{match.group(1)}'

        # Если ничего не распознано – вернуть исходную ссылку (может не работать)
        return url


class News(BaseContent):
    """Новость"""
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    date = models.DateTimeField('Дата публикации', default=timezone.now)
    content = models.TextField('Полный текст')
    slug = models.SlugField('URL', unique=True, blank=True)
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
class SiteContent(models.Model):
    """Настройки текстов всех блоков на сайте (одна запись)"""

    # Блок «Главный экран» (Hero) - если не хотите хранить в HeroBlock
    hero_title = models.CharField('Заголовок', max_length=200, default='Вместе на передовой - вместе в мирной жизни')
    hero_subtitle = models.TextField('Подзаголовок', blank=True, default='Объединение участников СВО и ветеранов боевых действий...')
    hero_button1_text = models.CharField('Текст кнопки 1', max_length=50, default='Присоединиться к Ассоциации')
    hero_button2_text = models.CharField('Текст кнопки 2', max_length=50, default='Связаться с нами')

    # Блок «Руководство»
    team_title = models.CharField('Заголовок', max_length=200, default='Руководство Ассоциации')
    team_subtitle = models.CharField('Подзаголовок', max_length=300, blank=True, default='')

    # Блок «Наши цели»
    goals_title = models.CharField('Заголовок', max_length=200, default='Наши цели')
    goals_subtitle = models.CharField('Подзаголовок', max_length=500, default='Ассоциация ветеранов СВО создана для защиты прав и всесторонней поддержки...')

    # Блок «Наши проекты»
    projects_title = models.CharField('Заголовок', max_length=200, default='Наши проекты')
    projects_subtitle = models.CharField('Подзаголовок', max_length=500, default='Социальные, спортивные и культурные события, объединяющие ветеранов Московской области')

    # Блок «Анонс мероприятий»
    events_title = models.CharField('Заголовок', max_length=200, default='Анонс мероприятий')
    events_subtitle = models.CharField('Подзаголовок', max_length=500, default='Присоединяйтесь к нашим событиям - участвуйте, общайтесь, находите поддержку')

    # Блок «Видеогалерея»
    videos_title = models.CharField('Заголовок', max_length=200, default='Видеогалерея')
    videos_subtitle = models.CharField('Подзаголовок', max_length=500, default='Истории ветеранов, репортажи с мероприятий и важные обращения')
    videos_all_button_text = models.CharField('Текст кнопки "Все видео"', max_length=50, default='Посмотреть все видео')

    # Блок «Новости»
    news_title = models.CharField('Заголовок', max_length=200, default='Новости')
    news_subtitle = models.CharField('Подзаголовок', max_length=500, default='Актуальные события и последние новости из жизни Ассоциации ветеранов СВО')

    # Блок «FAQ»
    faq_title = models.CharField('Заголовок', max_length=200, default='Часто задаваемые вопросы')

    # Блок «Контакты» (заголовок)
    contacts_title = models.CharField('Заголовок', max_length=200, default='Наши контакты')

    class Meta:
        verbose_name = 'Заголовки информационных блоков'
        verbose_name_plural = 'Заголовки информационных блоков'

    def __str__(self):
        return 'Настройки заголовков сайта'

    def save(self, *args, **kwargs):
        # Ограничиваем создание только одной записи
        if not self.pk and SiteContent.objects.exists():
            raise Exception('Можно создать только одну запись SiteContent')
        super().save(*args, **kwargs)
    