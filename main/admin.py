from django.contrib import admin
from .models import (
    HeroBlock, GovernorBlock, AboutBlock, ContactInfo, Phone,
    TeamMember, Goal, FAQ, Project, Event, Video, News, SiteContent
)

# ============================================
# INLINE МОДЕЛИ (ДЛЯ СВЯЗАННЫХ ДАННЫХ)
# ============================================

class PhoneInline(admin.TabularInline):
    """Телефоны для контактной информации"""
    model = Phone
    extra = 1
    fields = ['number', 'type', 'order']
    ordering = ['order']


# ============================================
# МОДЕЛИ С ЕДИНСТВЕННЫМ ЭКЗЕМПЛЯРОМ (БЛОКИ ГЛАВНОЙ)
# ============================================

@admin.register(HeroBlock)
class HeroBlockAdmin(admin.ModelAdmin):
    """Главный экран с кнопками"""
    fieldsets = (
        ('Основной контент', {
            'fields': ('title', 'subtitle', 'background_image')
        }),
        ('Кнопки', {
            'fields': ('button1_text', 'button1_link', 'button2_text', 'button2_link')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        """Запрещаем создавать больше одного экземпляра"""
        if HeroBlock.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление (можно только деактивировать)"""
        return False


@admin.register(GovernorBlock)
class GovernorBlockAdmin(admin.ModelAdmin):
    """Блок с губернатором (опциональный)"""
    list_display = ['is_enabled', 'name', 'position']
    fieldsets = (
        ('Видимость', {
            'fields': ('is_enabled',)
        }),
        ('Содержание', {
            'fields': ('name', 'position', 'quote', 'image')
        }),
    )
    
    def has_add_permission(self, request):
        if GovernorBlock.objects.exists():
            return False
        return True


@admin.register(AboutBlock)
class AboutBlockAdmin(admin.ModelAdmin):
    """Блок 'О нас'"""
    fields = ['title', 'content']
    
    def has_add_permission(self, request):
        if AboutBlock.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Контактная информация и карта"""
    inlines = [PhoneInline]
    fieldsets = (
        ('Контакты', {
            'fields': ('email', 'address', 'work_time')
        }),
        ('Карта', {
            'fields': ('map_coordinates', 'map_zoom'),
            'classes': ('collapse',),
            'description': 'Координаты можно скопировать из Яндекс.Карт или Google Maps'
        }),
    )
    
    def has_add_permission(self, request):
        if ContactInfo.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False


# ============================================
# КОЛЛЕКЦИОННЫЕ МОДЕЛИ (МНОГО ЭКЗЕМПЛЯРОВ)
# ============================================

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Члены руководства"""
    list_display = ['name', 'position', 'order']
    list_editable = ['order']
    list_filter = ['position']
    search_fields = ['name', 'position', 'bio']
    fields = ['name', 'position', 'bio', 'photo', 'order']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """Цели организации"""
    list_display = ['title', 'order']
    list_editable = ['order']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'icon', 'order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Вопросы-ответы"""
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    fields = ['question', 'answer', 'order', 'is_active']


# ============================================
# ОСНОВНОЙ КОНТЕНТ
# ============================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Проекты"""
    list_display = ['title', 'id']
    search_fields = ['title', 'subtitle']
    fields = ['title', 'subtitle', 'image']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Мероприятия"""
    list_display = ['title', 'date', 'id']
    list_filter = ['date']
    search_fields = ['title', 'description']
    fields = ['title', 'image', 'date', 'description']
    date_hierarchy = 'date'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Видео"""
    list_display = ['title', 'id']
    search_fields = ['title', 'subtitle']
    fields = ['title', 'subtitle', 'video_url']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Новости (с отдельной страницей)"""
    prepopulated_fields = {'slug': ('title',)}  # Автогенерация slug из заголовка
    list_display = ['title', 'date', 'slug', 'id']
    list_filter = ['date']
    search_fields = ['title', 'subtitle', 'content']
    fields = ['title', 'subtitle', 'image', 'date', 'content', 'slug']
    date_hierarchy = 'date'

    
@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Главный экран', {'fields': ('hero_title', 'hero_subtitle', 'hero_button1_text', 'hero_button2_text')}),
        ('Руководство', {'fields': ('team_title', 'team_subtitle')}),
        ('Наши цели', {'fields': ('goals_title', 'goals_subtitle')}),
        ('Наши проекты', {'fields': ('projects_title', 'projects_subtitle')}),
        ('Анонс мероприятий', {'fields': ('events_title', 'events_subtitle')}),
        ('Видеогалерея', {'fields': ('videos_title', 'videos_subtitle', 'videos_all_button_text')}),
        ('Новости', {'fields': ('news_title', 'news_subtitle')}),
        ('FAQ', {'fields': ('faq_title',)}),
        ('Контакты', {'fields': ('contacts_title',)}),
    )