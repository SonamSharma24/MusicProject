from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class Song(models.Model):
    song_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length= 2000)
    singer = models.CharField(max_length= 2000)
    image = models.ImageField()
    song = models.FileField()
    movie = models.CharField(max_length = 150, default = "None")


    def __str__(self):
        return self.name


