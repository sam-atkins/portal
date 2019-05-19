from django.urls import path

from home.views import auth, finance, home, weather

urlpatterns = [
    path("", home.index, name="index"),
    path("home/", home.home_view, name="home"),
    path("weather/", weather.weather_view, name="weather"),
    path("finance/", finance.finance_view, name="finance"),
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
]
