from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     url(r'^society/$', login_required((views.SocietyEdit.as_view()))),
     url(r'^approvals/$', login_required((views.Societyapprovals.as_view()))),
     url(r'^groups/$', login_required((views.Societygroups.as_view()))),
     url(r'^groups/mypageapprovals/$', login_required((views.Mypage.as_view()))),

        ]

