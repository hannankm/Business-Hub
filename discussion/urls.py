from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.discussion_forum, name="discussion_forum"),
    path('create/question/', views.create_question, name="create_question"),
    path('question/<int:question_id>/response/create/', views.create_response, name='create_response'),
    path('question/<int:question_id>/', views.question_detail, name="question_detail")
    # update question
    # update response
    # delete question
    # delete response 
    # view question 

    # path('profile/', views.profile, name="profile"),
    # path('edit/profile/', views.edit_profile, name="edit_profile"),
    # path('delete_account', views.delete_account, name="delete_account"),
    # path('follow/', views.follow, name="follow"),
    # path('unfollow/', views.unfollow, name="unfollow"),
    # path('followers/:id', views.view_followers, name="followers"),
    # path('following/:id', views.view_following, name="following")

]