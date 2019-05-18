from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Something went wrong. Please try again")
            return render(request, "registration/login.html", context)

    return render(request, "registration/login.html", context)


def logout_view(request):
    logout(request)
    return render(request, "home/home.html")
