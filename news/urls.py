from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.events, name='events'),
    path('calendar/', views.events_calendar, name='events_calendar'),
    path('calendar/year/<int:year>/', views.events_calendar, name='events_calendar_year'),
    path('calendar/year/<int:year>/month/<int:month>/', views.events_calendar, name='events_calendar_month'),
    path('calendar/year/<int:year>/month/<int:month>/day/<int:day>/', views.events_calendar, name='events_calendar_day'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
]