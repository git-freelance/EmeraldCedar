from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import resolve_url

from sorl.thumbnail import ImageField
from smart_selects.db_fields import ChainedForeignKey

from core.helpers import upload_common_images_to


'''
CUSTOM USER
'''


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        # if is_staff and is_superuser:
        #     user.user_type = ADMIN  # TODO Just highlight

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user
        """
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user
        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class AbstractCustomUser(AbstractBaseUser, PermissionsMixin):
    """Abstract User with the same behaviour as Django's default User.
    AbstractEmailUser does not have username field. Uses email as the
    USERNAME_FIELD for authentication.
    Use this if you need to extend EmailUser.
    Inherits from both the AbstractBaseUser and PermissionMixin.
    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """

    email = models.EmailField(_('email address'), max_length=255,
                              unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        try:
            send_mail(subject, message, from_email, [self.email], **kwargs)
        except Exception as e:
            print(e)


class CustomUser(AbstractCustomUser):
    # type_choices = (
    #     (ADMIN, 'Admin'),
    #     (CLIENT, 'Client'),
    # )

    # user_type = models.CharField(max_length=10, choices=type_choices, default=CLIENT)
    primary_phone = models.CharField(max_length=100, blank=True)
    secondary_phone = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    class Meta(AbstractCustomUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def is_admin(self):
        return self.is_superuser

    def is_client(self):
        return not self.is_admin()


class Attribute(models.Model):
    # projects = models.ManyToManyField(Project, related_name='attributes')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='subattributes')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class WarrantyType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='projects')
    address = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, )
    cover_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)

    warranty_type = models.ForeignKey(WarrantyType, blank=True, null=True, related_name='projects', on_delete=models.SET_NULL)
    warranty_start_date = models.DateField(blank=True, null=True)
    warranty_end_date = models.DateField(blank=True, null=True)
    warranty_certificate = ImageField(upload_to=upload_common_images_to, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return resolve_url('dash_project', self.pk)

    class Meta:
        ordering = ('-created_at',)


class AttributeSubattributePair(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    subattribute = ChainedForeignKey(SubAttribute, chained_field='attribute',
                                     chained_model_field='attribute',
                                     blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
