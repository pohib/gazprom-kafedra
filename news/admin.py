from django.contrib import admin
from .models import News, NewsImage, NewsSettings
from django.utils.html import format_html

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('image_url', 'crop_position', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="100" height="150" style="object-fit: cover; object-position: {}; border-radius: 4px;" />',
                obj.image_url,
                obj.crop_position if obj.crop_position else 'center'
            )
        return '' 
    image_preview.allow_tags = True
    image_preview.short_description = 'Превью изображения'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published', 'is_title_edited', 'is_body_edited')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'body')
    ordering = ('-date',)
    inlines = [NewsImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'date', 'views', 'is_published', 'source_id', 'is_title_edited', 'is_body_edited', 'auto_title_sentences',)
        }),
    )
    readonly_fields = ('source_id',)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-date')

@admin.register(NewsSettings)
class NewsSettingsAdmin(admin.ModelAdmin):
    list_display = ('news_count',)