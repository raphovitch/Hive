from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from first_app.forms import NewTweetForm, ProfileEditForm, PasswordEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from first_app.models import UserProfileInfo, Tweet
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.hashers import check_password, make_password


def get_all_users(username):
	all_users = UserProfileInfo.objects.exclude(user__username = username)
	return all_users
	
	
def gets_lasts_tweets(n=10):
	lasts_tweets = Tweet.objects.all().order_by('-date')[:n]
	return lasts_tweets

def get_all_tweets():
	all_tweets = Tweet.objects.all()
	return all_tweets

def get_all_likers(tweet_id):
	tweet = Tweet.objects.get(id= tweet_id)
	all_likers = tweet.liked_by.all()
	return all_likers


def get_tweets_of_user(profile_info_id):
	tweets = Tweet.objects.filter(user=profile_info_id)
	
	return tweets

# Create your views here.

def all_tweets(request):
	if request.user.is_authenticated:

		user_p = UserProfileInfo.objects.get(user=request.user)
		
		tweets = [tweet for tweet in Tweet.objects.all()]

		# This is for all likes
		all_likes = []
		all_likers = []
		for tweet in tweets:
			if user_p in tweet.liked_by.all():
				print(tweet)
				all_likes.append(True)
			else:
				print(tweet)
				all_likes.append(False)
			all_likers.append(get_all_likers(tweet.id))



		# range_list = [index for index in range(len(all_likes))]
		# print(range_list)

		my_list = zip(tweets, all_likes, all_likers)


		return render(request, 'all_tweets.html',context={'my_list': my_list, 'user_p':user_p, 'logged_in': True, 'user': request.user})

	else:
		tweets = [tweet for tweet in Tweet.objects.all()]
		all_likes = [False for tweet in tweets]

		my_list = zip(tweets, all_likes)


	return render(request, 'all_tweets.html',context={'my_list': my_list, 'logged_in': False,})


def all_users(request):
	if request.user.is_authenticated:
		user_p = UserProfileInfo.objects.get(user= request.user)
		return render(request, 'all_users.html',context={'list': get_all_users(request.user.username), 'user_p':user_p, 'list_followers': user_p.follows.all(), 'logged_in': True, 'user': request.user}) 
	else:
		return render(request, 'all_users.html',context={'list': get_all_users(request.user.username), 'logged_in': False})


def home(request):
	if request.user.is_authenticated:
		return render(request, 'home.html',context={'list': gets_lasts_tweets(), 'logged_in': True, 'user': request.user})
	else:
		return render(request, 'home.html', {'list': gets_lasts_tweets(), 'logged_in': False})
	


@login_required
def publish_a_tweet(request):
	
	user = request.user
	userprofile = UserProfileInfo.objects.get(user=user)

	if request.method == 'POST':
		tweet_form = NewTweetForm(request.POST)
		
		if tweet_form.is_valid():
			text = tweet_form.cleaned_data['text']
			title = tweet_form.cleaned_data['title']
			tweet = Tweet(title=title, text=text, user=userprofile, date=datetime.datetime.now())
			tweet.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		
		else:
			print('Error - tweet_form is unvalid')
	else:
		tweet_form = NewTweetForm()

	return render(request, 'publish_a_tweet.html', context={'tweet_form': tweet_form, 'user': user, 'logged_in': True, 'list': gets_lasts_tweets()})


