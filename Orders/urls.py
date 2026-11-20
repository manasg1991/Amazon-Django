from django.contrib import admin
from django.urls import path,include
from urllib3 import request

from .import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.Payments, name='payments'),
    path('order_complete/',views.order_complete,name='order_complete'),
]