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