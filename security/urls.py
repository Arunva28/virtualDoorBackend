from django.conf.urls import url
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^security/', login_required(views.SecurityOfficeView.as_view())),
        ]

