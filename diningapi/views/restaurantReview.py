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
        fields = ['restaurant', 'review', 'user']

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

        try:
            # Start with all rows
            reviews = RestaurantReview.objects.all()

            serializer = RestaurantReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)