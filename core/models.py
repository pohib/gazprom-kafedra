from django.db import models

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
