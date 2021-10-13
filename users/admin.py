from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()

admin.site.register(User)
'''
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'code_number', 'first_name', 'last_name']

admin.site.register(User, CustomUserAdmin)
'''

admin.site.site_header = 'DREM INTERNATIONAL ADMIN PAGE'