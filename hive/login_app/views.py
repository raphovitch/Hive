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
			'errors': errors,
		})
