from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import ListView,  DetailView, UpdateView, DeleteView

from .models import Post,Like, Comment,Share
from .forms import postform, CommentForm

def register(request):
      if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']

        user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
        user.save()
        print("user create")

      return render(request, 'register.html')
    

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user})

def share_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        # Create a new share object for the current user and the post
        Share.objects.create(user=request.user, post=post)
        return redirect('shared_posts')  # Redirect to the shared posts page after sharing
    return render(request, 'share_post.html', {'post': post})

def shared_posts(request):
    shared_posts = Share.objects.filter(user=request.user).select_related('post').order_by('-shared_at')
    return render(request, 'shared.html', {'shared_posts': shared_posts})

    
def delete_shared_post(request, share_id):
    share = get_object_or_404(Share, pk=share_id, user=request.user)
    if request.method == 'POST':
        share.delete()
        return redirect('shared_posts')
    return render(request, 'delete_shared_post.html', {'share': share})


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    comments_dict = {post.pk: Comment.objects.filter(post=post).order_by('-created_at') for post in posts}
    return render(request, 'home.html', {'posts': posts, 'comments_dict': comments_dict})



@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        # If the like already exists, the user is unliking the post
        like.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def create_post(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        form = postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user 
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = postform()
    return render(request, 'create_post.html', {'form': form})

# 
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'postdetail.html', {'post': post})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Log the email and password
        print(f"Email: {email}")
        print(f"Password: {password}")

        # Authenticate manually
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.username}")  # Log user if found

            if user.check_password(password):
                auth_login(request, user)
                print("User logged in and redirected")
                return redirect('home')
                #  return redirect('profile', user_id=user.id)
                # return redirect('profile', username=user.username)
            else:
                print("Invalid password")  # Log if password is incorrect
                return render(request, 'login.html', {'error': 'Invalid password'})
        except User.DoesNotExist:
            print("No user with this email")  # Log if email does not exist
            return render(request, 'login.html', {'error': 'No user with this email'})

    return render(request, 'login.html')

class homeview(ListView):
    model = Post 
    template_name = 'home.html'
    ordering = ['-created_at']

class view_post_detail(DetailView):
    model = Post
    template_name = 'view_post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        form = CommentForm()
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(request.path_info)
        else:
            comments = Comment.objects.filter(post=post).order_by('-created_at')
            return self.render_to_response(self.get_context_data(form=form, comments=comments))

class update_post(UpdateView):
    model =  Post 
    template_name = 'update_post.html'
    fields =  ['title', 'text_content', 'file_content']

    def get_success_url(self):
        return reverse('postdetail', kwargs={'pk': self.object.pk})

class delete_post(DeleteView):
    model =  Post 
    template_name = 'delete_post.html'
    fields =  ['title', 'text_content', 'file_content']

    def get_success_url(self):
        return reverse('home')