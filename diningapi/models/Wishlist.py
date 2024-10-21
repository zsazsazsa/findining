from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='restaurantWish')
    user = models.ForeignKey(User, on_delete=models.CASCADE)