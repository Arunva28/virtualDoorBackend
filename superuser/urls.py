from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^addquerysuperuser/$', views.Registration.as_view()),
    url(r'^updatesuperuser/$', views.UpdateUserRights.as_view()),
   # url(r'^deleteuser/$', views.DeRegister.as_view()),
    ]