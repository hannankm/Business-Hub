from django.shortcuts import render


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Group, Announcement, GroupArticle, Event, GroupArticleVote
from .forms import GroupForm, AnnouncementForm, EventForm, GroupArticleForm, GroupArticleUpdateForm
from django.utils.safestring import mark_safe

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            group.members.add(request.user)  # Automatically add owner to members
            return redirect('group_detail', slug=group.slug)
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form})

def view_groups(request):
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', 'popular')
    
    groups = Group.objects.exclude(Q(owner=request.user) | Q(members=request.user))
    
    if search_query:
        groups = groups.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if sort_option == 'earliest':
        groups = groups.order_by('created_at')
    elif sort_option == 'recent':
        groups = groups.order_by('-created_at')
    else:  # popular
        groups = groups.annotate(member_count=Count('members')).order_by('-member_count')

    paginator = Paginator(groups, 9)  # Show 9 groups per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'groups/groups.html', {'page_obj': page_obj, 'search_query': search_query, 'sort_option': sort_option})

@login_required
def my_groups(request):
    owned_groups = request.user.owned_groups.all()
    member_groups = request.user.member_groups.exclude(owner=request.user)
    return render(request, 'groups/my_groups.html', {'owned_groups': owned_groups, 'member_groups': member_groups})

@login_required
def update_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    if request.user != group.owner:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', slug=group.slug)
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/group_form.html', {'form': form})

@login_required
def delete_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    if request.user != group.owner:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        group.delete()
        return redirect('view_groups')
    return render(request, 'groups/group_confirm_delete.html', {'group': group})

def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    is_member = request.user in group.members.all()
    announcements = Announcement.objects.filter(group=group).order_by('-created_at')
    events = Event.objects.filter(group=group)
    members = group.members.all()
    authored_articles = request.user.coauthored_articles.all()
    owned_articles = request.user.owned_articles.all()
    articles = GroupArticle.objects.filter(group=group, post_status="approved")
    pending_articles = GroupArticle.objects.filter(group=group, post_status="pending")

    for article in pending_articles:
        article.approve_count = article.votes.filter(vote=True).count()
        article.reject_count = article.votes.filter(vote=False).count()
        article.user_voted = article.votes.filter(voter=request.user).exists()
        article.user_vote = article.votes.filter(voter=request.user).first().vote if article.user_voted else None


    return render(request, 'groups/group_detail.html', {'group': group, 'is_member': is_member, 'announcements': announcements, 'events': events, 'members': members, 'authored_articles': authored_articles, 'owned_articles': owned_articles, 'articles': articles, 'pending_articles': pending_articles})

@login_required
def join_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    group.members.add(request.user)
    return redirect('group_detail', slug=group.slug)

@login_required
def create_announcement(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user != group.owner:
        return redirect('group_detail', group_slug=group.slug)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.group = group
            announcement.save()
            return redirect('group_detail', group_slug=group.slug)
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/announcement_form.html', {'form': form, 'group': group})
@login_required
def vote_article(request, article_slug):
    article = get_object_or_404(GroupArticle, slug=article_slug)
    group = article.group

    if request.user not in group.members.all():
        return redirect('group_detail', group.slug)

    if request.method == 'POST':
        vote_value = request.POST.get('vote')
        vote = vote_value == 'yes'
        GroupArticleVote.objects.create(article=article, voter=request.user, vote=vote)
        article.update_status()
        return redirect('group_detail', group.slug)

    return render(request, 'groups/vote_article.html', {'article': article, 'group': group})

@login_required
def update_announcement(request, group_slug, pk):
    group = get_object_or_404(Group, slug=group_slug)
    announcement = get_object_or_404(Announcement, pk=pk, group=group)
    
    if request.user != group.owner:
        return redirect('group_detail', group_slug=group.slug)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_slug=group.slug)
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'announcements/announcement_form.html', {'form': form, 'group': group, 'announcement': announcement})

@login_required
def delete_announcement(request, group_slug, pk):
    group = get_object_or_404(Group, slug=group_slug)
    announcement = get_object_or_404(Announcement, pk=pk, group=group)
    
    if request.user == group.owner:
        announcement.delete()
    
    return redirect('group_detail', group_slug=group.slug)

