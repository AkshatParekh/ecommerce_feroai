from rest_framework import generics, status
from rest_framework.response import Response

from .constants import CUSTOMER_CREATED, CUSTOMER_UPDATED, PRODUCT_CREATED, ORDER_PLACED, ORDER_UPDATED
from .models import Customer, Product, Order
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderUpdateSerializer


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": CUSTOMER_CREATED,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class CustomerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": CUSTOMER_UPDATED
        }
        return Response(data=data, status=status.HTTP_200_OK)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": PRODUCT_CREATED,
            "data": serializer.data
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')

        products_param = self.request.query_params.get('products')
        if products_param:
            products = products_param.split(',')
            queryset = queryset.filter(order_item_order__product__name__in=products)

        customer_param = self.request.query_params.get('customer')
        if customer_param:
            queryset = queryset.filter(order_customer__name=customer_param)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": ORDER_PLACED
        }
        return Response(data=data)


class RetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": ORDER_UPDATED,
        }
        return Response(data=data, status=status.HTTP_200_OK)
