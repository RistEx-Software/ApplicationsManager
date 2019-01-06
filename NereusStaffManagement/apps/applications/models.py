from django.db import models
from django.contrib.auth.models import User

TIME_CHOICES = (
	('1', '1-2 Hours'),
	('2', '2-4 Hours'),
	('3', '4-6 Hours'),
	('4', '6-8 Hours'),
	('5', 'More'),
)

# This is a staff application, they will likely
# need to register/login to use this.
class Application(models.Model):
	# Email, realname, and such will be included in the user.
	username = models.ForeignKey(User, on_delete=models.CASCADE)

	# The date they decided to make the application
	datetime = models.DateTimeField(auto_now=True)

	# User's in-game name
	ign = models.CharField(max_length=16)

	# User's Age
	age = models.IntegerField()

	# Gender
	gender = models.CharField(max_length=255)

	# Discord name
	discord = models.CharField(max_length=255)

	## Now for the questions in the form. ##

	# Do they have a microphone?
	microphone = models.BooleanField(default=False)
	# What country are they in?
	country = models.CharField(max_length=255, default="United States")
	# Can they screenshare?
	screenshare = models.BooleanField(default=False)
	# How much time can they spend on Nereus?
	timededication = models.CharField(max_length=2, choices=TIME_CHOICES, default='1')
	# Why should we hire them?
	hirereason = models.TextField(null=True)

	# the scenarios
	scenario1 = models.TextField(null=True)
	scenario2 = models.TextField(null=True)
	scenario3 = models.TextField(null=True)

	def GetName(self):
		if self.username.first_name and self.username.last_name:
			return "%s %s" % (self.username.first_name, self.username.last_name)
		else:
			return self.username.username
