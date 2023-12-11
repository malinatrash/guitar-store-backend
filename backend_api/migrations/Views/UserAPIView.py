from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_api.models import Session, User

import uuid


def generate_unique_session_id():
    return str(uuid.uuid4())


class UserAPIView(APIView):

    def create_session(self, user):
        session_id = generate_unique_session_id()
        Session.create_session(
            user=user, session_id=session_id)
        return session_id

    def get(self, request):
        try:
            email = request.query_params.get('email')
            password = request.query_params.get('password')

            if not email or not password:
                response_data = {
                    'message': 'Email and password are required.',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, email=email, password=password)

            session_id = self.create_session(user)

            user_data = {
                'user_id': user.user_id,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'role': user.role,
            }

            response_data = {
                'user': user_data,
                'session_id': session_id,
                'status_code': status.HTTP_200_OK
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            response_data = {
                'message': 'User not found.',
                'status_code': status.HTTP_404_NOT_FOUND
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                'message': str(e),
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if request.data['firstname'] != '' and request.data['lastname'] != '' and request.data['email'] != '' and \
                    request.data['password'] != '':
                new_user = User.objects.create(
                    first_name=request.data['firstname'],
                    last_name=request.data['lastname'],
                    email=request.data['email'],
                    password=request.data['password'],
                    role='client'
                )

                session_id = self.create_session(new_user)

                user_data = {
                    'id': new_user.user_id,
                    'firstname': new_user.first_name,
                    'lastname': new_user.last_name,
                    'email': new_user.email,
                    'role': new_user.role,
                }

                response_data = {
                    'user': user_data,
                    'session_id': session_id,
                    'message': 'User created successfully',
                    'status_code': status.HTTP_201_CREATED
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'message': 'filed is empty',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'message': str(e),
                'status_code': status.HTTP_400_BAD_REQUEST
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
