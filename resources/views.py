from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Like
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
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