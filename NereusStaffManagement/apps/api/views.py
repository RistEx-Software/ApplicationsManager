from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.template import Template, Context
from django import forms
from django.conf import settings
import requests, json
from NereusStaffManagement.apps.applications.models import Application

# This is mostly an internal function for sending messages to discord
def _ManagerMessage(message):
	content = {
		"content":message
	}
	requests.post(settings.DISCORD_WEBHOOK, json=content)

# Just a shortcut function to the above for rendering a templated string.
def _TemplateManagerMessage(messagecode, **kwargs):
	t = Template(messagecode)
	_ManagerMessage(t.render(Context(kwargs)))

# Handle 404 errors
def page_not_found(request, exception):
	return render(request, '404.html', status=404)

# Handle 500 errors
def server_error(request):
	return render(request, '500.html', status=500)

class SearchForm(forms.Form):
	query = forms.CharField(max_length=255)

# Create your views here.
def search(request):
	if request.POST:
		searchq = SearchForm(request.POST)
		if searchq.is_valid():

			query = searchq.cleaned_data.get('query')
			# Okay here's where things get fun. We don't allow the users/staff to view
			# other people's applications, but superusers can view it. This affects
			# search as they should not search for applications by anyone other than themselves.
			objs = None

			if request.user.is_superuser:
				objs1 = Application.objects.filter(discord__icontains=query)
				objs2 = Application.objects.filter(ign__icontains=query)
				objs3 = Application.objects.filter(username__username__icontains=query)
				objs4 = Application.objects.filter(username__first_name__icontains=query)
				objs5 = Application.objects.filter(username__last_name__icontains=query)
				objs6 = Application.objects.filter(username__email__icontains=query)
				objs = objs1 | objs2 | objs3 | objs4 | objs5 | objs6
			else:
				# They're not a superuser, just search within their own applications.
				objs1 = Application.objects.filter(discord__icontains=query, username=request.user)
				objs2 = Application.objects.filter(ign__icontains=query, username=request.user)
				# pointless query but whatever.
				objs3 = Application.objects.filter(username__username__icontains=query, username=request.user)
				objs = objs1 | objs2 | objs3

			
			if not objs:
				return JsonResponse({"status": 0, "msg": "Not Found"})
			
			# We don't just want to blast all the user's info out into the world
			# so first what we do is check if they're admin or not.
			results = []
			for app in objs:
				results.append({
					"username": app.username.username,
					"ign": app.ign,
					"discord": app.discord,
					"applicationid": app.pk,
					"email": app.username.email if request.user.is_superuser else None,
					"firstname": app.username.first_name if request.user.is_superuser else None,
					"lastname": app.username.last_name if request.user.is_superuser else None})
			return JsonResponse({"status": 1, "msg": "Results", "objects": results})
		else:
			return JsonResponse({"status": 0, "msg": "Not Found"})
	else:
		return JsonResponse({"status": 0, "msg": "Invalid request"})
