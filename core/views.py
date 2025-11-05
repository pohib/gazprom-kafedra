from django.shortcuts import render
from news.views import events as news_events

def index(request):
    return render(request, 'index.html')

def enrollment(request):
    return render(request, 'enrollment.html')

def events(request):
    return news_events(request)

def achievements(request):
    return render(request, 'achievements.html')

def partners(request):
    return render(request, 'partners.html')

def plan(request):
    return render(request, 'plan.html')

def contact(request):
    return render(request, 'contact.html')

context = {
    'range_1_8': range(1, 9),
}
