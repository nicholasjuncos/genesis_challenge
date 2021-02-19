from django.db.models import Q
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article
from .permissions import IsAuthorOrReadOnly
from .serializers import ArticleSerializer, AdminArticleSerializer


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'post', 'author__username', 'language', ]
    search_fields = ['title', 'post', 'author__username', ]
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminArticleSerializer
        return self.serializer_class

    def get_queryset(self, *args, **kwargs):
        # allow superusers to see all articles
        if self.request.user.is_superuser:
            return self.queryset
        # by default only show articles by users themselves and any published articles
        if not self.request.user.is_authenticated:
            return self.queryset.filter(status='Published')
        # getting language from url arguments. If none, then queryset is based on preferred language
        language = self.request.GET.get('language')
        if language:
            return self.queryset.filter(Q(author_id=self.request.user.id) | Q(status='Published'))
        return self.queryset.filter(Q(author_id=self.request.user.id) |
                                    Q(status='Published', language=self.request.user.preferred_language))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # below detects if a language is filtered. If not, and the queryset is empty, returns a message
        language = self.request.GET.get('language')
        if not language:
            message = 'There are no articles for your preferred language! Please add a filter for another language to' \
                      ' possibly view other articles.'
        else:
            message = 'There are no articles! Please add/edit language filter to possibly view other articles.'
        if not any(serializer.data):
            headers = self.get_success_headers(serializer.data)
            return Response({'Message': message}, status=status.HTTP_204_NO_CONTENT, headers=headers)
        return Response(serializer.data)
