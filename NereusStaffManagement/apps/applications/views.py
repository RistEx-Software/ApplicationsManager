
from django.shortcuts import render, get_object_or_404, Http404
from django.forms import ModelForm
from django import forms
from datetime import datetime
from NereusStaffManagement.apps.applications.models import Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
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
		# TODO: send a notification to interested parties.
		# Now we return the "Done" page.
		return render(request, 'applications/finished.html')
	else:
		form = CreateApplication(initial=request.GET)

	return render(request, 'applications/apply.html', {'form': form})


#@permission_required('staff.listapps')
def liststaffapps(request):
	pass

@login_required
def index(request):
	if request.user.has_perm("applications.viewallapps") or request.user.is_staff or request.user.is_superuser:
		allapplications = Application.objects.all()
		applications = Application.objects.filter(username=request.user)
		return render(request, 'applications/index.html', {'apps': allapplications, 'yourapps': applications})
	else:
		applications = Application.objects.filter(username=request.user)
		return render(request, 'applications/index.html', {'yourapps': applications})

@login_required
def viewapplication(request, applicationid):
	application = get_object_or_404(Application, pk=applicationid)

	# Staff member is making a change to it.
	if request.POST:
		if request.user.has_perm("applications.modifyapp") or request.user.is_staff or request.user.is_superuser or request.user == application.username:
			if 'AcceptApplication' in request.POST:

				# Only allow them to accept the application once, otherwise they can't do it but only if they're not changing status of the app.
				if (application.firstapproval == request.user or application.secondapproval == request.user) and application.status != '1':
					raise forms.FieldError("You can only be one acceptor on an application.")

				# If they're the first approval, set them as such. Otherwise set them as the second approver.
				if not application.firstapproval or application.status != '0':
					application.firstapproval = request.user
				elif not application.secondapproval:
					application.secondapproval = request.user
				else:
					# XXX: wat?
					raise forms.FieldError("Are you trying to accept an already accepted application?")

				# Okay, if they have both approvers, then the application is considered 'accepted'
				if application.firstapproval and application.secondapproval:
					application.status = '2'
					application.decisiontime = datetime.now()
				
				# Commit the changes to the database.
				application.save()

			elif 'DenyApplication' in request.POST:
				application.status = '1'
				application.decisiontime = datetime.now()
				application.firstapproval = request.user
				# TODO: Add denial reason to form somehow and save it here.
				application.save()

		else: # Yeet.
			raise Http404()

	if request.user.has_perm("applications.viewallapps") or request.user.is_staff or request.user.is_superuser or request.user == application.username:
		return render(request, 'applications/view.html', {'application': application})
	else:
		# They don't have access, so tell them this page doesn't exist.
		raise Http404()
