from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend_api.models import CountryOfOrigin
import logging  # Импортируйте модуль logging


class CountryAPIView(APIView):
    def get(self, request):
        response = CountryOfOrigin.objects.all()
        response_data = []
        for i in response:
            response_data.append({'id': i.country_id, 'name': i.name})
        return Response(response_data, status=status.HTTP_200_OK)
