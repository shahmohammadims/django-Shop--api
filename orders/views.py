from orders.models import Order
from store.models import Product
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from store.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView



class CartAddView(APIView):
    def get(self, request, product_id):
        global product
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


    def post(self, request, product_id):
        user = request.user
        order = request.data
        if not Order.objects.filter(user=user, product=product).exists():
            Order.objects.create(
                user = user,
                product = product,
                number = order['number']
            )
        else:
            new_order = Order.objects.get(user=user, product=product)
            new_order.number += order['number']
            new_order.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CartRemoveView(APIView):
    def get(self, request, order_id, count):
        order = Order.objects.get(id=order_id)
        product = order.product
        if order != None and request.user == order.user:
            if order.number == 1 or count == 'all':
                order.delete()
            elif count == 'one':
                order.number -= 1
                order.save()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class MyCard(ListAPIView):
    model = Order
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

