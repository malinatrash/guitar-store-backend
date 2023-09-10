from rest_framework import serializers
from .models import User, Order, Product, ProductCategory, ProductComment, ShoppingCart


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
            'product_id_id',
            'user_id_id'
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
