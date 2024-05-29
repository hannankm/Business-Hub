from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(User, related_name='member_groups')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo = models.ImageField(upload_to='group_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Announcement(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Event(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GroupArticle(models.Model):
    ARTICLE_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    LESSONS_LEARNED = 'lessons_learned'
    BEST_PRACTICES = 'best_practices'
    OTHER = 'other'

    TYPE_CHOICES = [
        (LESSONS_LEARNED, 'Lessons Learned'),
        (BEST_PRACTICES, 'Best Practices'),
        (OTHER, 'Other'),
    ]


    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_articles')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='articles')
    authors = models.ManyToManyField(User, null=True, blank=True, related_name='coauthored_articles')
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=ARTICLE_STATUS_CHOICES, default='draft')
    # pending, approved, rejected
    post_status = models.CharField(max_length=20, default="pending")
    invitation_note = models.TextField(blank=True, null=True)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    

    def update_status(self):
        if self.votes.filter(vote=True).count() >= 2:
            self.post_status = 'approved'
            self.save()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    
class GroupArticleVote(models.Model):
    article = models.ForeignKey(GroupArticle, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField()

# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Notification for {self.user.username} - {self.message[:20]}'

# group
# events
# announcements
# joint articles -> add as a coauthor by username then if co-author allow updates in 
# best practices 
# lessons learnt -> or as an article but include type = best practice, lessons learnt, other -- include co -authors - ascoiated with a group
# meeting view, members view


# group articles -> title, owner, authors, type, content, date_created, visbility (group, everryone), status (pending, published), invitation description
# publish if content is not empty and if requester is owner 
# co authors can add content if status is pending, 
# create artcile with pending status content can be empty on create

# when displaying articles 
# notification when added as a co author, membership approved/ rejected
# tabs -> members (view), announcements (CRUD), calendar(CRUD), about, meeting, articles(crud) 

# joint articles -> add as a coauthor by username then if co-author allow updates in 
# an article but include type = best practice, lessons learnt, other -- include co -authors - ascoiated with a group
# co authors can add content if status is pending, 
# publish if content is not empty and if requester is owner 
# create artcile with pending status content can be empty on create
# when displaying articles list co authors 




# document -> 

# joint articles 


# members excpet for themselves 