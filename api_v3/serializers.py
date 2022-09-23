from rest_framework import serializers

from webapp.models import Product


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id", )
