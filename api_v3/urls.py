from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api_v3.views import ProductViewSet

app_name = 'api_v3'

router = DefaultRouter()
router.register("products", ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
