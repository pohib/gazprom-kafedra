from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plan/', views.plan, name='plan'),
    path('partners/', views.partners, name='partners'),
    path('enrollment/', views.enrollment, name='enrollment'),
    path('events/', views.events, name='events'),
    path('achievements/', views.achievements, name='achievements'),
    path('contact/', views.contact, name='contact'),
]
