from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django import forms

def user_exists(username):
	return User.objects.filter(username=username).exists()

class PasswordChangeForm(forms.Form):
	oldpassword = forms.CharField(max_length=255, label="Old Password")
	password1 = forms.CharField(max_length=255, label="Password")
	password2 = forms.CharField(max_length=255, label="Password (again)")

class PersonalInfoChange(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		labels = {
			'email': "E-Mail Address"
		}

# Create your views here.
class RegistrationForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password']

class ImpersonateForm(forms.Form):
	person = forms.CharField(max_length=255, label='Username')

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
				user = User.objects.get(username=form.cleaned_data.get('username'))
				auth.login(request, user)
				# Redirect them to the home.
				return HttpResponseRedirect(reverse('applications:index'))
	else:
		form = RegistrationForm(initial=request.GET)
		
	return render(request, 'account/register.html', {'form': form})


def profile(request):
	passwdfm = PasswordChangeForm(request.POST, initial=request.GET)
	personalfm = PersonalInfoChange(request.POST, initial=request.GET)

	if request.POST:
		if passwdfm.is_valid():
			# user changed their password -- verify the passwords match and update it.
			pass  # TODO
		if personalfm.is_valid():
			# User changed their personal account info, update it.
			pass  # TODO
	else:
		return render(request, 'account/profile.html', {'personalinfo': personalfm, 'passwordchange': passwdfm})

def impersonate(request):
	# First check if they're superuser, superuser can do anything
	if request.user.is_superuser:
		# Get the form data
		impernatee = ImpersonateForm(request.POST, initial=request.GET)
		# If they're posting, they're logging in as someone and not grabbing the form.
		if request.POST and impernatee.is_valid():
			# Check if the user exists at all.
			if not user_exists(impernatee.cleaned_data['person']):
				raise forms.ValidationError("User does not exist.")

			# Get that user object from the database
			user = User.objects.get(username=impernatee.cleaned_data['person'])
			# Authenticate them as that user.
			auth.login(request, user)
			# Redirect them to the homepage so they can see that user's home page.
			return HttpResponseRedirect(reverse('applications:index'))
		else:
			return render(request, 'account/impersonate.html', {'form': impernatee})
