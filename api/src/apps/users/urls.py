from django.contrib import admin
from django.urls import path
  
# importing views from views..py
from .views import activation_view
  
urlpatterns = [
    path('activate/<str:id>/<str:token>/', activation_view ),
]