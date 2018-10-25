from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     #url('^accounts/', login_required(views.AccountsView.as_view())),
     url('^accounts/', login_required((views.AccountsView.as_view()))),
     url(r'^accounts_Dropdown/delete/(?P<Fields>.+?)/', login_required(views.AccountsDropdownviewDelete.as_view())),
     url('^accounts_Dropdown/', login_required((views.AccountsDropdownview.as_view()))),
     url('analyze/', login_required((views.Expenses.as_view()))),
     url('^all/', login_required((views.AllAccountsView.as_view())))
        ]

