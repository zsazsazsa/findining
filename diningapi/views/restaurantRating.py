from rest_framework.viewsets import ViewSet
from diningapi.models import RestaurantRating, Restaurant
from rest_framework import  serializers, status
from rest_framework.response import Response

from django.contrib.auth.models import User


class RestaurantRatingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RestaurantRatingRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'category', 'user']

class RestaurantRatingSerializer(serializers.ModelSerializer):

    restaurant = RestaurantRatingRestaurantSerializer(many=False)
    user = RestaurantRatingUserSerializer(many=False)

    class Meta:
        model = RestaurantRating
        fields = ['restaurant', 'rating', 'user']

class RestaurantRatingView(ViewSet):

    def create(self, request):
        rating = RestaurantRating()
        restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
        rating.restaurant = restaurant
        rating.rating = request.data['rating']
        rating.user = request.user
        rating.save()

        serialized = RestaurantRatingSerializer(rating, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)