from django.db import models
from django.contrib.auth.models import User

class DishReview(models.Model):
    dish_id = models.ForeignKey("Dish", on_delete=models.CASCADE, related_name='dishReview')
    review = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)