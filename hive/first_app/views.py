from django.shortcuts import render, redirect
from django.http import HttpResponse
from first_app.models import Tweet
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	return render(request, 'index.html')


def gets_lasts_tweets(n=10):
	lasts_tweets ={
	'list' : Tweet.objects.all().order_by('-date')[:n]
	} 
	return lasts_tweets


def home(request):
	return render(request, 'home.html',context=gets_lasts_tweets())
