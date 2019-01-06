from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django import forms

def user_exists(username):
	return User.objects.filter(username=username).exists()

# Create your views here.
class RegistrationForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password']

def register(request):
	if request.user.is_authenticated:
		raise Http404("You're already logged in")
	
	form = RegistrationForm(request.POST, initial=request.GET)

	if request.POST and form.is_valid():
		if not form.errors:
			if user_exists(form.cleaned_data.get('username')):
				raise forms.ValidationError("Sorry, this username is taken.")
			else:
				# The user can register, save the form.
				form.save()
				# now log them in.
				auth.login(request, form.cleaned_data.get('username'))
				# Redirect them to the home.
				return HttpResponseRedirect(reverse('index'))

	else:
		form = RegistrationForm(initial=request.GET)
	

	return render(request, 'account/register.html', {'form': form})


def profile(request):
	return render(request, 'account/profile.html')

def impersonate(request):
	pass