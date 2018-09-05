from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     url(r'^updatefeedback/$', login_required((views.UpdateFeedback.as_view()))),
     url(r'^complaints_dropdown/$', login_required((views.ComplaintsDropdownview.as_view()))),
     url(r'addcomplaint/$', login_required((views.ComplaintsView.as_view()))),
     url(r'^updatestatus/$', login_required((views.UpdateStatus.as_view())))
        ]

