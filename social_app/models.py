from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

from django.contrib.auth import get_user_model

User = get_user_model()

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()  
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to="profile_images", default="placeholder.jpg")
    interest = models.ManyToManyField(Interest)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post_img=models.ImageField(upload_to="Posts_images")
    caption=models.TextField()
    no_of_likes=models.IntegerField(default=0)
    created_at=models.DateField(default=datetime.now())

    def __str__(self):
        return str(self.id)

class LikeModel(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=500)

    def __str__(self):
        return f"{self.username} -> {self.username}"
    
class Followers_Model(models.Model):
    user=models.CharField(max_length=500)
    follower=models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.follower}"