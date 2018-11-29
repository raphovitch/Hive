
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from first_app.forms import NewTweetForm, ProfileEditForm, PasswordEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from first_app.models import UserProfileInfo, Tweet
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
	
def gets_lasts_tweets(n=10):
	lasts_tweets = Tweet.objects.all().order_by('-date')[:n]
	return lasts_tweets


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
			return redirect('/first_app/home')
		
		else:
			print('Error - tweet_form is unvalid')
	else:
		tweet_form = NewTweetForm()

	return render(request, 'publish_a_tweet.html', context={'tweet_form': tweet_form, 'user': user, 'logged_in': True})


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

	return render(request, 'profile_edit.html', {
			'edit_form': edit_form,
			'form_error': form_error,
			'password_form': password_form,
			'password_error': password_error
		})


@login_required
def feed_page(request):
	
	user = request.user
	userprofile = UserProfileInfo.objects.get(user=user)
	follows = userprofile.follows.all()

	tweets_of_user = Tweet.objects.all().order_by('-id').filter(user__in=follows)
	all_tweets = []
	
	for tweet in tweets_of_user:
		all_tweets.append(tweet)
	
	
	return render(request, 'feed_page.html', context={'list': all_tweets, 'logged_in': True, 'user': user})




















