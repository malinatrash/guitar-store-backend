from xml.dom import ValidationErr
from backend_api.models import ProductComment, User, Product
from backend_api.serializers import ProductCommentSerializer, UserSerializer, ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class CommentsAPIView(APIView):
    def get(self, request):
        req = request.query_params.get('product_id')
        if req is not None:
            comments = ProductComment.objects.filter(product_id_id=req)
            response_data = []

            for comment in comments:
                user_serializer = UserSerializer(
                    comment.user_id)
                user_data = user_serializer.data
                response_data.append({
                    'id': comment.comment_id,
                    'user_name': f"{user_data['first_name']} {user_data['last_name']}",
                    'product_id': comment.product_id_id,
                    'comment_text': comment.comment_text,
                    'likes_count': comment.likes_count,
                    'comment_date': comment.comment_date
                })

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Product ID is required in query parameters'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ProductCommentSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            product_id = serializer.validated_data.get('product_id')

            user_exists = User.objects.filter(pk=user_id).exists()
            product_exists = Product.objects.filter(pk=product_id).exists()

            if user_exists and product_exists:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationErr("User or Product does not exist")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
