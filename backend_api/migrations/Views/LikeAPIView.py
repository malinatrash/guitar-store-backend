from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from backend_api.models import ProductComment


class LikeAPIView(APIView):

    def post(self, request, comment_id):
        comment = get_object_or_404(ProductComment, comment_id=comment_id)
        action = request.data.get('action')

        if action not in ['like', 'unlike']:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'like':
            comment.likes_count += 1
        elif action == 'unlike':
            if comment.likes_count > 0:
                comment.likes_count -= 1
            else:
                return Response({'error': 'Cannot unlike a comment with zero likes'}, status=status.HTTP_400_BAD_REQUEST)

        print(comment.comment_id)
        comment.save()
        return Response({'likes_count': comment.likes_count}, status=status.HTTP_200_OK)
