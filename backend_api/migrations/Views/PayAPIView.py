from backend_api.models import Order
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class PayAPIView(APIView):

    def post(self, request):
        order_id = request.data.get('order_id')
        print(order_id)
        try:
            order = Order.objects.get(pk=order_id)
            order.order_status = 'закрыт'
            order.save()
            return Response({'message': 'Статус заказа успешно обновлен'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
