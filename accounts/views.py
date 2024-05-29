from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, ProfileForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from posts.models import PostShare, Post
from . import models
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm


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

            # Create a profile object for the user
            models.Profile.objects.create(user=user)

            login(request, user)
            return redirect('home')  # Redirect to a success page.
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# add interest
def home(request):
    context = {}
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(posted_by=request.user)
        followed_users = models.Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        followed_users_posts = Post.objects.filter(posted_by__in=followed_users)
        all_posts = user_posts | followed_users_posts
        all_posts = all_posts.order_by('-created_at')  # Order by the creation date

        context['posts'] = all_posts
        return render(request, 'accounts/home.html', context)
    
    return render(request, 'accounts/guests.html')


    

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(models.CustomUser, id=user_id)
    if request.user != user_to_follow:
        follow, created = models.Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            # If already following, unfollow
            follow.delete()

    
        # Update follower count and following count for both users
        request.user.following_count = request.user.following.count()
        request.user.save()
        user_to_follow.follower_count = user_to_follow.followers.count()
        user_to_follow.save()
    return redirect('home')  # Adjust the redirect URL as needed

@login_required
def view_followers(request, user_id):
    user = get_object_or_404(models.CustomUser, id=user_id)
    followers = models.Follow.objects.filter(following=user)
    return render(request, 'accounts/followers.html', {'user': user, 'followers': followers})

@login_required
def view_following(request, user_id):
    user = get_object_or_404(models.CustomUser, id=user_id)
    following = models.Follow.objects.filter(follower=user)
    return render(request, 'accounts/following.html', {'user': user, 'following': following})

@login_required
def profile(request):
    today = timezone.now()
    user = request.user
    profile, created = models.Profile.objects.get_or_create(user=user)
    userInfo = models.CustomUser.objects.get(username=user)
    shared_posts = PostShare.objects.filter(user=request.user).select_related('post').order_by('-shared_at')
    user_posts = Post.objects.filter(posted_by=request.user)

    followers = models.Follow.objects.filter(following=user)
    following = models.Follow.objects.filter(follower=user)
    # followers, following 
    return render(request, 'accounts/my_profile.html', {
        'profile': profile,
        'user': userInfo,
        'today': today,
        'shared_posts': shared_posts,
        'user_posts': user_posts,
        'followers': followers,
        'following': following
    
    })

def profile_view(request, username):
    user = get_object_or_404(models.CustomUser, username=username)
    profile = get_object_or_404(models.Profile, user =user)
    shared_posts = PostShare.objects.filter(user=user).select_related('post').order_by('-shared_at')
    user_posts = Post.objects.filter(posted_by=user)
    followers = models.Follow.objects.filter(following=user)
    following = models.Follow.objects.filter(follower=user)
    is_following = models.Follow.objects.filter(follower=request.user, following=user).exists()

    return render(request, 'accounts/profile.html', {'user': user, 'profile': profile, 'shared_posts': shared_posts, 'user_posts': user_posts, 'followers': followers,'following': following,         'is_following': is_following
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
            return redirect('my_profile')  # Redirect to a profile view or another page
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Logic to delete the account
        request.user.delete()
        logout(request)
        return redirect('home')  # Redirect to home page after deletion
    return render(request, 'accounts/delete_account.html')



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

