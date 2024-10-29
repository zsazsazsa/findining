from rest_framework.viewsets import ViewSet
from diningapi.models import RestaurantRating, Restaurant
from rest_framework import  serializers, status
from rest_framework.response import Response
from django.http import HttpResponseServerError
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
        fields = ['id', 'restaurant', 'rating', 'user']

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
    
    def list(self, request):
        # Get dish_id from the query parameters
        restaurant_id = request.query_params.get('restaurant_id', None)
        
        if restaurant_id is not None:
            reviews = RestaurantRating.objects.filter(restaurant_id=restaurant_id)
            if reviews.exists():
                serializer = RestaurantRatingSerializer(reviews, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No review found for this dish."}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
            # Start with all rows
                reviews = RestaurantRating.objects.all()

                serializer = RestaurantRatingSerializer(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as ex:
                return HttpResponseServerError(ex)
            
    def update(self, request, pk=None):
        restaurantRating = RestaurantRating.objects.get(pk=pk)
        restaurantRating.rating = request.data["rating"]
        restaurantRating.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)