from datetime import date
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
        comment_data = request.data
        user_id = comment_data.get('user_id')
        print(user_id)
        product_id = comment_data.get('product_id')
        print(product_id)
        comment_text = comment_data.get('comment_text')

        user = User.objects.get(pk=user_id)
        product = Product.objects.get(pk=product_id)

        comment_date = date.today()

        comment = ProductComment(
            comment_id=-1,
            user_id_id=user,
            product_id_id=product,
            comment_text=comment_text,
            comment_date=comment_date
        )

        print(comment.__dict__)

        serializer = ProductCommentSerializer(data=comment.__dict__)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
