from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portal/login/', views.auth_login, name='auth_login'),
    path('portal/home', views.home_view, name='home_view'),
]
