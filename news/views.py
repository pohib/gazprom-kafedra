import requests
from django.shortcuts import render
from datetime import datetime, timezone as dt_timezone
from .models import News, NewsImage, NewsSettings

VK_GROUP_ID = '218299724'
VK_ACCESS_TOKEN = '5b329a175b329a175b329a177d580e1f6b55b325b329a173239fc2f75bfa8b099b910f8'
VK_API_VERSION = '5.131'

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

        new_title = (post['text'][:60] + '...') if len(post['text']) > 60 else post['text']
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

    news_to_display = News.objects.filter(is_published=True).order_by('-date')[:NEWS_COUNT]

    return render(request, 'events.html', {'posts': news_to_display})

