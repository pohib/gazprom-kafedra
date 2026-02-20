from django.contrib import admin
from django.db.models import Count
from .models import Visit, PlanEvent
from django.db import models
from django import forms
from django.utils import timezone

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
    

class PlanEventAdminForm(forms.ModelForm):
    class Meta:
        model = PlanEvent
        fields = '__all__'
        widgets = {
            'month1': forms.TextInput(attrs={'size': 8}),
            'month2': forms.TextInput(attrs={'size': 8}),
            'month3': forms.TextInput(attrs={'size': 8}),
            'month4': forms.TextInput(attrs={'size': 8}),
            'month5': forms.TextInput(attrs={'size': 8}),
            'month6': forms.TextInput(attrs={'size': 8}),
            'day1': forms.NumberInput(attrs={'min': 1, 'max': 31, 'style': 'width:60px'}),
            'day2': forms.NumberInput(attrs={'min': 1, 'max': 31, 'style': 'width:60px'}),
            'day3': forms.NumberInput(attrs={'min': 1, 'max': 31, 'style': 'width:60px'}),
            'day4': forms.NumberInput(attrs={'min': 1, 'max': 31, 'style': 'width:60px'}),
            'day5': forms.NumberInput(attrs={'min': 1, 'max': 31, 'style': 'width:60px'}),
            'day6': forms.NumberInput(attrs={'min': 1, 'max': 31, 'style': 'width:60px'}),
        }

@admin.register(PlanEvent)
class PlanEventAdmin(admin.ModelAdmin):
    form = PlanEventAdminForm
    
    fieldsets = (
        ('Настройки года', {
            'fields': ('use_current_year', 'myyear')
        }),
        ('Дата 1', {'fields': ('day1', 'month1')}),
        ('Дата 2', {'fields': ('day2', 'month2')}),
        ('Дата 3', {'fields': ('day3', 'month3')}),
        ('Дата 4', {'fields': ('day4', 'month4')}),
        ('Дата 5', {'fields': ('day5', 'month5')}),
        ('Дата 6', {'fields': ('day6', 'month6')}),
    )