from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from manageconf import get_config

from home.utils import split_strings, parse_weather_data
from services.service_proxy import ServiceProxy

CACHE_PAGE_VIEW_DURATION = get_config("CACHE_PAGE_VIEW_DURATION", 30)


@login_required
@cache_page(CACHE_PAGE_VIEW_DURATION)
def weather_view(request):
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
