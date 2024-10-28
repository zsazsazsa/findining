from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, related_name='dishWish')
    user = models.ForeignKey(User, on_delete=models.CASCADE)