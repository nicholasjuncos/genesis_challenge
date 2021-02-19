from django.contrib.auth import get_user_model

from rest_framework import status, filters, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'first_name', 'last_name', ]
    search_fields = ['username', 'email', 'first_name', 'last_name', ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # allow superusers to see all users
        if self.request.user.is_superuser:
            return self.queryset
        # by default only show users themselves, alter this filter to allow users to see others
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
