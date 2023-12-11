from datetime import datetime, timezone
from rest_framework import serializers
from .models import OrderProduct, User, Order, Product, ProductCategory, ProductComment, ShoppingCart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'role')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'order_id',
            'order_date',
            'order_status',
            'total_price',
            'product_id_id',
            'user_id_id'
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'product_id',
            'product_name',
            'product_description',
            'price', 'in_stock',
            'vendor',
            'country_of_origin',
            'year_of_production',
            'image_url',
            'category_id_id'
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            'category_id',
            'category_name'
        )


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = (
            'comment_id',
            'comment_text',
            'likes_count',
            'comment_date',
            'product_id',
            'user_id'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'cart_id',
            'products_count',
            'product_id_id',
            'user_id_id'
        )


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'wishlist_id',
            'product_id_id',
            'user_id_id'
        )


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Product
        fields = '__all__'  # Если нужно включить все поля модели Product


class OrderProductSerializer(serializers.ModelSerializer):
    # Используем ProductSerializer для связанной модели Product
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']  # Указываем поля для сериализации


class DateOnlyField(serializers.Field):
    def to_representation(self, value):
        if value is not None and isinstance(value, datetime):
            return value.astimezone(timezone.utc).date() if value.tzinfo else value.date()
        return value


class OrderSerializer(serializers.ModelSerializer):
    order_date = DateOnlyField()
    order_products = OrderProductSerializer(
        source='orderproduct_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_date', 'order_status',
                  'total_price', 'order_products']
        # Эти поля только для чтения
        read_only_fields = ['order_id', 'order_date',
                            'total_price', 'order_products']
        extra_kwargs = {
            # Ограничиваем выбор только двумя статусами
            'order_status': {'choices': Order.ORDER_STATUS_CHOICES},
        }
