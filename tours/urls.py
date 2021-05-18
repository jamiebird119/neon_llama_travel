from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.tour_search, name="tour_search"),
    path('details/<int:tour_id>', views.tour_details, name="tour_details")
]