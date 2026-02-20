from django.db import models
from django.utils import timezone
class Visit(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    city = models.CharField(max_length=100, blank=True, null=True, default='Не определено', verbose_name='Город')
    country = models.CharField(max_length=100, blank=True, null=True, default='Не определено', verbose_name='Страна')
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name='Ключ сессии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата посещения')
    user_agent = models.TextField(blank=True, null=True, verbose_name='Сведения')

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['city']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
        verbose_name = 'Посещение'
        verbose_name_plural = "Посещения"

    def __str__(self):
        return f"{self.ip_address} - {self.city or 'Неизвестно'}"

class PlanEvent(models.Model):
    day1 = models.PositiveIntegerField(verbose_name='День', blank=True, null=True, default=0)
    month1 = models.TextField(max_length=20, verbose_name='Месяц', blank=True, null=True, default="-")
    day2 = models.PositiveIntegerField(verbose_name='День', blank=True, null=True, default=0)
    month2 = models.TextField(max_length=20, verbose_name='Месяц', blank=True, null=True, default="-")
    day3 = models.PositiveIntegerField(verbose_name='День', blank=True, null=True, default=0)
    month3 = models.TextField(max_length=20, verbose_name='Месяц', blank=True, null=True, default="-")
    day4 = models.PositiveIntegerField(verbose_name='День', blank=True, null=True, default=0)
    month4 = models.TextField(max_length=20, verbose_name='Месяц', blank=True, null=True, default="-")
    day5 = models.PositiveIntegerField(verbose_name='День', blank=True, null=True, default=0)
    month5 = models.TextField(max_length=20, verbose_name='Месяц', blank=True, null=True, default="-")
    day6 = models.PositiveIntegerField(verbose_name='День', blank=True, null=True, default=0)
    month6 = models.TextField(max_length=20, verbose_name='Месяц', blank=True, null=True, default="-")
    myyear = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год')
    use_current_year = models.BooleanField(default=False, verbose_name="Авто-год (текущий)")

    @property
    def year(self):
        return timezone.now().year if self.use_current_year else (self.myyear or timezone.now().year)

    class Meta:
        verbose_name = "Даты проведения устного собеседования "
        verbose_name_plural = "Устное собеседование даты"