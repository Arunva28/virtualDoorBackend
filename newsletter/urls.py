from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     url(r'^newsletter/$', login_required((views.newsletterEdit.as_view()))),
     url(r'^newsletter/delete/(?P<ID>.+?)/', login_required(views.NewsletterDelete.as_view())),

        ]

