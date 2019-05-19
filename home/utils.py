def split_strings(original_string: str, delimiter: str = "__"):
    """Splits a string by the given (or default) delimiter

    Args:
        original_string (str): the string to split

    Returns:
        list: containing the split strings e.g. ldn__london -> ['ldn', 'london']
    """
    return original_string.split(delimiter)


def parse_weather_data(location_name: str, weather_data: dict) -> dict:
    """Parses weather data into a context dict

    Args:
        location_name (str): the weather forecast location
        weather_data (dict): the weather forecast data

    Returns:
        dict: weather data used to render the view
    """
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
