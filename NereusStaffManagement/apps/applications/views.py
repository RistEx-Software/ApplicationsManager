from django.shortcuts import render, get_object_or_404
from django.forms import ModelForm
from django import forms
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
	if request.user.has_perm("staff.listapps") or request.user.is_staff or request.user.is_superuser:
		applications = Application.objects.all() # Not actually an error, Visual Code misunderstanding.
		return render(request, 'applications/index.html', {'apps': applications})
	else:
		return render(request, 'applications/index.html')

def viewapplication(request, applicationid):
	application = get_object_or_404(Application, pk=applicationid)
	return render(request, 'applications/view.html', {'application': application})
