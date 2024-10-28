from django.db import models
from django.contrib.auth.models import User

class DishReview(models.Model):
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, related_name='dishReview')
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)