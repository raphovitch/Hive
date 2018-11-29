from django.urls import path 
from . import views

app_name = 'first_app'

urlpatterns = [
	path('home/', views.home, name='home'),
	path('publish_a_tweet/', views.publish_a_tweet, name='publish_a_tweet'),
	path('edit_profile/', views.edit_page, name='edit_profile'),
	path('profile_page/<username>', views.profile_page, name='profile_page'),
	path('all_users/', views.all_users, name='all_users'),
	path('follow_user/<username>/', views.follow_user, name='follow_user'),
	path('unfollow_user/<username>/', views.unfollow_user, name='unfollow_user'),
	path('all_followees/<username>/', views.all_followees, name='all_followees'),
	path('all_followers/<username>/', views.all_followers, name='all_followers'),

]