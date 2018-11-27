from django import forms
from django.core import validators
from django.contrib.auth.models import User
from first_app.models import User, UserProfileInfo

class UserForm(forms.ModelForm):
	password = forms.CharField(widget= forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
	class Meta:
		model = UserProfileInfo
		fields = ('bio', 'profile_pic')
