from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class BankUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, card_number, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(full_name=username, card_number=card_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, card_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, card_number, password, **extra_fields)

    def create_superuser(self, username, card_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, card_number, password, **extra_fields)


class BankClient(AbstractBaseUser, PermissionsMixin):
    card_number = models.BigIntegerField(
        _('card number'),
        primary_key=True,
        unique=True
    )
    full_name = models.CharField(
        _('full name'),
        max_length=255,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.'
                    ' Unselect this instead of deleting accounts.')
    )
    # money value stored as smaller part of currency (kops for rubles and cents for dollar) to prevent float point
    # problems on calculation and custom DB storage. So $100 will be 10000 here.
    balance = models.BigIntegerField(
        _('balance'),
        default=0
    )
    login_fail_count = models.SmallIntegerField(
        _('login fail count'),
        default=0
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    USERNAME_FIELD = 'card_number'
    REQUIRED_FIELDS = ['full_name', 'balance']
    MAX_LOGIN_FAIL_COUNT = 3
    objects = BankUserManager()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    class Meta:
        verbose_name = _('bank client')
        verbose_name_plural = _('bank clients')


class ClientAction(models.Model):
    bank_client = models.ForeignKey(BankClient, blank=False, null=False)
    code = models.SmallIntegerField(verbose_name=_('action code'))
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('action time'))
    value = models.BigIntegerField(verbose_name=_('action value'))

    ACTION_CHECK_BALANCE = 1
    ACTION_GET_MONEY = 2

    class Meta:
        verbose_name = _('client action')
        verbose_name_plural = _('client actions')
