from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     #url('^accounts/', login_required(views.AccountsView.as_view())),
     url('^accounts/', login_required((views.AccountsView.as_view()))),
        ]

