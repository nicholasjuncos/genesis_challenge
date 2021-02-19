from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('email', 'username', 'password')}),  # Remove username if only email
            (_('Personal info'), {'fields': ('first_name', 'last_name')}),
            (_('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),  # Remove username if only email
        }),
    )
    list_display = ('email', 'username', 'full_name', 'is_staff', 'is_superuser')  # Remove username if only email
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('email', 'username')  # Remove username if only email
