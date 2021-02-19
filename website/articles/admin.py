from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'publication_date', 'status',)
    list_filter = ('status',)
    search_fields = ('title', 'author')
    ordering = ('status', 'author')
