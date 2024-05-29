from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    text_content = models.TextField(null=True, blank=True)
    file_content = models.FileField(upload_to='content_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, through='PostLike', related_name='liked_posts')
    status = models.CharField(max_length=20, default='pending')
    def __str__(self):
        return f"{self.title} | {self.posted_by.username}"

    def is_text(self):
        return self.text_content is not None

    def is_file(self):
        return self.file_content is not None

class PostLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class PostShare(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

class PostComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

