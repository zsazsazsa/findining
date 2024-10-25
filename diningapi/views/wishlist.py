from rest_framework.viewsets import ViewSet
from diningapi.models import Wishlist, Restaurant
from rest_framework import  serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response


class WishlistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class WishlistRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'category', 'user']

class WishlistSerializer(serializers.ModelSerializer):

    restaurant = WishlistRestaurantSerializer(many=False)
    user = WishlistUserSerializer(many=False)

    class Meta: 
        model = Wishlist
        fields = ['restaurant', 'user']


class WishlistView(ViewSet):
    def create(self, request):
        wishlist = Wishlist()
        restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
        wishlist.restaurant = restaurant
        wishlist.user = request.user
        wishlist.save()

        serialized = WishlistSerializer(wishlist, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)