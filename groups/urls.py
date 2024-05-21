# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_groups, name='view_groups'),
    path('my/', views.my_groups, name='my_groups'),
    # path(' popular/', views.view_popular_groups, name='view_popular_groups'),
    path('create/', views.create_group, name='create_group'),
    path('<slug:slug>/', views.group_detail, name='group_detail'),
    path('<slug:slug>/edit/', views.update_group, name='update_group'),
    path('<slug:slug>/delete/', views.delete_group, name='delete_group'),
    path('<slug:slug>/join/', views.join_group, name='join_group'),
    path('<slug:group_slug>/announcement/create/', views.create_announcement, name='create_announcement'),
    path('<slug:group_slug>/announcement/<slug:slug>/update/', views.update_announcement, name='update_announcement'),
    path('<slug:group_slug>/announcement/<slug:slug>/delete/', views.delete_announcement, name='delete_announcement'),
    path('announcements/', views.view_all_announcements, name='view_all_announcements'),
    path('announcement/<slug:slug>/', views.view_announcement_detail, name='view_announcement_detail'),
    path('<slug:group_slug>/events/', views.event_list, name='event_list'),
    path('<slug:group_slug>/events/create/', views.event_create, name='event_create'),
    path('<slug:group_slug>/events/<slug:event_slug>/', views.event_detail, name='event_detail'),
    path('<slug:group_slug>/events/<slug:event_slug>/update/', views.event_update, name='event_update'),
    path('<slug:group_slug>/events/<slug:event_slug>/delete/', views.event_delete, name='event_delete'),
    path('articles/<slug:article_slug>', views.view_group_article, name='view_group_article'),
    path('<slug:group_slug>/articles/create/', views.create_article, name='create_group_article'),
    path('articles/<slug:article_slug>/update/', views.update_article, name='update_group_article'),
    path('articles/<slug:article_slug>/publish/', views.publish_article, name='publish_article'),
    path('articles/', views.view_all_articles, name='view_all_articles'),
    path('articles/<slug:article_slug>', views.view_group_article, name='view_group_article'),
    path('articles/<slug:article_slug>/delete/', views.delete_article, name='delete_group_article'),
    path('articles/owned/', views.view_owned_articles, name='view_owned_articles'),
    path('articles/coauthored/', views.view_coauthored_articles, name='view_coauthored_articles'),
]

