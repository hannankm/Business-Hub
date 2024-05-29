
from django.contrib import admin
from django.urls import path
from . import views
from .views import  view_post_detail,update_post,delete_post,share_post,shared_posts,delete_shared_post,follow

urlpatterns = [
    # path('index', HomeView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    # path('', homeview.as_view(), name='home'),
    # path('member/', memberview.as_view(), name="member"),

    path('create/', views.create_post, name='create_post'),
    path('view_post_detail/<int:pk>/', view_post_detail.as_view(), name='view_post_detail'),
    path('update_post/<int:pk>/', update_post.as_view(), name='update_post'),
    path('delete_post/<int:pk>/', delete_post.as_view(), name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('<int:post_id>/share/', share_post, name='share_post'),
    path('shared/', views.shared_posts, name='shared_posts'), 
    path('shared/<int:share_id>/delete/', delete_shared_post, name='delete_shared_post'), 
]
