from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

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
