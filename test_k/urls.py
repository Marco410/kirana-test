from django.urls import path
from . import views



urlpatterns = [
    path('index/',views.index),
    path('cargar-datos/',views.cargar_datos,name="cargar-datos"),
]