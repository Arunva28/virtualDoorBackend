from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     url(r'^staff/$', login_required((views.StaffEdit.as_view()))),

        ]

