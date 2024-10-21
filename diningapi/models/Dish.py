from django.db import models
from django.contrib.auth.models import User


class Dish(models.Model):
    name = models.CharField(max_length=255)
    restaurant_id = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='restaurants')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)