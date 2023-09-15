from django.forms import model_to_dict
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Order, Product, ProductCategory, ProductComment, ShoppingCart, Wishlist
from .serializers import UserSerializer, OrderSerializer, ProductSerializer, ProductCategorySerializer, \
    ShoppingCartSerializer, ProductCommentSerializer, WishlistSerializer

class OrderAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductCommentAPIView(generics.ListAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer


# class ShoppingCartAPIView(generics.ListAPIView):
#     queryset = ShoppingCart.objects.all()
#     serializer_class = ShoppingCartSerializer


# class WishlistAPIView(generics.ListAPIView):
#     queryset = Wishlist.objects.all()
#     serializer_class = WishlistSerializer

