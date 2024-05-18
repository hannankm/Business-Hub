from django.db import models
from django.contrib.auth.models import AbstractUser

class Industry(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    # automobile, delivery, 


class Photo(models.Model):
    image = models.ImageField(upload_to='profiles')

# Create your models here.
class CustomUser(AbstractUser):
    is_org = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=18, blank=True, null=True)
    profile_pic = models.OneToOneField(Photo, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(max_length=250, blank=True, null=True)
    headline = models.CharField(max_length=50, blank=True, null=True)
    post_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)



    class Meta:
        verbose_name = "Users"

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    industry_iterests = models.ManyToManyField(Industry, related_name="users")
    # managing director 
    position = models.CharField(max_length=70,blank=True, null=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    # phd, masters, 
    education_level = models.CharField(max_length=50, blank=True, null=True)
    # agriculture, business, construction
    education_field = models.CharField(max_length=50, blank=True, null=True)
    # entry level,intermediate, mid level, senior, expert 
    experience_level = models.CharField(max_length=20, blank=True,  null=True)
    # company you are hired at or your business 
    company = models.CharField(max_length=60, blank=True,  null=True)


class Organization_Details(models.Model):
    organization = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=18, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name="orgs", null=True)
    # year started ``
    start_date = models.DateField(blank=True, null=True)
    # location = models.CharField(max)
    is_verified = models.BooleanField(default=False)



class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower} follows {self.followed}'


# custom user
# profile
# org details


# models -- views -- urls -- forms -- templates 