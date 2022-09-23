from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v3.serializers import ProductModelSerializer, OrderModelSerializer
from webapp.models import Product, Order


# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        elif self.request.user.is_staff:
            return [AllowAny]
        return super().get_permissions()


class OrderView(APIView):
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('pk'):
            order = Order.objects.get(id=self.kwargs.get('pk'))
            order_data = self.serializer_class(order).data
            return Response(order_data)
        else:
            orders = Order.objects.all()
            orders_data = self.serializer_class(orders, many=True).data
            return Response(orders_data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        elif self.request.user.is_staff:
            return [AllowAny]
        return super().get_permissions()
