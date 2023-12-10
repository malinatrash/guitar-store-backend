
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from backend_api.models import Wishlist, Product, ShoppingCart
import logging

logger = logging.getLogger(__name__)


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
            print(str(e))
            # Обработка ошибок, если что-то идет не так
            response_data = {
                'message': 'An error occurred.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            if not user_id or not product_id:
                response_data = {
                    'message': 'Both user_id and product_id are required.',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.filter(product_id=product_id).first()
            if not product:
                response_data = {
                    'message': 'Product not found.',
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            if quantity < 0:
                raise ValidationError("Quantity should be a positive integer.")

            existing_cart_item = ShoppingCart.objects.filter(
                user_id=user_id, product_id=product_id).first()

            if existing_cart_item:
                existing_cart_item.delete()
                response_data = {
                    'message': 'Existing product removed from the shopping cart.',
                    'status_code': status.HTTP_200_OK
                }
            else:
                ShoppingCart.objects.create(
                    user_id_id=user_id, product_id_id=product_id, products_count=quantity)
                response_data = {
                    'message': 'Product added to the shopping cart successfully.',
                    'status_code': status.HTTP_201_CREATED
                }

            return Response(response_data, status=response_data['status_code'])

        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}")
            response_data = {
                'message': str(ve),
                'status_code': status.HTTP_400_BAD_REQUEST
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            response_data = {
                'message': 'An error occurred.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
