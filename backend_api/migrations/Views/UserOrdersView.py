from datetime import datetime
from decimal import Decimal
from backend_api.models import Order, OrderProduct, ShoppingCart, User, Product
from backend_api.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers


class UserOrdersView(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({"message": "Параметр user_id отсутствует"}, status=400)
        orders = Order.objects.filter(user_id=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user_id')
        products_data = request.data.get('products', [])

        if not user_id or not products_data:
            return Response({"message": "Отсутствуют данные для создания заказа"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        total_price = Decimal('0.00')

        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')
            product = Product.objects.get(pk=product_id)
            total_price += product.price * quantity

        new_order = Order.objects.create(
            user_id=User.objects.get(pk=user_id),
            order_status='открыт',
            total_price=total_price
        )

        # Связываем продукты с заказом, используя экземпляры OrderProduct
        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')
            product = Product.objects.get(pk=product_id)

            OrderProduct.objects.create(
                order=new_order,
                product=product,
                quantity=quantity
            )

        # Удаление товаров из корзины пользователя
        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')
            # Удалите товар из корзины пользователя, используя ваш метод удаления или логику
            # Например:
            try:
                cart_item = ShoppingCart.objects.get(
                    user_id=user_id, product_id=product_id)
                if cart_item.products_count <= quantity:
                    cart_item.delete()
                else:
                    cart_item.products_count -= quantity
                    cart_item.save()
            except ShoppingCart.DoesNotExist:
                pass  # Обработайте ситуацию, если товар не найден в корзине пользователя

        serializer = OrderSerializer(new_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
