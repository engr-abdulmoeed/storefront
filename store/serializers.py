from decimal import Decimal
from rest_framework import serializers
from store.models import Cart, Product, Collection, Review, CartItem


class CollectionSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'unit_price',
                  'price_with_tax', 'inventory', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product) -> Decimal:
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data) -> Review:
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='calculate_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def calculate_total_price(self, cart_item: CartItem) -> Decimal:
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(
        method_name='calculate_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def calculate_total_price(self, cart: Cart) -> Decimal:
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
