from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from ..common.fields import CIEmailField, CICharField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# IF CHANGING TO EMAIL ONLY AND NO USERNAME, WILL HAVE TO RUN MAKEMIGRATIONS AND MIGRATE! MAYBE EVEN DELETE DB
class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = CICharField(
        _('username'),
        max_length=150,
        unique=True,  # Remove this when utilizing email auth
        # null=True,  # Comment this back in when utilizing email auth
        # blank=True, # Comment this back in when utilizing email auth
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # username = None  # Comment this in if NOT wanted usernames, and comment above username field and validator OUT
    email = CIEmailField(_('email address'), unique=True)  # Change to blank is true and not unique if emails not needed
    # USERNAME_FIELD = 'email'  # Comment out if using usernames
    # REQUIRED_FIELDS = []  # comment this out if change to username

    class Meta:
        ordering = ('email',)

    # objects = UserManager()  # Comment out for username validation

    def __str__(self):
        return self.email  # Change to email in future
        # if self.name:
        #     return self.name
        # if self.first_name and self.last_name:
        #     return self.first_name + " " + self.last_name
        # else:
        #     return "Anonymous User"

    @property
    def full_name(self):
        return (self.first_name + ' ' + self.last_name).strip()

    def has_group(self, group):
        return self.groups.filter(name=group).exists()

    def initial_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
        }


