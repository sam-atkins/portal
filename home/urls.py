from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # TODO(sam) delete once auth flow is finalised
    path('portal/login/', views.auth_login, name='auth_login'),
    path('home/', views.home_view, name='home_view'),
]
