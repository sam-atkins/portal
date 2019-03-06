from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


@login_required
def home_view(request):
    return render(request, 'home/home.html')
