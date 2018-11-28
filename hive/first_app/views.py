
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from first_app.forms import NewTweetForm, ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from first_app.models import UserProfileInfo, Tweet
from django.contrib.auth.models import User
import datetime

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
def publish_a_tweet(request, user_id):
	
	if not request.user.is_authenticated:
		return HttpResponseNotFound("Not Found")
	
	else:
		user = User.objects.get(id=user_id)
		
		if request.user.id == user_id:
			form = NewTweetForm()
			
			if request.method == 'POST':
				form = NewTweetForm(request.POST)
				
				if form.is_valid():
					text = form.cleaned_data['text']
					tweet = Tweet(text=text, user=user, date=datetime.datetime.now())
					tweet.save()
					return redirect('/first_app/homepage/{int:user_id}')
				
				else:
					print('Error - form is unvalid')

		return render(request, 'publish_a_tweet.html', context={'form': form, 'user': user})


@login_required
def edit_page(request):
	if request.method == 'POST':
		edit_form = ProfileEditForm(request.POST)
		if edit_form.is_valid():
			clean_data = edit_form.clean()
			pass
			# UserProfileInfo.objects.


	else:
		user = request.user
		userprofile = UserProfileInfo.objects.get(user=user)
		default_data = {'email': user.email, 'username': user.username, 'bio': userprofile.bio}
		edit_form = ProfileEditForm(default_data, label_suffix=': ')

	return render(request, 'profile_edit.html', {
			'edit_form': edit_form,
		})




















