# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/new/', views.article_create, name='article_create'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/edit/', views.article_update, name='article_update'),
    path('article/<slug:slug>/delete/', views.article_delete, name='article_delete'),
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
    path('liked-articles/', views.view_liked_articles, name='view_liked_articles'),
    path('popular-articles/', views.view_popular_articles, name='view_popular_articles'),
    path('media/', views.media_list, name='media_list'),
    path('media/upload/', views.upload_media, name='upload_media'),
    path('media/<slug:slug>/download/', views.download_media, name='download_media'),
    path('media/<slug:slug>/update/', views.update_media, name='update_media'),
    path('media/<slug:slug>/delete/', views.delete_media, name='delete_media'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/<slug:slug>/update/', views.update_document, name='update_document'),
    path('documents/<slug:slug>/delete/', views.delete_document, name='delete_document'),
    path('documents/<slug:slug>/download/', views.download_document, name='download_document'),
    path('documents/', views.document_list, name='document_list'),

]