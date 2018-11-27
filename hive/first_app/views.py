from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from first_app.forms import NewTweetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
	return render(request, 'index.html')

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