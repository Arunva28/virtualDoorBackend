from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     url(r'^vendor/$', login_required((views.vendorEdit.as_view()))),

        ]

