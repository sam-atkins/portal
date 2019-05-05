from django.test import TestCase

from home.views import parse_weather_data
from users.models import CustomUser
from tests.datasets.weather_data import WEATHER_DATA


class HomeViewsLoggedInUserTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            CustomUser.objects.get_or_create(username="testuser")[0]
        )

    def test_logged_in_user_index_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_index_renders_home_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home/base.html", "home/home.html")
        self.assertTemplateUsed(response, "home/nav.html")

    def test_logged_in_user_home_returns_200(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_home_renders_home_html(self):
        response = self.client.get("/home/")
        self.assertTemplateUsed(response, "home/base.html", "home/home.html")
        self.assertTemplateUsed(response, "home/nav.html")


class HomeViewsTestCase(TestCase):
    def test_index_redirect_follow_returns_200(self):
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logged_out_user_index_renders_login_html(self):
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "home/base.html", "registration/login.html")
        self.assertTemplateUsed(response, "home/nav.html")

    def test_home_redirects_returns_302(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 302)

    def test_logged_out_user_home_renders_login_html(self):
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "home/base.html", "registration/login.html")
        self.assertTemplateUsed(response, "home/nav.html")


class LogInViewTestCase(TestCase):
    def test_login_view_returns_200(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_renders_login_template(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "home/base.html", "registration/login.html")


class WeatherViewTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            CustomUser.objects.get_or_create(username="testuser")[0]
        )

    def test_logged_in_user_weather_view_returns_200(self):
        response = self.client.get("/weather/")
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_weather_renders_weather_html(self):
        response = self.client.get("/home/")
        self.assertTemplateUsed(response, "home/base.html", "home/weather_page.html")


class WeatherViewLoggedOutUserTestCase(TestCase):
    def test_weather_view_redirects(self):
        response = self.client.get("/weather/")
        self.assertEqual(response.status_code, 302)

    def test_logged_out_user_weather_view_renders_login_html(self):
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "home/base.html", "registration/login.html")
        self.assertTemplateUsed(response, "home/nav.html")


class ParseWeatherData(TestCase):
    def test_parse_weather_data(self):
        weather_data = parse_weather_data(
            location_name="san_francisco", weather_data=WEATHER_DATA
        )
        assert weather_data == {
            "name": "san francisco",
            "current_temp": 14,
            "current_summary": "Mostly Cloudy",
            "forecast_summary": "Light rain tomorrow, with high temperatures rising to 20°C on Wednesday.",  # noqa E501
            "forecast_summary_icon": "rain",
        }
