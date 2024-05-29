from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
# Create your models here.

# tags are added by admin - can be none to 3, search then pick in checkbox manner

# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

class Question(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=150)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)
    # tags = models.ManyToManyField(Tag, related_name='questions')

    def __str__(self):
        return self.title

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="responses")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.content

class Vote(models.Model):
    # 1 up 2 down
    type = models.BooleanField(default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

    def __str__(self):
        return self.type