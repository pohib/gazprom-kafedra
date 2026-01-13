from django.contrib import admin
from django.db.models import Count
from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'city', 'country', 'created_at', 'session_key']
    list_filter = ['city', 'country', 'created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['ip_address', 'city', 'created_at', 'user_agent', 'session_key']

    def changelist_view(self, request, extra_context=None):
        city_stats = Visit.objects.values('city').annotate(
            count=Count('city')
        ).order_by('-count')[:10]
        
        extra_context = extra_context or {}
        extra_context['city_stats'] = city_stats
        return super().changelist_view(request, extra_context=extra_context)