from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from api_v3.serializers import ProductModelSerializer
from webapp.models import Product


# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
