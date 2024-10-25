from rest_framework.viewsets import ViewSet
from diningapi.models import Wishlist, Dish
from rest_framework import  serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response


class WishlistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class WishlistDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['name', 'restaurant', 'user']

class WishlistSerializer(serializers.ModelSerializer):

    dish = WishlistDishSerializer(many=False)
    user = WishlistUserSerializer(many=False)

    class Meta: 
        model = Wishlist
        fields = ['dish', 'user']


class WishlistView(ViewSet):
    def create(self, request):
        wishlist = Wishlist()
        restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
        wishlist.restaurant = restaurant
        wishlist.user = request.user
        wishlist.save()

        serialized = WishlistSerializer(wishlist, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)