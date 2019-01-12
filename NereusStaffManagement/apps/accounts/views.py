from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth
from django.urls import reverse
from django import forms

def user_exists(username):
	return User.objects.filter(username=username).exists()

class PasswordChangeForm(forms.Form):
	oldpassword = forms.CharField(max_length=255, label="Old Password", widget=forms.PasswordInput)
	password1 = forms.CharField(max_length=255, label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(max_length=255, label="Password (again)", widget=forms.PasswordInput)

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
	personalfm = PersonalInfoChange(request.POST, instance=request.user)

	if request.POST: 
		if passwdfm.is_valid():
			# user changed their password -- verify the old password and that the passwords match then update it.
			user = authenticate(username=request.user.username, password=passwdfm.cleaned_data.get('oldpassword'))
			
			if not user:
				# Should really change to a notification.
				raise forms.ValidationError("Your password was incorrect.")

			passwd1 = passwdfm.cleaned_data.get('password1')
			passwd2 = passwdfm.cleaned_data.get('password2')

			# Compare the two passwords, this can be done in JS as well but Django does enforcement.
			if passwd1 != passwd2:
				# Should really change to a notification.
				raise forms.ValidationError("Your passwords do not match.")

			if not validate_password(passwd1, user=request.user):
				# Should really change to a notification.
				raise forms.ValidationError("Your password does not meet the strength requirements")

			request.user.set_password(passwd1)
			request.user.save()

			# XXX: TODO: make some kind of notification, probably javascript but this whole func should be AJAX
			# Green Notification box that appears at where it suits best
			return HttpResponseRedirect(reverse("account:profile"))

		if personalfm.is_valid():
			# User updated their information.
			personalfm.save()
			# TODO: make this AJAX instead.
			return HttpResponseRedirect(reverse("account:profile"))
		else:
			raise forms.ValidationError("You have an error in your stuff")

		# They did an invalid submit. Return 404.
		raise Http404()
	else:
		# we have to reinstantiate it because the form will not auto-fill if we do it once.
		personalfm = PersonalInfoChange(instance=request.user)
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
