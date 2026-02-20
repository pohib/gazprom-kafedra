from django.shortcuts import render
from news.views import events as news_events
from django.views.decorators.csrf import csrf_protect
from .models import PlanEvent

@csrf_protect
def index(request):
    return render(request, 'index.html')

@csrf_protect
def enrollment(request):
    plan_event = PlanEvent.objects.first()
    if not plan_event:
        plan_event = PlanEvent.objects.create()
    
    context = {
        'plan_event': plan_event
    }
    return render(request, 'enrollment.html', context)

@csrf_protect
def events(request):
    return news_events(request)

@csrf_protect
def achievements(request):
    return render(request, 'achievements.html')

@csrf_protect
def partners(request):
    return render(request, 'partners.html')

@csrf_protect
def plan(request):
    return render(request, 'plan.html')

@csrf_protect
def contact(request):
    return render(request, 'contact.html')
