from django.db import models
from django.contrib.auth.models import User

# The write-up.
class WriteUp(models.Model):
	# The person who made the writeup
	owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

	# This is only available to upper-staff/management/whatever
	# and will send a notification to the user in question.
	# TODO: This probably needs to DM the user directly once implemented.
	official = models.BooleanField(default=False)

	# the person in question
	suspect = models.ForeignKey(User, on_delete=models.DO_NOTHING)

	# Subject/summary of the writeup. It's limited cuz it's a summary not a fucking novel.
	subject = models.CharField(max_length=128)

	# This is where your novel goes.
	explanation = models.TextField()