@login_required
def edit_page(request):
	user = request.user
	form_error = False
	password_error = False
	userprofile = UserProfileInfo.objects.get(user=user)
	default_data = {'email': user.email, 'username': user.username, 'bio': userprofile.bio}

	if request.method == 'POST':
		if 'edit_profile' in request.POST:
			edit_form = ProfileEditForm(request.POST)
			if edit_form.is_valid():
				clean_data = edit_form.clean()
				if user.username == clean_data['username'] or (user.username != clean_data['username'] and len(User.objects.filter(username=clean_data['username'])) == 0 ):
					user.username = clean_data['username']
					user.email = clean_data['email']
					userprofile.bio = clean_data['bio']

					userprofile.save()
					user.save()
					return home(request)
				else:
					password_form = PasswordEditForm(label_suffix=' : ')
					edit_form =  ProfileEditForm(default_data, label_suffix=' : ')
					form_error = True
			else:
				print(edit_form.errors)

		elif 'change_pass' in request.POST:
			password_form = PasswordEditForm(request.POST)
			if password_form.is_valid():
				clean_data = password_form.clean()
				if check_password(clean_data['old_password'], user.password):
					# print(clean_data['new_password'])
					new_pass = make_password(clean_data['new_password'])
					# print(new_pass)
					user.password = new_pass
					# print(user.password)
					user.save()
					return home(request)
				else:
					password_error = True
					password_form = PasswordEditForm(label_suffix=' : ')
					edit_form =  ProfileEditForm(default_data, label_suffix=' : ')

			else:
				print(password_form.errors)
				password_form = PasswordEditForm(label_suffix=' : ')
				edit_form = ProfileEditForm(default_data, label_suffix=' : ')

	else:
		edit_form = ProfileEditForm(default_data, label_suffix=' : ')
		password_form = PasswordEditForm(label_suffix=' : ')


	if request.user.is_authenticated:
		return render(request, 'profile_edit.html', {
				'edit_form': edit_form,
				'form_error': form_error,
				'password_form': password_form,
				'password_error': password_error,
				'logged_in': True,
				'user': request.user,
			})


@login_required
def feed_page(request):
	
	user = request.user
	userprofile = UserProfileInfo.objects.get(user=user)
	follows = userprofile.follows.all()

	tweets_of_user = Tweet.objects.all().order_by('-id').filter(user__in=follows)
	
	return render(request, 'feed_page.html', context={'list': tweets_of_user, 'logged_in': True, 'user': user})

@login_required
def follow_user(request, username):
	user1 = request.user
	user = UserProfileInfo.objects.get(user= user1)
	user_to_follow = UserProfileInfo.objects.get(user__username= username)
	user.follows.add(user_to_follow)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow_user(request, username):
	user1 = request.user
	user = UserProfileInfo.objects.get(user= user1)
	user_to_unfollow = UserProfileInfo.objects.get(user__username= username)
	user.follows.remove(user_to_unfollow)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def all_followees(request, username):
		user1 = UserProfileInfo.objects.get(user__username= username)
		list_user_followees = user1.follows.all()
		if request.user.is_authenticated:
			return render(request, 'all_followees.html',context={'list': list_user_followees, 'user1':user1, 'logged_in': True, 'user': request.user})

		return render(request, 'all_followees.html',context={'list': list_user_followees, 'user1':user1, 'logged_in': False})

def all_followers(request, username):
	user1 = UserProfileInfo.objects.get(user__username= username)
	list_of_all_users = UserProfileInfo.objects.exclude(user__username = username) 
	list_of_followers = [user for user in list_of_all_users if user1 in user.follows.all()]
	if request.user.is_authenticated:
		return render(request, 'all_followers.html',context={'list': list_of_followers, 'user1':user1, 'list_followers': user1.follows.all(), 'logged_in': True, 'user': request.user})

	return render(request, 'all_followers.html',context={'list': list_of_followers, 'user1':user1, 'list_followers': user1.follows.all(), 'logged_in': False})
	

  
def profile_page(request, username):
	profile_info = UserProfileInfo.objects.get(user__username=username)
	profile_info_id = profile_info.user.id 
	
	if request.user.is_authenticated:
		# following = False
		# if profile_info in :
		# 	following = True

		return render(request, 'profile.html', {'logged_in': True, 'user': request.user, 'profile_info': profile_info, 'tweets': get_tweets_of_user(profile_info_id), 'following': UserProfileInfo.objects.get(user=request.user).follows.all()})


	return render(request, 'profile.html', {'logged_in': False, 'profile_info': profile_info, 'tweets': get_tweets_of_user(profile_info_id)})




@login_required
def like_tweet(request,tweet_id):
	user1 = request.user
	user = UserProfileInfo.objects.get(user= user1)
	tweet_to_like = Tweet.objects.get(id= tweet_id)
	tweet_to_like.liked_by.add(user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def dislike_tweet(request,tweet_id):
	user1 = request.user
	user = UserProfileInfo.objects.get(user= user1)
	tweet_to_dislike = Tweet.objects.get(id= tweet_id)
	tweet_to_dislike.liked_by.remove(user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	








