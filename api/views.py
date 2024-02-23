from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app.models import Comment, User
from .serializers import CommentSerializer, UserSerializer, UserCreateSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        sort_by = self.request.query_params.get('sort_by')
        allowed_names = {
            'user_id': 'user_name',
            'email': 'user_name__email',
            '-user_id': '-user_name',
            '-email': '-user_name__email',

        }
        if sort_by:
            if sort_by in allowed_names:
                sort_by = allowed_names[sort_by]
        allowed_fields = ['user_name', 'user_name__email', 'created_date', '-user_name', '-user_name__email',
                          '-created_date']

        if sort_by not in allowed_fields:
            sort_by = '-created_date'

        queryset = Comment.objects.filter(parent_comment__isnull=True)

        queryset = queryset.order_by(sort_by)

        return queryset


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_superuser(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            return Response({'message': 'Superuser created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
