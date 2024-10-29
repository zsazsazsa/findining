from rest_framework.viewsets import ViewSet
from diningapi.models import RestaurantReview, Restaurant
from rest_framework import  serializers, status
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.contrib.auth.models import User


class RestaurantReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RestaurantReviewRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'category', 'user']

class RestaurantReviewSerializer(serializers.ModelSerializer):

    restaurant = RestaurantReviewRestaurantSerializer(many=False)
    user = RestaurantReviewUserSerializer(many=False)

    class Meta:
        model = RestaurantReview
        fields = ['id', 'restaurant', 'review', 'user']

class RestaurantReviewView(ViewSet):

    def create(self, request):
        review = RestaurantReview()
        restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
        review.restaurant = restaurant
        review.review = request.data['review']
        review.user = request.user
        review.save()

        serialized = RestaurantReviewSerializer(review, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
        
        
    def list(self, request):
        # Get dish_id from the query parameters
        restaurant_id = request.query_params.get('restaurant_id', None)
        
        if restaurant_id is not None:
            reviews = RestaurantReview.objects.filter(restaurant_id=restaurant_id)
            if reviews.exists():
                serializer = RestaurantReviewSerializer(reviews, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No review found for this dish."}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
            # Start with all rows
                reviews = RestaurantReview.objects.all()

                serializer = RestaurantReviewSerializer(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as ex:
                return HttpResponseServerError(ex)
            
    def update(self, request, pk=None):
        restaurantReview = RestaurantReview.objects.get(pk=pk)
        restaurantReview.review = request.data["review"]
        restaurantReview.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)