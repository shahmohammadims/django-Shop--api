from .models import Order
from rest_framework import serializers
from store.serializers import ProductSerializer



class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Order
        fields = ('product', 'number')

