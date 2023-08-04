from django.db import models
from django.contrib.auth.models import User



class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)