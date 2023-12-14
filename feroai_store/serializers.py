from django.utils import timezone
from rest_framework import serializers

from feroai_store.constants import CUSTOMER_NAME_ALREADY_EXISTS, PRODUCT_NAME_ALREADY_EXISTS, NO_NEGATIVE_WEIGHT, \
    PRODUCT_MAX_WEIGHT, ORDER_MAX_WEIGHT, NO_PAST_ORDER_DATE, ORDER_ITEM_NOT_FOUND, PROVIDE_ORDER_ITEM_ID
from feroai_store.models import Customer, Product, OrderItem, Order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    @staticmethod
    def validate_name(value):

        existing_customer = Customer.objects.filter(name=value).first()
        if existing_customer:
            raise serializers.ValidationError(CUSTOMER_NAME_ALREADY_EXISTS)
        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def validate_name(value):

        existing_product = Product.objects.filter(name=value).first()
        if existing_product:
            raise serializers.ValidationError(PRODUCT_NAME_ALREADY_EXISTS)
        return value

    @staticmethod
    def validate_weight(value):

        if value <= 0:
            raise serializers.ValidationError(NO_NEGATIVE_WEIGHT)
        elif value > 25:
            raise serializers.ValidationError(PRODUCT_MAX_WEIGHT)
        return value


class OrderItemDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_weight = 0

    def validate(self, data):
        product_obj = Product.objects.get(pk=data.get('product').id)
        self.max_weight += (product_obj.weight * data.get('quantity'))

        if self.max_weight > 150:
            raise serializers.ValidationError(ORDER_MAX_WEIGHT)

        return data


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'address', 'order_items']

    @staticmethod
    def validate_order_date(value):
        if value < timezone.now().date():
            raise serializers.ValidationError(NO_PAST_ORDER_DATE)
        return value

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')

        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def to_representation(self, instance):
        rep = super(OrderSerializer, self).to_representation(instance)
        rep['order_items'] = OrderItemDetailSerializer(instance.order_item_order, many=True).data
        return rep


class OrderUpdateSerializer(serializers.ModelSerializer):
    order_items = OrderItemDetailSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'address', 'order_items']

    @staticmethod
    def validate_order_date(value):
        if value < timezone.now().date():
            raise serializers.ValidationError(NO_PAST_ORDER_DATE)
        return value

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')

        for item_data in order_items_data:
            if not item_data.get('id'):
                raise serializers.ValidationError(PROVIDE_ORDER_ITEM_ID)
            order_item_instance = OrderItem.objects.filter(pk=item_data.get('id')).first()
            if not order_item_instance:
                raise serializers.ValidationError(ORDER_ITEM_NOT_FOUND)

            order_item_instance.product = item_data.get('product')
            order_item_instance.quantity = item_data.get('quantity')
            order_item_instance.save()

        return validated_data
