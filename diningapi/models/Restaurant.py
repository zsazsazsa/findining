from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='categories')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   