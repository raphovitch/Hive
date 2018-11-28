from django import forms
from django.contrib.auth.models import User

class NewTweetForm(forms.Form):
	text = forms.CharField(max_length=140, widget=forms.Textarea)


class ProfileEditForm(forms.Form):
	email = forms.EmailField(required=False)
	username = forms.CharField(max_length=150)
	bio = forms.CharField(max_length=400)

	def clean(self):
		clean_data = super().clean()
		return clean_data