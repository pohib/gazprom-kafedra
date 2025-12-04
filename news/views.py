import requests
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from .models import News, NewsImage, NewsSettings, Event
import random
from django.core.paginator import Paginator
from calendar import monthrange
from django.db.models import Q, F
import os
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN', 'default_value_if_missing')
VK_GROUP_ID = os.getenv('VK_GROUP_ID', 'default_group_id')
VK_API_VERSION = os.getenv('VK_API_VERSION', '5.131')

@cache_page(60 * 15)
def events(request):
    settings = NewsSettings.objects.first()
    NEWS_COUNT = settings.news_count if settings else 6
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': f'-{VK_GROUP_ID}',
        'count': NEWS_COUNT,
        'access_token': VK_ACCESS_TOKEN,
        'v': VK_API_VERSION,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'response' not in data:
        news_qs = News.objects.filter(is_published=True).order_by('-date')[:NEWS_COUNT]
        return render(request, 'events.html', {'posts': news_qs})

    
    posts = data['response']['items']
    vk_ids = set()

    for post in posts:
        source_id = str(post['id'])
        vk_ids.add(source_id)

        new_title = post['text']
        new_body = post['text']
        date = datetime.fromtimestamp(post['date'], tz=dt_timezone.utc)

        views_count = 0
        if 'views' in post:
            views_count = post['views'].get('count', 0)

        news_obj, created = News.objects.get_or_create(source_id=source_id)

        if not news_obj.is_title_edited:
            news_obj.title = new_title
        if not news_obj.is_body_edited:
            news_obj.body = new_body

        news_obj.date = date
        news_obj.views = views_count
        news_obj.is_published = True
        news_obj.save()

        old_images = {img.image_url: img.crop_position for img in news_obj.images.all()}
        news_obj.images.all().delete()

        if 'attachments' in post:
            for att in post['attachments']:
                if att['type'] == 'photo':
                    sizes = att['photo']['sizes']
                    max_photo = max(sizes, key=lambda x: x['height'] * x['width'])
                    crop_position = old_images.get(max_photo['url'], 'center')
                    NewsImage.objects.create(
                        news=news_obj,
                        image_url=max_photo['url'],
                        crop_position=crop_position
                    )

    News.objects.filter(source_id__isnull=False).exclude(source_id__in=vk_ids).delete()
    
    news_obj.auto_title_sentences = 1
    
    news_to_display = News.objects.filter(is_published=True).order_by('-date')[:NEWS_COUNT]

    logo_variants = ['blue', 'white']
    extended_posts = []
    for post in news_to_display:
        has_images = post.images.exists()
        logo_choice = None
        if not has_images:
            logo_choice = random.choice(logo_variants)
        extended_posts.append({
            'post': post,
            'logo_choice': logo_choice,
        })
        
    return render(request, 'events.html', {'posts_extended': extended_posts})

def events_calendar(request, year=None, month=None, day=None):
    now = timezone.now()

    now_year = now.year
    min_year = now_year - 5
    max_year = now_year + 5
    
    selected_year = int(year) if year else now.year
    selected_month = int(month) if month else now.month
    selected_day = int(day) if day else None
    
    years = list(range(min_year, max_year + 1))
    
    if year and (selected_year < min_year or selected_year > max_year):
        from django.http import Http404
        raise Http404("Выбранный год недоступен")

    current_year = selected_year

    all_events = Event.objects.filter(is_active=True)

    events = all_events.order_by('event_date_start')

    if year:
        events = events.filter(event_date_start__year=selected_year)
    if month:
        events = events.filter(event_date_start__month=selected_month)
    if day:
        events = events.filter(event_date_start__day=selected_day)

    days_in_month = monthrange(selected_year, selected_month)[1]
    days = list(range(1, days_in_month + 1))
    months = list(range(1, 13))

    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)

    months_with_events = set()
    if selected_year:
        months_with_events = set(
            all_events.filter(event_date_start__year=selected_year)
            .values_list('event_date_start__month', flat=True)
            .distinct()
        )

    days_with_events = set()
    if selected_year and selected_month:
        days_with_events = set(
            all_events.filter(
                event_date_start__year=selected_year,
                event_date_start__month=selected_month
            )
            .values_list('event_date_start__day', flat=True)
            .distinct()
        )
    
    
    context = {
        'events': events_page,
        'years': years,
        'months': months,
        'days': days,
        'months_with_events': months_with_events,
        'days_with_events': days_with_events,
        
        'current_year': current_year,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'selected_day': selected_day,
        
        'now': now,
        'current_month': now.month,
        'current_day': now.day,
    }
    
    days_with_events_count = {}
    if selected_year and selected_month:
        events_in_month = all_events.filter(
            event_date_start__year=selected_year,
            event_date_start__month=selected_month
        )
        
        for day_num in range(1, days_in_month + 1):
            count = events_in_month.filter(event_date_start__day=day_num).count()
            if count > 0:
                days_with_events_count[day_num] = count
    
    context.update({
        'days_with_events_count': days_with_events_count,
    })
    
    return render(request, 'events_calendar.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    
    prev_event = (
        Event.objects.filter(
            is_active=True,
            event_date_start__lt=event.event_date_start
        )
        .order_by('-event_date_start')
        .first()
    )

    next_event = (
        Event.objects.filter(
            is_active=True,
            event_date_start__gt=event.event_date_start
        )
        .order_by('event_date_start')
        .first()
    )

    return render(
        request,
        'event_detail.html',
        {
            'event': event,
            'prev_event': prev_event,
            'next_event': next_event,
        },
    )