from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse('Hello Project Hive\n Pour vous dire raph est une pute')