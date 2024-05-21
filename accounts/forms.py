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
    



class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'is_org', 'phone_number', 'profile_pic', 'bio', 'headline')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Bio'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Headline'})
        }

class ProfileForm(forms.ModelForm):
    
    GENDER_CHOICES = (
        ('0', 'Male'),
        ('1', 'Female'),
    )
    EDUCATION_CHOICES = (
        ('PhD', 'PhD'),
        ('Bachelor', 'Bachelor'),
        ('Masters', 'Masters'),
        ('Highschool', 'Highschool'),
        ('None', 'None'),
    )
    EXPERIENCE_CHOICES = (
        ('Entry', 'Entry'),
        ('Intermediate', 'Intermediate'),
        ('Senior', 'Senior'),
        ('Expert', 'Expert'),
    )
    class Meta:
        model = Profile
        fields = ('position', 'gender', 'dob', 'education_level', 'education_field', 'experience_level', 'company')
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'gender': forms.RadioSelect(choices= (('0', 'Male'),('1', 'Female')),
    ),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'education_level': forms.Select(choices=(
         (
        ('PhD', 'PhD'),
        ('Bachelor', 'Bachelor'),
        ('Masters', 'Masters'),
        ('Highschool', 'Highschool'),
        ('None', 'None'),
    )
    ), attrs={'class': 'form-control'}),
            'education_field': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Education Field'}),
            'experience_level': forms.Select(choices=(
        ('Entry', 'Entry'),
        ('Intermediate', 'Intermediate'),
        ('Senior', 'Senior'),
        ('Expert', 'Expert'),
    ), attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
        }

class OrganizationDetailsForm(forms.ModelForm):
    class Meta:
        model = Organization_Details
        fields = ()

