from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def index(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    return render(request, 'home/home.html')


@login_required
def home_view(request):
    return render(request, 'home/home.html')
