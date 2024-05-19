from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.TextField(null=True, blank=True)
    file_content = models.FileField(upload_to='content_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
 
    def __str__(self):
        return self.title + ' | ' + self.posted_by
    def is_text(self):
        return self.text_content is not None

    def is_file(self):
        return self.file_content is not None

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name='following')
    following = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return f'Profile of {self.user.username}'
