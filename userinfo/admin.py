from django.contrib import admin
from .models import BasicUserInfo
from django.contrib.auth.admin import UserAdmin
#from .forms import UserCreationForm


# Register your models here.

# class BasicUserAdmin(UserAdmin):
#     print("somw")
#     pass
#
#
# class CustomUserAdmin(UserAdmin):
#     print(("some1"))
#     # The forms to add and change user instances
#     add_form = UserCreationForm
#     list_display = ("email",)
#     ordering = ("email",)
#
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')}),
#         )
#
#     filter_horizontal = ()
#
# #admin.site.unregister(BasicUserInfo)
#

admin.site.register(BasicUserInfo, UserAdmin)
