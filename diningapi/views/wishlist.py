from rest_framework.viewsets import ViewSet
from diningapi.models import Wishlist, Dish
from rest_framework import  serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponseServerError


class WishlistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class WishlistDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'restaurant', 'user']

class WishlistSerializer(serializers.ModelSerializer):

    dish = WishlistDishSerializer(many=False)
    user = WishlistUserSerializer(many=False)

    class Meta: 
        model = Wishlist
        fields = ['id', 'dish', 'user']


class WishlistView(ViewSet):
    def create(self, request):
        wishlist = Wishlist()
        dish = Dish.objects.get(pk=request.data['dish'])
        wishlist.dish = dish
        wishlist.user = request.user
        wishlist.save()

        serialized = WishlistSerializer(wishlist, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):

        try:
            # Start with all rows
            wishlist = Wishlist.objects.all()

            serializer = WishlistSerializer(wishlist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)