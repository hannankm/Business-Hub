from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Like, Media, Document
from .forms import ArticleForm, CommentForm, MediaForm, DocumentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import FileResponse, JsonResponse, HttpResponseForbidden
from django.utils.safestring import mark_safe



def article_list(request):
    sort_by = request.GET.get('sort_by', 'recent')
    search_query = request.GET.get('search', '')

    if sort_by == 'earliest':
        articles = Article.objects.order_by('created_at')
    elif sort_by == 'most_likes':
        articles = Article.objects.order_by('-like_count', '-comment_count')
    else:  # Default to 'recent'
        articles = Article.objects.order_by('-created_at')

    if search_query:
        articles = articles.filter(title__icontains=search_query)

    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request, 'resources/articles.html', {'articles': articles, 'sort_by': sort_by, 'search_query': search_query})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments_list = article.comments.all()
    paginator = Paginator(comments_list, 10)  # 10 comments per page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    form = CommentForm()
    user_has_liked = article.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    article.content = mark_safe(article.content)  # Mark content as safe

    return render(request, 'resources/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'user_has_liked': user_has_liked,
    })


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'resources/article_form.html', {'form': form})

@login_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'resources/article_form.html', {'form': form})

@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'resources/article_confirm_delete.html', {'article': article})

@login_required
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            article.update_comment_count()
            return redirect('article_detail', slug=article.slug)
    return redirect('article_detail', slug=article.slug)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        article_slug = comment.article.slug
        comment.delete()
        comment.article.update_comment_count()
        return redirect('article_detail', slug=article_slug)
    return render(request, 'resources/comment_confirm_delete.html', {'comment': comment})

@login_required
def like_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, article=article)
    if not created:
        like.delete()
        article.update_like_count()
        return JsonResponse({'status': 'unliked', 'like_count': article.like_count})
    else:
        article.update_like_count()
        return JsonResponse({'status': 'liked', 'like_count': article.like_count})


@login_required
def view_liked_articles(request):
    user = request.user
    liked_articles = Article.objects.filter(likes__user=user).order_by('-created_at')
    paginator = Paginator(liked_articles, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'resources/liked_articles.html', {'articles': articles})

@login_required
def view_popular_articles(request):
    popular_articles = Article.objects.annotate(
        total_interactions=Count('likes') + Count('comments')
    ).order_by('-like_count', '-comment_count')[:5]
    
    return render(request, 'resources/popular_articles.html', {'articles': popular_articles})

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.user = request.user
            media.save()
            return redirect('media_list', slug=media.slug)
    else:
        form = MediaForm()
    return render(request, 'resources/media_form.html', {'form': form})

# def media_detail(request, slug):
#     media = get_object_or_404(Media, slug=slug)
#     return render(request, 'resources/media_detail.html', {'media': media})


def download_media(request, slug):
    media = get_object_or_404(Media, slug=slug)
    media.increment_download_count()
    response = FileResponse(media.file.open(), as_attachment=True)
    return response

@login_required
def update_media(request, slug):
    media = get_object_or_404(Media, slug=slug)
    if request.user != media.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            return redirect('resources/mdeias.html', slug=media.slug)
    else:
        form = MediaForm(instance=media)
    return render(request, 'resources/media_form.html', {'form': form})

@login_required
def delete_media(request, slug):
    media = get_object_or_404(Media, slug=slug)
    if request.user != media.user:
        return HttpResponseForbidden()
    media.delete()
    return redirect('media_list')

def media_list(request):
    sort_option = request.GET.get('sort', 'recent')  # Default sorting option
    media_type = request.GET.get('type', 'image')  # Default media type
    search_query = request.GET.get('search', '')

    if sort_option == 'earliest':
        order_by = 'created_at'
    elif sort_option == 'most_downloaded':
        order_by = '-download_count'
    else:
        order_by = '-created_at'

    if media_type not in ['image', 'video', 'audio']:
        media_type = 'image'

    media = Media.objects.filter(
        media_type=media_type,
        title__icontains=search_query
    ).order_by(order_by)

    return render(request, 'resources/medias.html', {
        'media': media,
        'media_type': media_type,
        'sort_option': sort_option,
        'search_query': search_query
    })


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'resources/document_form.html', {'form': form})

@login_required
def update_document(request, slug):
    document = get_object_or_404(Document, slug=slug)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'resources/document_form.html', {'form': form})

@login_required
def delete_document(request, slug):
    document = get_object_or_404(Document, slug=slug)
    if request.method == 'POST':
        document.delete()
        return redirect('document_list')
    return render(request, 'resources/document_confirm_delete.html', {'document': document})

@login_required
def download_document(request, slug):
    document = get_object_or_404(Document, slug=slug)
    document.increment_download_count()
    return redirect(document.file.url)

def document_list(request):
    sort_option = request.GET.get('sort', 'latest')
    search_query = request.GET.get('search', '')

    if sort_option == 'earliest':
        order_by = 'uploaded_at'
    elif sort_option == 'most_downloaded':
        order_by = '-download_count'
    else:
        order_by = '-uploaded_at'

    documents = Document.objects.filter(title__icontains=search_query).order_by(order_by)

    paginator = Paginator(documents, 9)  # 9 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'resources/documents.html', {
        'documents': page_obj,
        'sort_option': sort_option,
        'search_query': search_query
    })