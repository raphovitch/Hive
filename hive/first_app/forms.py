from django import forms
from django.contrib.auth.models import User

class NewTweetForm(forms.Form):
	text = forms.CharField(max_length=140, widget=forms.Textarea)