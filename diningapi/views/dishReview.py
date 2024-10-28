from rest_framework.viewsets import ViewSet
from diningapi.models import DishReview, Dish
from rest_framework.response import Response
from rest_framework import  serializers, status

class DishReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishReview()
        fields = ['id', 'dish', 'user', 'review']

class DishReviewView(ViewSet):

    def create(self, request):
        rating = DishReview()
        dish = Dish.objects.get(pk=request.data['dish'])
        rating.dish = dish
        rating.review = request.data['review']
        rating.user = request.user
        rating.save()

        serialized = DishReviewSerializer(rating, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        # Get dish_id from the query parameters
        dish_id = request.query_params.get('dish_id', None)
        
        if dish_id is not None:
            ratings = DishReview.objects.filter(dish_id=dish_id)
            if ratings.exists():
                serializer = DishReviewSerializer(ratings, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No review found for this dish."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "dish_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        dishReview = DishReview.objects.get(pk=pk)
        dishReview.review = request.data["review"]
        dishReview.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)