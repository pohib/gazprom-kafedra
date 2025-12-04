from django.db import models
from django.utils import timezone

class News(models.Model):
    source_id = models.CharField(max_length=50, unique=True, verbose_name='ID поста')
    title = models.CharField(max_length=1000, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Наполнение')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Показывать на сайте')
    is_title_edited = models.BooleanField(default=False, verbose_name='Заголовок отредактирован вручную')
    is_body_edited = models.BooleanField(default=False, verbose_name='Текст отредактирован вручную')
    auto_title_sentences = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='Обрезать заголовок до N предложений (авто)',
        help_text='Число предложений для автоматического заголовка'
    )

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

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название мероприятия')
    description = models.TextField(verbose_name='Описание')
    event_date_start = models.DateField('Дата начала', help_text='дд.мм.гггг')
    event_date_end = models.DateField('Дата окончания', blank=True, null=True)
    registration_deadline = models.DateField('Дедлайн заявок', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, verbose_name='Место проведения')
    venue = models.CharField(max_length=200, blank=True, verbose_name='Площадка')
    tags = models.CharField(max_length=500, blank=True, verbose_name='Теги', 
                        help_text='Через запятую: конференция, семинар, хакатон')
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    @classmethod
    def get_month_name(cls, month_num):
        MONTH_NAMES = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        return MONTH_NAMES.get(month_num, f'Месяц {month_num}')
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-event_date_start']

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]