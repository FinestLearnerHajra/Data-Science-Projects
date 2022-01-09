from django.contrib import admin
from django.urls import path, include
from . import views
from .views import submit_success, submit_order

urlpatterns=[
	
	path('user_orders/<str:username>', views.submit_success, name='user-orders'),
]