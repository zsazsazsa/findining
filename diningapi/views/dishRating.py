from rest_framework.viewsets import ViewSet
from diningapi.models import DishRating, Dish
from rest_framework.response import Response
from rest_framework import  serializers, status

class DishRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishRating
        fields = ['id', 'dish', 'user', 'rating']

class DishRatingView(ViewSet):

    def create(self, request):
        rating = DishRating()
        dish = Dish.objects.get(pk=request.data['dish'])
        rating.dish = dish
        rating.rating = request.data['rating']
        rating.user = request.user
        rating.save()

        serialized = DishRatingSerializer(rating, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)