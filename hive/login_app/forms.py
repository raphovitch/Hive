from django import forms
from django.core import validators


class LoginForm(forms.Form):
	username = forms.CharField(max_length=150)
	password = forms.CharField(widget=forms.PasswordInput())

	def clean(self):
		all_clean_data = super().clean()
		return all_clean_data

