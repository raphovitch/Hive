from django.urls import path 
from . import views

app_name = 'first_app'

urlpatterns = [
	path('', views.index, name='homepage'),
	path('home/', views.home, name='home'),
]