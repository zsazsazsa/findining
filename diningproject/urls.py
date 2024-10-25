from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantView, 'restaurant')
router.register(r'categories', CategoryView, 'category')
router.register(r'dishes', DishView, 'dishes')
router.register(r'wishlist', WishlistView, 'wishlist')
router.register(r'restaurant-rating', RestaurantRatingView, 'restaurant-ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

