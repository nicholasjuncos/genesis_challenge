from rest_framework import serializers

from .models import Article
from ..common import PREFERRED_LANGUAGE_CHOICES


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    language = serializers.ChoiceField(choices=PREFERRED_LANGUAGE_CHOICES, source='get_language_display')

    class Meta:
        model = Article
        fields = ['status', 'author', 'title', 'post', 'language', 'publication_date', 'url']
        read_only_fields = ('author', 'publication_date')

        extra_kwargs = {
            'url': {'view_name': 'api:article-detail', 'lookup_field': 'id'}
        }

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class AdminArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    language = serializers.ChoiceField(choices=PREFERRED_LANGUAGE_CHOICES, source='get_language_display')

    class Meta:
        model = Article
        fields = ['status', 'author', 'author_name', 'title', 'post', 'language', 'publication_date', 'url']
        read_only_fields = ('publication_date',)

        extra_kwargs = {
            'url': {'view_name': 'api:article-detail', 'lookup_field': 'id'}
        }
