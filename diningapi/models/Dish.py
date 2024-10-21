from django.db import models
from django.contrib.auth.models import User


class Dish(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='dishes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)