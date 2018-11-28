from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.

def log_in(request):
	errors = False
	if request.method == 'POST':
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			clean_data = login_form.clean()
			user = authenticate(username=clean_data['username'], password=clean_data['password'])

			if user is not None:
				login(request, user)
				print('Logged In: {}'.format(user))
				return redirect('/first_app/', permanent=True)
			else:
				errors = True
	else:
		login_form = forms.LoginForm()

	return render(request, 'login_form.html', {
			'login_form': login_form,
			'errors': errors,})

def signup(request):
	registered = False
	if request.method =='POST':
		user_form = forms.UserForm(data= request.POST) 
		profile_form = forms.UserProfileInfoForm(data= request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit= False)
			profile.user = user

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']

			profile.save()
			registered = True


		else : 
			print(user_form.errors, profile_form.errors)

	else: 
		user_form = forms.UserForm()
		profile_form = forms.UserProfileInfoForm()

	return render(request, 'signup_form.html', context = {
		'user_form' : user_form,
		'profile_form' : profile_form, 
		'registered': registered
		})

@login_required
def log_out(request):
	logout(request)
	return redirect('/first_app/', permanent=True)














