from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username', 'email', 'is_org', 'phone_number', 'profile_pic', 'bio', 'headline', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_org', 'phone_number', 'profile_pic', 'bio', 'headline')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_org', 'phone_number', 'profile_pic', 'bio', 'headline')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
