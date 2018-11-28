from django.urls import path 
from . import views

app_name = 'first_app'

urlpatterns = [
	path('home/', views.home, name='home'),
	path('publish_a_tweet/', views.publish_a_tweet, name='publish_a_tweet'),
	path('edit_profile/', views.edit_page, name='edit_profile'),

]