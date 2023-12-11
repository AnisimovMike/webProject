from django.urls import path
from HouseHunter import views

urlpatterns = [
    path("", views.index),
    path("about-us", views.about_us),
    path("catalog/<str:object_filter>", views.catalog),
    path("services", views.services),
    path("charts", views.charts),
    path("authorization", views.authorization),
    path("bd/<int:f>", views.bd),
    path("send_mes", views.send_mes),
]
