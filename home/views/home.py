from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from manageconf import get_config

from services.service_proxy import ServiceProxy
from home.utils import split_strings, parse_weather_data


def index(request):
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
