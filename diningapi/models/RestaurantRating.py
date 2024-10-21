from django.db import models
from django.contrib.auth.models import User

class RestaurantRating(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='restaurantRating')
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)