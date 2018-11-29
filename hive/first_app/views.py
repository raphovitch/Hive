
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from first_app.forms import NewTweetForm, ProfileEditForm, PasswordEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from first_app.models import UserProfileInfo, Tweet
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.hashers import check_password, make_password


def gets_lasts_tweets(n=10):
	lasts_tweets = Tweet.objects.all().order_by('-date')[:n]
	return lasts_tweets


# Create your views here.
	


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



def profile_page(request, username):
	profile_info = UserProfileInfo.objects.get(user__username=username)
	print(profile_info.bio)
	if request.user.is_authenticated:


		return render(request, 'profile.html', {'logged_in': True, 'user': request.user, 'profile_info': profile_info})


	return render(request, 'profile.html', {'logged_in': False, 'profile_info': profile_info})


















