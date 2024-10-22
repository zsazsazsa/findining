from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from diningapi.views import register_user, login_user, RestaurantView
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantView, 'restaurant')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

