from django import forms
from django.contrib.auth.models import User

class NewTweetForm(forms.Form):
	title = forms.CharField(max_length=140)
	text = forms.CharField(max_length=140, widget=forms.Textarea)


class ProfileEditForm(forms.Form):
	email = forms.EmailField(required=False)
	username = forms.CharField(max_length=150)
	bio = forms.CharField(max_length=400)

	def clean(self):
		clean_data = super().clean()
		return clean_data



class PasswordEditForm(forms.Form):
	old_password = forms.CharField(widget= forms.PasswordInput())
	new_password = forms.CharField(widget= forms.PasswordInput())
	new_password_confirmation = forms.CharField(widget= forms.PasswordInput())

	def clean(self):
		clean_data = super().clean()
		new_pass = clean_data['new_password']
		new_pass_conf = clean_data['new_password_confirmation']
		if new_pass != new_pass_conf:
			raise forms.ValidationError('Make sure new passwords matchs.')

		return clean_data