from django.db.models import Q
from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'post', 'author__username', 'language', ]
    search_fields = ['title', 'post', 'author__username', 'language', ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        # allow superusers to see all articles
        if self.request.user.is_superuser:
            return self.queryset
        # by default only show articles by users themselves and any published articles
        if not self.request.user.is_authenticated:
            return self.queryset.filter(status='Published')
        return self.queryset.filter(Q(author_id=self.request.user.id) | Q(status='Published'))
