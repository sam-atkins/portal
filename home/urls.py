from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home_view, name="home"),
    path("weather/", views.weather_view, name="weather"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
