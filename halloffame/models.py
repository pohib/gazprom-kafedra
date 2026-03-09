from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

MONTHS_RU = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
    7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
}

def current_month_name_ru():
    today = date.today()
    return MONTHS_RU[today.month]

class Graduate(models.Model):
    full_name = models.CharField('ФИО', max_length=200)
    photo = models.ImageField('Фото', upload_to='graduates/', blank=True, null=True)
    
    group = models.CharField('Группа', max_length=50)
    graduation_year = models.IntegerField('Год выпуска')
    graduation_month = models.CharField(
        'Месяц выпуска', 
        max_length=20, 
        default=current_month_name_ru
    )
    vkr_theme = models.CharField('Тема ВКР/диплома', max_length=400, blank=True, null=True)
    scientific_supervisor = models.CharField('Научный руководитель', max_length=200, blank=True, null=True)

    specialization = models.CharField('Направление деятельности', max_length=300)
    status = models.CharField('Статус', max_length=100, help_text="Например: Выпускник / Аспирант / Магистрант")
    current_work_place = models.CharField('Текущее место работы', max_length=300, blank=True, null=True)
    key_skills = models.TextField('Ключевые навыки', blank=True, null=True, help_text="Введите через запятую: Python, SQL, CRM")
    achievements = models.TextField('Достижения', blank=True, null=True)
    
    short_info = models.TextField(
        'Коротко о выпускнике', 
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="Отображается в карточке в стеклянном блоке"
    )
    description = models.TextField('Полная биография', blank=True, null=True, help_text="Отображается в модальном окне")
    
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ['-graduation_year', 'full_name']
        verbose_name = 'Выпускник'
        verbose_name_plural = 'Выпускники'

    def __str__(self):
        return f"{self.full_name} ({self.graduation_year})"

    def get_contacts_html(self):
        contacts = self.contacts_set.all()
        if not contacts:
            return ""
            
        html_parts = []
        for c in contacts:
            if c.contact_type == 'text':
                if c.label:
                    html_parts.append(f"<span>{c.label}</span>")
            
            elif c.contact_type == 'link':
                display_text = c.label if c.label else c.url
                html_parts.append(f'<a href="{c.url}" class="contact-link" target="_blank">{display_text}</a>')
            
            elif c.contact_type == 'social':
                label = c.label if c.label else "Контакт"
                html_parts.append(f'{label}: <a href="{c.url}" class="contact-link" target="_blank">перейти</a>')
        
        return "; ".join(html_parts)

class GraduateContact(models.Model):
    CONTACT_TYPES = (
        ('text', 'Просто текст (Телефон, адрес)'),
        ('link', 'Ссылка (Сайт, Портфолио)'),
        ('social', 'Текст + Ссылка (Телеграм, ВК)'),
    )
    
    graduate = models.ForeignKey(
        Graduate, 
        related_name='contacts_set', 
        on_delete=models.CASCADE,
        verbose_name='Выпускник'
    )

    contact_type = models.CharField('Тип контакта', max_length=10, choices=CONTACT_TYPES, default='text')
    label = models.CharField('Заголовок/Текст', blank=True, null=True, max_length=100, help_text="Например: 'Телеграм' или номер телефона")

    url = models.URLField(
        'Ссылка', 
        blank=True, 
        null=True, 
        help_text="Обязательно с http:// или https://"
    )

    def clean(self):
        if self.contact_type == 'text' and not self.label:
            raise ValidationError({'label': 'Заполните текст контакта (например, номер телефона).'})
        
        if self.contact_type in ['link', 'social'] and not self.url:
            raise ValidationError({'url': 'Укажите ссылку (URL).'})

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.label or self.url} ({self.get_contact_type_display()})"