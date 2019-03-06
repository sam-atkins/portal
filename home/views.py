# from django.contrib.auth import authenticate
from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


# TODO(sam) add auth user decorator
def home_view(request):
    return render(request, 'home/home.html')
