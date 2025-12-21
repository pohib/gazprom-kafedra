from django.urls import path
from . import views

app_name = 'halloffame'

urlpatterns = [
    path('graduates/', views.graduates, name='graduates'),
]
