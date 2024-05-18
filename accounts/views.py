from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from . import models



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_org = form.cleaned_data.get('is_org') == 'True'
            user.phone_number = form.cleaned_data.get('phone_number')
            user.profile_pic = form.cleaned_data.get('profile_pic')
            user.bio = form.cleaned_data.get('bio')
            user.headline = form.cleaned_data.get('headline')
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page.
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# add interest
def home(request):
    context={}
    if request.user.is_authenticated:
        request.user 
        return render(request, 'accounts/home.html', context=context)
    return render(request, 'accounts/guests.html', )

def follow(requests):
    return render()

def unfollow(requests):
    return

@login_required
def profile(request):
    user = request.user
    profile, created = models.Profile.objects.get_or_create(user=user)
    userInfo = models.CustomUser.objects.get(username=user)
    
    # followers, following 
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'user': userInfo
    })

@login_required
def edit_profile(request):
    user = request.user
    profile, created = models.Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to a profile view or another page
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    return

def delete_account(requests):
    return

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired redirect URL after login
            else:
                form.add_error(None, 'Invalid username or password.')  # Add non-field error
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_(request):
    logout(request)
    return redirect('home')

def view_followers(requests):
    return

def view_following(requests):
    return 

# maybe can be as a checkbox in edit profile
def addInterest(requests):
    return