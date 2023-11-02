from backend_api.models import ProductComment, User, Product
# Import the ProductSerializer
from backend_api.serializers import UserSerializer, ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
