from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import VERSION


def home(request):
    """Home page view"""
    context = {
        'django_version': f'{VERSION[0]}.{VERSION[1]}.{VERSION[2]}'
    }
    return render(request, 'home.html', context)