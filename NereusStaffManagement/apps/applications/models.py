from django.db import models
from django.contrib.auth.models import User

TIME_CHOICES = (
	('1', '1-2 Hours'),
	('2', '2-4 Hours'),
	('3', '4-6 Hours'),
	('4', '6-8 Hours'),
	('5', 'More'),
)

APPLICATION_STATUS = (
	('0', 'Pending'),
	('1', 'Denied'),
	('2', 'Approved'),
)

# This is a staff application, they will likely
# need to register/login to use this.
class Application(models.Model):
	# Email, realname, and such will be included in the user.
	username = models.ForeignKey(User, on_delete=models.DO_NOTHING)

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

	# Status -- are they pending, approved, or denied?
	status = models.CharField(max_length=2, choices=APPLICATION_STATUS, default='0')
	# The first staff member to approve it
	firstapproval = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="firstapproval", null=True, blank=True)
	# The second staff member to approve it
	secondapproval = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="secondapproval", null=True, blank=True)

	# The approval time
	decisiontime = models.DateTimeField(null=True)

	# If they were not approved, what was their denial reason?
	denialreason = models.TextField(null=True, blank=True)

	#def __str__(self):
		#return "%s's application on %s" % (self.GetName, self.datetime)
