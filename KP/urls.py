
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import homeview, view_post_detail,update_post,delete_post,share_post,shared_posts,delete_shared_post,CustomLogoutView,memberview,follow,HomeView

urlpatterns = [
    path('home2', HomeView.as_view(), name='home2'),
    path('admin/', admin.site.urls),
    path('', homeview.as_view(), name='home'),
    # path('', views.home, name='home'),
    path('login', views.login, name="login"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register', views.register, name="register"),
    path('member/', memberview.as_view(), name="member"),

    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/create_post/', views.create_post, name='create_post'),
    path('post/view_post_detail/<int:pk>/', view_post_detail.as_view(), name='view_post_detail'),
    path('post/update_post/<int:pk>/', update_post.as_view(), name='update_post'),
    path('post/delete_post/<int:pk>/', delete_post.as_view(), name='delete_post'),
    path('post/edited_post/<int:pk>/', views.post_detail, name='postdetail'),
    path('post/like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/share/', share_post, name='share_post'),
    path('post/shared/', views.shared_posts, name='shared_posts'), 
    path('post/shared/<int:share_id>/delete/', delete_shared_post, name='delete_shared_post'), 
    path('follow/<int:user_id>/', follow, name='follow'),
]
