from django.shortcuts import render, Http404, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from NereusStaffManagement.apps.staffmgmt.models import WriteUp
from NereusStaffManagement.apps.api.views import _ManagerMessage, _TemplateManagerMessage
from django.contrib.auth.decorators import login_required

# Create your views here.
class WriteUpForm(forms.ModelForm):
	class Meta:
		model = WriteUp
		exclude = ['owner', 'official']

		labels = (
			('suspect', "Staff Member"),
			('subject', "Subject"),
			('explanation', "Please explain your write-up:"),
		)


# This is to show all the writeups for the staff
# Only management can view this page.
@login_required
def viewwriteups(request):
	if not request.user.is_superuser: # Redirect users to the new write-up form.
		return HttpResponseRedirect(reverse("staffmgmt:new"))
	
	writeups = WriteUp.objects.all()
	return render(request, 'staffmgmt/list_writeups.html', {"writeups": writeups})

# View an individual writeup
@login_required
def viewwriteup(request, writeupid):
	writeup = get_object_or_404(WriteUp, pk=writeupid)

	if not request.user.is_superuser:
		return Http404()
	
	return render(request, 'staffmgmt/view_writeup.html', {'writeup': writeup})


# Make a writeup, can be either positive or negative.
# Any staff member can write-up another staff member.
@login_required
def writeup(request):
	# Don't allow randoms to make writeups
	if not request.user.is_staff and not request.user.is_superuser:
		print("hahaha get 404'd bitch!")
		print("is_staff = %d\nis_superuser = %d" % (request.user.is_staff, request.user.is_superuser))
		raise Http404()
	
	form = WriteUpForm(request.POST, initial=request.GET)
	if request.POST and form.is_valid():
		commit = form.save(commit=False)
		commit.owner = request.user
		commit.save()
		# Notify the different parties.
		_TemplateManagerMessage("{% load fuckyouzach %}"
		"{{ form.owner|getname }} wrote up {{ form.suspect|getname }}:\n"
		"```\n"
		"{{ form.subject }}\n"
		"```", form=commit)
		# return a page to the web user.
		return render(request, 'staffmgmt/writeup_complete.html')
	else:
		return render(request, 'staffmgmt/writeup.html', {"form": form})