def view_all_announcements(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    announcements = group.announcements.all()
    return render(request, 'announcements/announcement_list.html', {'group': group, 'announcements': announcements})

def view_announcement_detail(request, group_slug, pk):
    group = get_object_or_404(Group, slug=group_slug)
    announcement = get_object_or_404(Announcement, pk=pk, group=group)
    return render(request, 'announcements/announcement_detail.html', {'group': group, 'announcement': announcement})

@login_required
def event_list(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    events = Event.objects.filter(group=group)
    return render(request, 'groups/event_list.html', {'events': events})

@login_required
def event_detail(request, group_slug, event_slug):
    group = get_object_or_404(Group, slug=group_slug)
    event = get_object_or_404(Event, slug=event_slug, group=group)
    return render(request, 'groups/event_detail.html', {'event': event})

@login_required
def event_create(request, group_slug):
    
    group = get_object_or_404(Group, slug=group_slug)
    if request.user != group.owner:
        return redirect('group_detail', group_slug=group.slug)
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.group = group
            event.save()
            return redirect('group_detail', group_slug=group.slug)
    else:
        form = EventForm()
    return render(request, 'groups/event_form.html', {'form': form})

@login_required
def event_update(request, group_slug, event_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user != group.owner:
        return redirect('group_detail', group_slug=group.slug)
    
    event = get_object_or_404(Event, slug=event_slug, group=group)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', group_slug=group_slug, event_slug=event_slug)
    else:
        form = EventForm(instance=event)
    return render(request, 'groups/event_form.html', {'form': form})

@login_required
def event_delete(request, group_slug, event_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user != group.owner:
        return redirect('group_detail', group_slug=group.slug)
    
    event = get_object_or_404(Event, slug=event_slug, group=group)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'groups/event_delete.html', {'event': event})



@login_required
def create_article(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.method == 'POST':
        form = GroupArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.owner = request.user
            article.group = group
            article.status = 'pending'
            article.save()
            form.save_m2m()
            return redirect('view_group_article', article.slug)
    else:
        form = GroupArticleForm()
        form.fields['authors'].queryset = group.members.exclude(id=request.user.id)
    return render(request, 'groups/create_article.html', {'form': form, 'group': group})

@login_required
def update_article(request, article_slug):
    article = get_object_or_404(GroupArticle, slug=article_slug)
    if request.user != article.owner:
        # Co-authors can update only if the status is "pending"
        if request.user not in article.authors.all() or article.status != 'pending':
            return redirect('view_group_article', article.slug)
    if request.method == 'POST':
        form = GroupArticleUpdateForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('view_group_article', article.slug)
    else:
        form = GroupArticleUpdateForm(instance=article)
        form.fields['authors'].queryset = article.group.members.all()
    return render(request, 'groups/update_article.html', {'form': form, 'article': article})

@login_required
def publish_article(request, article_slug):
    article = get_object_or_404(GroupArticle, slug=article_slug)
    if request.user == article.owner:
        article.status = 'published'
        article.save()
    return redirect('view_group_article', article.slug)



@login_required
def view_group_article(request, article_slug):
    article = get_object_or_404(GroupArticle, slug=article_slug)
    article.content = mark_safe(article.content)  # Mark content as safe

    return render(request, 'groups/article_detail.html', {'article': article})

@login_required
def delete_article(request, article_slug):
    article = get_object_or_404(GroupArticle, slug=article_slug)
    if request.user == article.owner:
        article.delete()
    return redirect('group_detail')

@login_required
def view_all_articles(request):
    articles = GroupArticle.objects.filter(status='published', group__members=request.user)
    return render(request, 'articles/view_all_articles.html', {'articles': articles})

@login_required
def view_owned_articles(request):
    articles = request.user.owned_articles.all()
    return render(request, 'articles/view_owned_articles.html', {'articles': articles})

@login_required
def view_coauthored_articles(request):
    articles = request.user.coauthored_articles.all()
    return render(request, 'articles/view_coauthored_articles.html', {'articles': articles})