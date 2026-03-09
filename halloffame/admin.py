from django.contrib import admin
from .models import Graduate, GraduateContact

class ContactInline(admin.TabularInline):
    model = GraduateContact
    extra = 1
    class Media:
        js = ('admin/js/contact_admin.js',)

@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group', 'graduation_year', 'status')
    inlines = [ContactInline]
    list_filter = ('graduation_year', 'group')
    search_fields = ('full_name', 'group', 'current_work_place', 'vkr_theme')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'photo', 'short_info', 'description',)
        }),
        ('Учёба и выпуск', {
            'fields': (('graduation_year', 'graduation_month'), 'group', 'vkr_theme', 'scientific_supervisor')
        }),
        ('Карьера и навыки', {
            'fields': ('specialization', 'status', 'key_skills', 'achievements')
        }),
    )