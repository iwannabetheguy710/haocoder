from django.db import models
from django.contrib.auth.models import *

from martor.models import MartorField

class Announcement(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=1000, default='')
	content = MartorField(default='')
	visible = models.BooleanField(default=True)
	publish_date = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.title

class Profile(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	win = models.IntegerField(default=0)
	ratings = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
	highest_ratings = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
	role = models.CharField(max_length=100, default='Class H')
	highest_role = models.CharField(max_length=100, default='Class H')
	color = models.CharField(max_length=7, default='gray')
	highest_color = models.CharField(max_length=7, default='gray')

	def __str__(self):
		return self.user.username