from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend_api.models import Wishlist, Product, Vendor
import logging  # Импортируйте модуль logging


class VendorAPIView(APIView):
    def get(self, request):
        response = Vendor.objects.all()
        response_data = []
        for i in response:
            response_data.append({'id': i.vendor_id, 'name': i.name})
        return Response(response_data, status=status.HTTP_200_OK)

