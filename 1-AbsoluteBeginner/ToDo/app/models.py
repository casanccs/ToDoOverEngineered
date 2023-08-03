from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)