from rest_framework import serializers

from webapp.models import Product, Order, OrderProduct


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id", )


class OrderProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ("product", "qty")
        read_only_fields = ("id", "order")


class OrderModelSerializer(serializers.ModelSerializer):
    order_products = OrderProductModelSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "products")
