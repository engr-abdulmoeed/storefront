from decimal import Decimal

from rest_framework import serializers

from store.models import Cart, CartItem, Collection, Product, Review


class CollectionSerializer(serializers.ModelSerializer):
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

    @staticmethod
    def calculate_tax(product: Product) -> Decimal:
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

    @staticmethod
    def calculate_total_price(cart_item: CartItem) -> Decimal:
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='calculate_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    @staticmethod
    def calculate_total_price(cart: Cart) -> Decimal:
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    @staticmethod
    def validate_product_id(value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        else:
            return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)

            cart_item.quantity += quantity
            cart_item.save()

            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
