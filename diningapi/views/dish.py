from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import  serializers, status
from diningapi.models import Dish, Restaurant, Category
from django.contrib.auth.models import User

class DishUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DishRestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'type']

class DishRestaurantSerializer(serializers.ModelSerializer):

    category = DishRestaurantCategorySerializer(many=False)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'category']



class DishSerializer(serializers.ModelSerializer):

    user = DishUserSerializer(many=False)
    restaurant = DishRestaurantSerializer(many=False)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'user', 'restaurant')


class DishView(ViewSet): 
    def list(self, request):

        try:
            # Start with all rows
            dishes = Dish.objects.all()

            serializer = DishSerializer(dishes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        dish = Dish()
        dish.name = request.data['name']
        restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
        dish.restaurant = restaurant
        dish.user = request.user
        dish.save()

        serialized = DishSerializer(dish, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
       
        try:
            dish = Dish.objects.get(pk=pk)
            dish.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Dish.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)