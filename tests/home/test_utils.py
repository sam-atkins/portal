from django.test import TestCase

from home.utils import parse_weather_data, split_strings
from tests.datasets.weather_data import WEATHER_DATA


class Utils(TestCase):
    def test_split_strings(self):
        location = "wsz__warsaw"
        output = split_strings(original_string=location)
        assert output == ["wsz", "warsaw"]


class ParseWeatherData(TestCase):
    def test_parse_weather_data(self):
        weather_data = parse_weather_data(
            location_name="san_francisco", weather_data=WEATHER_DATA
        )
        self.assertEqual(
            weather_data,
            {
                "name": "san francisco",
                "current_temp": 14,
                "current_summary": "Mostly Cloudy",
                "forecast_summary": "Light rain tomorrow, with high temperatures rising to 20°C on Wednesday.",  # noqa E501
                "forecast_summary_icon": "rain",
            },
        )
