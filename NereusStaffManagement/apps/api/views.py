from django.shortcuts import render
from django.http import JsonResponse
from django.template import Template, Context
from django import forms
from django.conf import settings
import requests
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

class SearchForm(forms.Form):
	query = forms.CharField(max_length=255)

# Create your views here.

def search(request):
	if request.POST:
		searchq = SearchForm(request.POST)
		if searchq.is_valid():
			objs = Application.objects.filter(name__unaccent__lower__trigram_similar=searchq.cleaned_data['query'])
			if not objs:
				return JsonResponse({"status": 0, "msg": "Not Found"})
			return JsonResponse({"status": 1, "msg": objs})
		else:
			return JsonResponse({"status": 0, "msg": "Invalid request"})
	else:
		return JsonResponse({"status": 0, "msg": "Invalid request"})
