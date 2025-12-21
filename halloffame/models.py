from django.db import models
from django.core.files.storage import default_storage
from datetime import date

MONTHS_RU = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}

def current_month_name_ru():
    today = date.today()
    return MONTHS_RU[today.month]

class Graduate(models.Model):
    full_name = models.CharField('ФИО', max_length=200)
    group = models.CharField('Группа', max_length=50)
    graduation_year = models.IntegerField('Год выпуска')
    graduation_month = models.CharField(
        'Месяц выпуска',
        max_length=20,
        default=current_month_name_ru,
    )
    specialization = models.CharField('Направление производственной деятельности', max_length=300)
    photo = models.ImageField(
        'Фото',
        upload_to='graduates/',
        blank=True,
        null=True,
    )
    description = models.TextField('Описание', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        ordering = ['-graduation_year', 'full_name']
        verbose_name = 'Выпускник'
        verbose_name_plural = 'Выпускники'
    
    def __str__(self):
        return f"{self.full_name} ({self.graduation_year})"
