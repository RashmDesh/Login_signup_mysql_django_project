from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
     path("otp/", views.otp),
    path("otpresult/", views.optresult),
    path("update/", views.update),

]
