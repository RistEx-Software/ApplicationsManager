"""NereusStaffManagement URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from NereusStaffManagement.apps.api import views as api_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('NereusStaffManagement.apps.applications.urls', 'applications'), namespace='applications')),
    path('account/', include(('NereusStaffManagement.apps.accounts.urls', 'account'), namespace = 'account')),
    path('writeup/', include(('NereusStaffManagement.apps.staffmgmt.urls', 'staffmgmt'), namespace = 'staffmgmt')),
    path('api/', include(('NereusStaffManagement.apps.api.urls', 'api'), namespace = 'api')),
    path('doc/', include(('NereusStaffManagement.apps.docs.urls', 'docs'), namespace='docs')),
]

# Set our 404 and 500 error pages
handler404 = api_views.page_not_found
handler500 = api_views.server_error
