from django.shortcuts import render, get_object_or_404, Http404
from django.forms import ModelForm
from django import forms
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from NereusStaffManagement.apps.applications.models import Application
from NereusStaffManagement.apps.api.views import _ManagerMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.template import Template, Context
from django.utils.translation import gettext_lazy as _

# Create your views here.
class CreateApplication(ModelForm):
	class Meta:
		model = Application
		fields = ['ign', 'age', 'gender', 'discord', 'microphone', 'country',
                    'screenshare', 'timededication', 'hirereason', 'scenario1', 'scenario2', 'scenario3']
		labels = {
			'ign': _('In-Game Name'),
			'age': _('Age'),
			'gender': _('Gender'),
			'discord': _('Discord ID'),
			'microphone': _('Do you have a microphone?'),
			'country': _('What country do you live in?'),
			'screenshare': _('Can you screen share?'),
			'timededication': _('How much time can you dedicate to Nereus?'),
			'hirereason': _('Is there anything specific that inspired you to want to join the staff team?'),
			'scenario1': _('A player has begun an argument with another player and now they are both arguing in the chat constantly. What do you do?'),
			'scenario2': _('A player has found a bug and they have continued to abuse the bug without telling any staff. What do you do?'),
			'scenario3': _('A player has been caught scamming others for in-game items causing other players to get annoyed and toxic in the chat. What do you do?'),
		}

		widgets = {
                    'scenario1': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'textarea'}),
					'scenario2': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'textarea'}),
					'scenario3': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'textarea'}),
					'hirereason': forms.Textarea(attrs={'rows': 10, 'cols': 90, 'class': 'textarea'}),
                }

class GiveDenialReason(forms.Form):
	reason = forms.CharField(widget=forms.Textarea)

@login_required
def apply(request):
	# The user wants to apply.

	form = CreateApplication(request.POST, initial=request.GET)
	if request.POST and form.is_valid():
		# the user clicked submit. Check their details
		someform = form.save(commit=False)
		someform.username = request.user
		# Save the items to the database for later
		someform.save()
		revbersed = request.build_absolute_uri(reverse("applications:view", kwargs={"applicationid": someform.pk}))
		# Let interested parties know

		# Send a notification to Discord, I made this a template because it was MUCH easier to render
		# the message this way.
		t = Template("""{{request.user}} has filed an application to become staff on Nereus. {{reversed}}
			```
Username: {{someform.username.username}}
Real Name: {{ someform.username.get_full_name }}
Email: {{ someform.username.email }}
In-Game Name: {{someform.ign}}
Age: {{someform.age}}
Gender: {{someform.gender}}
Discord ID: {{someform.discord}}
Country: {{ someform.country }}
Has microphone: {{ someform.microphone|yesno }}
Can screenshare: {{ someform.screenshare|yesno }}
Time dedication: {{ someform.get_timededication_display }}```
			""")

		# Actually send the message in Discord
		_ManagerMessage(t.render(Context({'someform': someform, 'request': request, 'reversed': revbersed})))
		# Now we return the "Done" page.
		return render(request, 'applications/finished.html')
	else:
		form = CreateApplication(initial=request.GET)

	return render(request, 'applications/apply.html', {'form': form})

@login_required
def denialreason(request, applicationid):
	if request.user.is_superuser:
		obj = get_object_or_404(Application, pk=applicationid)
		form = GiveDenialReason(request.POST)

		if request.POST and form.is_valid():
			obj.status = '1'
			obj.decisiontime = datetime.now()
			obj.firstapproval = request.user
			obj.denialreason = form.cleaned_data.get('reason')

			_ManagerMessage(f"{request.user} denied {obj.username}'s application for the reason :\n`{obj.denialreason}`")
			obj.save()
			# Eventually need to add a thing of what type of application was wrote/got denied/got accepted.
			return HttpResponseRedirect(reverse("applications:view", kwargs={"applicationid": obj.pk}))

		return render(request, 'applications/denial.html', {'form': form, "app": obj})
	else:
		raise Http404()

@login_required
def index(request):
	if request.user.has_perm("applications.viewallapps") or request.user.is_superuser:
		allapplications = Application.objects.all().order_by('-datetime')
		applications = Application.objects.filter(username=request.user).order_by('-datetime')
		return render(request, 'applications/index.html', {'apps': allapplications, 'yourapps': applications})
	else:
		applications = Application.objects.filter(username=request.user).order_by('-datetime') 
		return render(request, 'applications/index.html', {'yourapps': applications})

@login_required
def viewapplication(request, applicationid):
	application = get_object_or_404(Application, pk=applicationid)

	# Staff member is making a change to it.
	if request.POST:
		if request.user.has_perm("applications.modifyapp") or request.user.is_superuser or request.user == application.username:
			if 'AcceptApplication' in request.POST:
				# Only allow them to accept the application once, otherwise they can't do it but only if they're not changing status of the app.
				if (application.firstapproval == request.user or application.secondapproval == request.user) and application.status != '1':
					#raise forms.ValidationError("You can only be one acceptor on an application.")
					return HttpResponse("$.notify( 'You can only be one acceptor on an application.', { position:'bottom, right', className: 'error' } );", content_type="text/javascript")
					# Should be below but is causing errors right now.
					# raise forms.FieldError("You can only be one acceptor on an application.")

				# If they're the first approval, set them as such. Otherwise set them as the second approver.
				if not application.firstapproval or application.status != '0':
					application.firstapproval = request.user
				elif not application.secondapproval:
					application.secondapproval = request.user
				else: # In-case a user some how sends data to accept an already accepted application
					# XXX: wat?
					raise forms.ValidationError("Are you trying to accept an already accepted application?")
					# Should be below but is causing errors right now.
					# raise forms.FieldError("Are you trying to accept an already accepted application?")

				# Okay, if they have both approvers, then the application is considered 'accepted'
				if application.firstapproval and application.secondapproval:
					application.status = '2'
					application.decisiontime = datetime.now()
					# Grant the user the staff permission.
					application.username.is_staff = True
					application.username.save()
					_ManagerMessage(f"{request.user} and {application.firstapproval} approved {application.username}'s application.")
				
				# Commit the changes to the database.
				application.save()
			elif 'DenyApplication' in request.POST:
				# redirect to a whole new page.
				return HttpResponseRedirect(reverse("applications:denial", kwargs={"applicationid": application.pk}))
			elif 'CancelApplication' in request.POST and request.user == application.username:
				# The user wants to cancel their application
				application.status = '3'
				application.decisiontime = datetime.now()
				application.save()
				_ManagerMessage(f"{request.user} cancelled their application made on {application.datetime}.")
		else: # Yeet
			raise Http404()

	if request.user.has_perm("applications.viewallapps") or request.user.is_superuser or request.user == application.username:
		return render(request, 'applications/view.html', {'application': application})
	else:
		# They don't have access, so tell them this page doesn't exist.
		raise Http404()
