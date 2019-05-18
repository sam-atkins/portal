from unittest.mock import patch

from django.test import TestCase

from users.models import CustomUser
from tests.datasets.weather_data import WEATHER_DATA


class WeatherViewTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            CustomUser.objects.get_or_create(username="testuser")[0]
        )

    @patch("home.views.weather.ServiceProxy.service_request", return_value=WEATHER_DATA)
    def test_logged_in_user_weather_view_returns_200(self, mock_service_proxy):
        response = self.client.get("/weather/")
        self.assertEqual(response.status_code, 200)

    @patch("home.views.weather.ServiceProxy.service_request", return_value=WEATHER_DATA)
    def test_logged_in_user_weather_renders_weather_html(self, mock_service_proxy):
        response = self.client.get("/weather/")
        self.assertTemplateUsed(response, "home/base.html", "home/weather_page.html")


class WeatherViewLoggedOutUserTestCase(TestCase):
    def test_weather_view_redirects(self):
        response = self.client.get("/weather/")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "home/weather_page.html")

    def test_logged_out_user_weather_view_renders_login_html(self):
        response = self.client.get("/weather/", follow=True)
        self.assertTemplateNotUsed(response, "home/weather_page.html")
