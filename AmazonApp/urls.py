from django.urls import path
from AmazonApp import views

urlpatterns = [

    path('',views.home,name='home'),

]