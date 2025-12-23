from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from .models import Visit

def site_stats(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    total = Visit.objects.aggregate(total=Count('id'))['total']
    today = Visit.objects.filter(created_at__gte=today_start).aggregate(total=Count('id'))['total']
    week = Visit.objects.filter(created_at__gte=week_start).aggregate(total=Count('id'))['total']

    return {
        'admin_total_visits': total or 0,
        'admin_today_visits': today or 0,
        'admin_week_visits': week or 0,
    }
