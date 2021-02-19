import csv
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.utils.cache import patch_cache_control
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


def never_ever_cache(decorated_function):
    """Like Django @never_cache but sets more valid cache disabling headers.

    @never_cache only sets Cache-Control:max-age=0 which is not
    enough. For example, with max-axe=0 Firefox returns cached results
    of GET calls when it is restarted.
    """

    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response

    return wrapper


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class NeverCacheMixin(object):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(NeverCacheMixin, self).dispatch(request, *args, **kwargs)


class NeverEverCacheMixin(object):
    @method_decorator(never_ever_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(NeverEverCacheMixin, self).dispatch(request, *args, **kwargs)


class HasGroupMixin(object):
    group = None
    groups = None

    def get_groups(self):
        if self.group is None and self.groups is None:
            raise ImproperlyConfigured(
                '{0} is missing either a group or groups attribute. Define one, or override '
                '{0}.get_group().'.format(self.__class__.__name__)
            )
        if self.group and not self.groups:
            return [self.group, 'SoftwareDevs']
        else:
            self.groups.append('SoftwareDevs')
            return self.groups

    def check_group(self):
        groups = self.get_groups()
        if self.request.user.is_superuser:
            return True
        return self.request.user.groups.filter(name__in=groups).exists()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_group():
            raise PermissionDenied('You do not have the proper groups assigned to you.')
        return super(HasGroupMixin, self).dispatch(request, *args, **kwargs)


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }

    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)
