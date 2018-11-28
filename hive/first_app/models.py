from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=400)
	profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
	follows = models.ManyToManyField('UserProfileInfo', related_name='followed_by', symmetrical=False, blank=True)

	def __str__(self):
		return (self.user.username)


class Tweet(models.Model):
	title = models.CharField(max_length=140, unique=False)
	text = models.CharField(max_length=140, unique=False)
	date = models.DateField()
	user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)

	liked_by = models.ManyToManyField('UserProfileInfo', related_name='likes', blank=True)


	def __str__(self):
		return self.title