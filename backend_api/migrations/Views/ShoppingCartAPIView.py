from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend_api.models import Wishlist, Product, ShoppingCart
import logging  # Импортируйте модуль logging

logger = logging.getLogger(__name__)  # Получите экземпляр логгера для текущего модуля

class ShoppingCartAPIView(APIView):
    def get(self, request):
        try:
            id = request.query_params.get('id')

            if not id:
                response_data = {
                    'message': 'id is required.',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            carts = ShoppingCart.objects.filter(user_id=id)

            products_data = []

            for cart in carts:
                product_id = cart.product_id_id
                product = Product.objects.get(product_id=product_id)
                product_data = {
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'product_description': product.product_description,
                    'price': product.price,
                    'in_stock': product.in_stock,
                    'vendor': product.vendor.name,
                    'country_of_origin': product.country_of_origin.name,
                    'year_of_production': product.year_of_production,
                    'image_url': product.image_url,
                }
                products_data.append(product_data)

            # Возвращение данных о товарах в ответе
            response_data = {
                'products': products_data,
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Логирование информации об ошибке
            logger.error(f"An error occurred: {str(e)}")

            # Обработка ошибок, если что-то идет не так
            response_data = {
                'message': 'An error occurred.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
