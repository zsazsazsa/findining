from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import  serializers, status
from diningapi.models import Restaurant, Category
from django.contrib.auth.models import User


class RestaurantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'type']


class RestaurantSerializer(serializers.ModelSerializer):

    category = RestaurantCategorySerializer(many=False)
    user = RestaurantUserSerializer(many=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'location', 'category', 'user')


class RestaurantView(ViewSet): 
    def list(self, request):

        try:
            # Start with all rows
            restaurants = Restaurant.objects.all()

            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        restaurant = Restaurant()
        restaurant.name = request.data['name']
        restaurant.location = request.data['location']
        category = Category.objects.get(pk=request.data['category'])
        restaurant.category = category
        restaurant.user = request.user
        restaurant.save()

        serialized = RestaurantSerializer(restaurant, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)