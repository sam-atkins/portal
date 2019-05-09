from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from manageconf import get_config

from services.service_proxy import ServiceProxy
from .forms import CurrencyExchangeForm
from .utils import split_strings


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
    context = {"weather": False, "weather_data": []}
    location = get_config("default_weather_location")
    if location is not None:
        location_name = split_strings(original_string=location)
        payload = {"name": location_name[0]}
        try:
            service_proxy = ServiceProxy()
            weather_data = service_proxy.service_request(
                service_name="met_service",
                service_version=1,
                function_name="weather",
                payload=payload,
            )
        except Exception:
            weather_data = {}
        if weather_data:
            context["weather"] = True
            location = get_config("default_location_name", "London")
            parsed_weather_data = parse_weather_data(
                location_name=location_name[1], weather_data=weather_data
            )
            weather_data = context.get("weather_data")
            weather_data.append(parsed_weather_data)
    return render(request, "home/home.html", context=context)


@login_required
def weather_view(request):
    # TODO(sam) use cache to minimise API requests
    context = {"weather": False, "weather_data": []}
    locations = get_config("weather_locations", [])
    for location in locations:
        location_name = split_strings(original_string=location)
        payload = {"name": location_name[0]}
        try:
            service_proxy = ServiceProxy()
            weather_data = service_proxy.service_request(
                service_name="met_service",
                service_version=1,
                function_name="weather",
                payload=payload,
            )
        except Exception:
            weather_data = {}
        if weather_data:
            context["weather"] = True
            location = get_config("default_location_name", "London")
            parsed_weather_data = parse_weather_data(
                location_name=location_name[1], weather_data=weather_data
            )
            weather_data = context.get("weather_data")
            weather_data.append(parsed_weather_data)

    return render(request, "home/weather_page.html", context=context)


def parse_weather_data(location_name: str, weather_data: dict) -> dict:
    current_temp = weather_data.get("currently").get("temperature")
    if current_temp is not None:
        current_temp = round(current_temp)
    current_summary = weather_data.get("currently").get("summary")
    forecast_summary = weather_data.get("daily").get("summary")
    # NOTE(sam) some Darksky responses have Â in the string for no apparent reason
    forecast_summary = forecast_summary.replace("Â", "")
    forecast_summary_icon = weather_data.get("daily").get("icon")
    formatted_location_name = location_name.replace("_", " ")
    return {
        "name": formatted_location_name,
        "current_temp": current_temp,
        "current_summary": current_summary,
        "forecast_summary": forecast_summary,
        "forecast_summary_icon": forecast_summary_icon,
    }

@login_required()
def finance_view(request):
    # context = {}
    # context["form"] = form
    form = CurrencyExchangeForm()
    return render(request, "home/finance_page.html", {"form": form})
