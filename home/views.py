from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from manageconf import get_config

from services.service_proxy import ServiceProxy

# TODO(sam) delete import after dev is complete
# from .weather_data import WEATHER_DATA


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
    # TODO(sam) get payload from config i.e. default location
    default_location_short_name = get_config("default_location_short_name", "ldn")
    payload = {"name": default_location_short_name}
    weather_data = ServiceProxy.service_request(
        service_name="met_service",
        service_version=1,
        service_function_name="GetWeatherFunction",
        payload=payload,
    )
    parsed_weather_data = parse_weather_data(weather_data=weather_data)
    location = get_config("default_location_name", "London")
    default_location = {"location": location}
    context = {**default_location, **parsed_weather_data}
    return render(request, "home/home.html", context=context)


@login_required
def weather_view(request):
    default_location_short_name = get_config("default_location_short_name", "ldn")
    payload = {"name": default_location_short_name}
    weather_data = ServiceProxy.service_request(
        service_name="met_service",
        service_version=1,
        service_function_name="GetWeatherFunction",
        payload=payload,
    )
    print(weather_data)
    context = {}
    return render(request, "home/weather_page.html", context=context)


def parse_weather_data(weather_data: dict) -> dict:
    # weather_data = WEATHER_DATA
    current_temp = weather_data.get("currently").get("temperature")
    if current_temp is not None:
        current_temp = round(current_temp)
    current_summary = weather_data.get("currently").get("summary")
    forecast_summary = weather_data.get("daily").get("summary")
    forecast_summary_icon = weather_data.get("daily").get("icon")
    weather_info = {
        "current_temp": current_temp,
        "current_summary": current_summary,
        "forecast_summary": forecast_summary,
        "forecast_summary_icon": forecast_summary_icon,
    }
    return weather_info
