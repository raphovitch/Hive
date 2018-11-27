from django.urls import path 
from . import views

app_name = 'first_app'

urlpatterns = [
	path('', views.index, name='homepage'),
	path('publish_a_tweet/', views.publish_a_tweet, name='publish_a_tweet'),
]