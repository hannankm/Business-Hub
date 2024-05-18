from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile, Organization_Details

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        (False, 'Register as an Individual'),
        (True, 'Register as an Organization'),
    )

    is_org = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label='Register as'
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_org')
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'First Name'
                }),
                'last_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Last Name'
                }),
                'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Username'
                }),
                'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
                'password1': PasswordInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Password'
                }),
                'password2': PasswordInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Confirm Password'
                })
        }
    


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','username', 'email', 'is_org', 'phone_number', 'profile_pic', 'bio', 'headline')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'industry_interests': forms.CheckboxSelectMultiple
        }

class OrganizationDetailsForm(forms.ModelForm):
    class Meta:
        model = Organization_Details
        fields = ()

