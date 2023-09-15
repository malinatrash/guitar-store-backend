from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend_api.models import Wishlist, Product
import logging  # Импортируйте модуль logging

logger = logging.getLogger(__name__)  # Получите экземпляр логгера для текущего модуля

class WhishlistAPIView(APIView):
    def get(self, request):
        try:
            id = request.query_params.get('id')

            if not id:
                response_data = {
                    'message': 'id is required.',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            wishlists = Wishlist.objects.filter(user_id=id)

            products_data = []

            for wishlist in wishlists:
                product_id = wishlist.product_id_id
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

            response_data = {
                'products': products_data,
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

            response_data = {
                'message': 'An error occurred.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            product_id = request.data.get('product_id')

            if not user_id or not product_id:
                response_data = {
                    'message': 'Both user_id and product_id are required.',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            existing_wishlist = Wishlist.objects.filter(user_id=user_id, product_id=product_id).first()

            if existing_wishlist:
                # If the product already exists in the wishlist, remove it.
                existing_wishlist.delete()
                response_data = {
                    'message': 'Product removed from the wishlist.',
                    'status_code': status.HTTP_200_OK
                }
            else:
                # If the product doesn't exist in the wishlist, add it.
                Wishlist.objects.create(user_id_id=user_id, product_id_id=product_id)
                response_data = {
                    'message': 'Product added to the wishlist successfully.',
                    'status_code': status.HTTP_201_CREATED
                }

            return Response(response_data, status=response_data['status_code'])

        except Exception as e:
            response_data = {
                'message': 'An error occurred.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_data, status=response_data['status_code'])