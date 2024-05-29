from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView,  DetailView, UpdateView, DeleteView
from accounts.models import Follow 
from .models import Post,PostLike, PostComment,PostShare
from .forms import postform, CommentForm

User = get_user_model()

@login_required
def follow(request, user_id):
    if request.method == 'POST':
        user_to_follow = User.objects.get(pk=user_id)
        follow_instance, created = Follow.objects.get_or_create(user=request.user)
        follow_instance.following.add(user_to_follow)
        return HttpResponseRedirect(reverse('member'))  # Redirect back to the member page
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect back to the previous page
        # return redirect('profile', user_id=user_id) 
    

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user})

def share_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        # Create a new share object for the current user and the post
        PostShare.objects.create(user=request.user, post=post)
        return redirect('home')  # Redirect to the shared posts page after sharing
    return render(request, 'share_post.html', {'post': post})

def shared_posts(request):
    shared_posts = PostShare.objects.filter(user=request.user).select_related('post').order_by('-shared_at')
    return render(request, 'shared.html', {'shared_posts': shared_posts})

    
def delete_shared_post(request, share_id):
    share = get_object_or_404(PostShare, pk=share_id, user=request.user)
    if request.method == 'POST':
        share.delete()
        return redirect('home')
    return render(request, 'delete_shared_post.html', {'share': share})


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    comments_dict = {post.pk: PostComment.objects.filter(post=post).order_by('-created_at') for post in posts}
    return render(request, 'home.html', {'posts': posts, 'comments_dict': comments_dict})



@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        # If the like already exists, the user is unliking the post
        like.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def create_post(request):
    if request.method == 'POST':
        form = postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user 
            post.save()
            request.user.post_count += 1
            request.user.save()
            return redirect('home')
    else:
        form = postform()
    return render(request, 'create_post.html', {'form': form})



class view_post_detail(DetailView):
    model = Post
    template_name = 'view_post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = PostComment.objects.filter(post=post).order_by('-created_at')
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
            comments = PostComment.objects.filter(post=post).order_by('-created_at')
            return self.render_to_response(self.get_context_data(form=form, comments=comments))

class update_post(UpdateView):
    model =  Post 
    template_name = 'update_post.html'
    fields =  ['title', 'text_content', 'file_content']

    def get_success_url(self):
        return reverse('postdetail', kwargs={'pk': self.object.pk})
    
class delete_post(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    fields = ['title', 'text_content', 'file_content']

    def delete(self, request, *args, **kwargs):
        # Get the post object
        post = self.get_object()

        # Decrement the post count for the author
        author_profile = post.posted_by.profile
        author_profile.post_count -= 1
        author_profile.save()

        # Call the delete() method to delete the post
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')