from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    restaurant_id = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='restaurantWish')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)