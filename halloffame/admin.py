from django.contrib import admin
from .models import Graduate

@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group', 'graduation_year', 'specialization')
    list_filter = ('graduation_year', 'group')
    search_fields = ('full_name', 'group', 'specialization')
    ordering = ('-graduation_year', 'full_name')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'group', 'photo')
        }),
        ('Даты выпуска', {
            'fields': ('graduation_year', 'graduation_month')
        }),
        ('Профессиональная информация', {
            'fields': ('specialization', 'description')
        }),
    )
