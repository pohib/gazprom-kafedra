from django.db import models

class News(models.Model):
    source_id = models.CharField(max_length=50, unique=True, verbose_name='ID поста')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Наполнение')
    date = models.DateTimeField(verbose_name='Дата публикации')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Показывать на сайте')
    is_title_edited = models.BooleanField(default=False, verbose_name='Заголовок отредактирован вручную')
    is_body_edited = models.BooleanField(default=False, verbose_name='Текст отредактирован вручную')

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    CROP_CHOICES = [
        ('top', 'Сверху'),
        ('center', 'По центру'),
        ('bottom', 'Снизу'),
    ] + [(f'{i}%', f'{i}% сверху') for i in range(0, 101, 5)]

    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500, verbose_name='URL картинки')
    crop_position = models.CharField(
        max_length=10,
        choices=CROP_CHOICES,
        default='center',
        verbose_name='Позиция обрезки'
    )

    def __str__(self):
        return f"Image for {self.news.title}"

class NewsSettings(models.Model):
    news_count = models.PositiveIntegerField(default=6, verbose_name='Кол-во новостей для парсинга')

    def __str__(self):
        return f"Настройки новостей"

    class Meta:
        verbose_name = "Настройка новостей"
        verbose_name_plural = "Настройки новостей"
