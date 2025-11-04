from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def enrollment(request):
    return render(request, 'enrollment.html')

def events(request):
    return render(request, 'events.html')

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
