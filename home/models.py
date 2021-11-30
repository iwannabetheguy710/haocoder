from django.db import models
from django.contrib.auth.models import *

# Create your models here.
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