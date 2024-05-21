from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_, name="login"),
    path('logout/', views.logout_, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/my', views.profile, name="my_profile"),
    path('edit/profile/', views.edit_profile, name="edit_profile"),
    path('delete_account', views.delete_account, name="delete_account"),
    path('follow/', views.follow, name="follow"),
    path('unfollow/', views.unfollow, name="unfollow"),
    path('followers/:id', views.view_followers, name="followers"),
    path('following/:id', views.view_following, name="following")

]