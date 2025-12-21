from django.shortcuts import render
from .models import Graduate

def graduates(request):
    graduates = Graduate.objects.all()
    graduation_years = sorted(
        set(g.graduation_year for g in graduates), 
        reverse=True
    )
    unique_groups = set(g.group for g in graduates)
    
    context = {
        'graduates': graduates,
        'graduation_years': graduation_years,
        'unique_groups': unique_groups,
        'total_graduates': graduates.count(),
    }
    return render(request, 'graduates.html', context)