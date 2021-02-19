from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel, StatusModel

from . import ARTICLE_STATUS_CHOICES
from ..common import PREFERRED_LANGUAGE_CHOICES

User = get_user_model()


class Article(TimeStampedModel, StatusModel):
    status = models.CharField(max_length=9, choices=ARTICLE_STATUS_CHOICES, default='Draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    post = models.TextField()
    language = models.CharField(max_length=2, choices=PREFERRED_LANGUAGE_CHOICES)
    publication_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.title, self.author, self.created, self.status)

    def save(self):
        if self.status == 'Published' and not self.publication_date:
            self.publication_date = timezone.now()
        if self.status == 'Draft':
            self.publication_date = None
        super().save()
