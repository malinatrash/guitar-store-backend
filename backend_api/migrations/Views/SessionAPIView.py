from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend_api.models import Session, User
import uuid


def generate_unique_session_id():
    return str(uuid.uuid4())


class SessionAPIView(APIView):
    def get(self, request):
        try:
            session_id = request.query_params.get('session_id')
            session = Session.get_session(session_id)

            if session and not session.is_expired():
                user = session.user
                user_data = {
                    'user_id': user.user_id,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'email': user.email,
                    'role': user.role,
                }
                return Response({"user": user_data, "status_code": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Сессия истекла", "status_code": 404}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': "Сессия истекла", "status_code": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
