from django.contrib.auth import authenticate
from django.shortcuts import redirect, render


def index(request):
    return render(request, 'home/index.html')


# TODO(sam)
# change form to username instead of email - check user Model requirements
# hook up html form so posts on submit
# verify logic and flow of the fn
# add error message for unhappy path
def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            return redirect('home')

        else:
            # No backend authenticated the credentials
            # TODO(sam) re render form and error message
            return render(request, 'home/login_form.html')

    return render(request, 'home/login_form.html')


# TODO(sam) add auth user decorator
def home_view(request):
    return render(request, 'home/home.html')
