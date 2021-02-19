from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from ..common import PREFERRED_LANGUAGE_CHOICES

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):

    preferred_language = serializers.ChoiceField(choices=PREFERRED_LANGUAGE_CHOICES)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.preferred_language = self.data.get('preferred_language')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'full_name', 'preferred_language', 'url']

        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', 'lookup_field': 'username'}
        }
