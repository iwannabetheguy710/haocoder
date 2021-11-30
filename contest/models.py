from django.db import models
from django.contrib.auth.models import *
from home.models import *
from martor.models import MartorField

from datetime import *

CONTEST_FORMAT = [
	("AtCoder", "AtCoder"),
	("ACM", "ACM"),
	("OI", "OI"),
]
CONTEST_STATUS = [
	("SCHEDULE", "Schedule"),
	("RUNNING", "Running"),
	("ARCHIVED", "Archived"),
]


class Contest(models.Model):
	contest_id = models.CharField(max_length=100, default='', primary_key=True)
	contest_title = models.CharField(max_length=500, default='')
	contest_description = MartorField(default='')
	contest_format = models.CharField(max_length=100, default='OI', choices=CONTEST_FORMAT)
	contest_rating_range = models.CharField(max_length=50, default='0-5000')
	contestant_count = models.IntegerField(default=0)
	contest_created = models.DateTimeField(auto_now_add=True, blank=True)
	contest_schedule = models.DateTimeField(default=datetime.now)
	contest_long = models.CharField(max_length=20, default="01:00:00")
	contest_status = models.CharField(max_length=50, default="SCHEDULE", choices=CONTEST_STATUS)
	contest_rated = models.BooleanField(default=True)

	def __str__(self):
		return self.contest_title

class Leaderboard(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
	ranking = models.IntegerField(default=1)
	scoring = models.CharField(default='0', blank=True, max_length=300)
	total_score = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
	total_time = models.CharField(default='00:00:00', max_length=50)
	def __str__(self):
		return f"{self.contest.contest_title}: contestant - {self.profile.user.username}"

class Problem(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
	contest_problem_id = models.CharField(default='A', max_length=1)
	problem_id = models.CharField(default='', max_length=50)
	problem_title = models.CharField(default='', max_length=100)
	problem_description = MartorField(default='')
	problem_sample_in = models.TextField(default='')
	problem_sample_out = models.TextField(default='')
	problem_hidden_in = models.TextField(default='')
	problem_hidden_out = models.TextField(default='')
	problem_time_limit = models.DecimalField(default=1.000, max_digits=5, decimal_places=3)
	problem_memory_limit = models.IntegerField(default=65536)
	problem_score = models.DecimalField(default=100.0, max_digits=6, decimal_places=2)
	publish_date = models.DateTimeField(auto_now_add=True, blank=True)
	problem_accepted = models.IntegerField(default=0)
	problem_wrongans = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.contest.contest_title}: Problem {self.problem_title}"
