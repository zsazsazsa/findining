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
    
    def list(self, request):
        # Get dish_id from the query parameters
        dish_id = request.query_params.get('dish_id', None)
        
        if dish_id is not None:
            ratings = DishRating.objects.filter(dish_id=dish_id)
            if ratings.exists():
                serializer = DishRatingSerializer(ratings, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No ratings found for this dish."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "dish_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        dishRating = DishRating.objects.get(pk=pk)
        dishRating.rating = request.data["rating"]
        dishRating.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)