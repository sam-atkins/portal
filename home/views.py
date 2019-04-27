import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from manageconf import get_config
import requests

from services.service_proxy import ServiceProxy
from .weather_data import WEATHER_DATA


def index(request):
    return render(request, "home/home.html")


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


@login_required
def home_view(request):
    location = get_config("default_location_name", "London")
    default_location = {"location": location}
    weather_data = parse_weather_data()
    context = {**default_location, **weather_data}
    return render(request, "home/home.html", context=context)


def parse_weather_data():
    data = WEATHER_DATA
    current_temp = data.get("currently").get("temperature")
    if current_temp is not None:
        current_temp = round(current_temp)
    current_summary = data.get("currently").get("summary")
    forecast_summary = data.get("daily").get("summary")
    forecast_summary_icon = data.get("daily").get("icon")
    weather_info = {
        "current_temp": current_temp,
        "current_summary": current_summary,
        "forecast_summary": forecast_summary,
        "forecast_summary_icon": forecast_summary_icon,
    }
    return weather_info


@login_required
def weather_view(request):
    payload = {"name": "ldn"}
    # TODO(sam) confirm lambda function name for met_service
    weather_data = ServiceProxy.service_request(
        service_name="met_service",
        service_version=1,
        service_function_name="GetWeatherFunction",
        payload=payload,
    )
    print(weather_data)
    context = {}
    return render(request, "home/weather_page.html", context=context)
