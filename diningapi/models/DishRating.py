from django.db import models
from django.contrib.auth.models import User

class DishRating(models.Model):
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, related_name='dishRating')
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)