"""ApplicationsManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path, include
from ApplicationsManager.apps.accounts import views as account_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'account/login.html'), name = 'login'),
   	path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
	path('register/', account_views.register, name = 'register'),
    path('', account_views.profile, name = 'profile'),
	
	# User lost their account.
	path('lost/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',
                                                    email_template_name='account/password_reset_email.txt', success_url="/account/lost/done/"), name='password_reset'),
	path('lost/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_email.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'account/password_confirm.html', success_url="/account/reset/done/"), name = 'password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_complete.html'),
	     name='password_reset_complete'),
	
	# A special impersonation feature for superusers.
	path('impersonate/', account_views.impersonate, name='impersonate'),
]
