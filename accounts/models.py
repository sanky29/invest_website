from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from .database import *

class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, phone, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password,phone):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255, unique=True)
    phone = models.CharField('phone',max_length=13, unique=True)
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    is_active = models.BooleanField('active',default=True,help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField('staff status',
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField('date joined', default=timezone.now
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadhar = models.CharField(null=True, max_length=12)
    pan = models.CharField(null=True, max_length=10)
    image = models.ImageField(null=True, default='{static "/images/profile.jpeg"}')


class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sector = models.CharField(choices=SECTORS, max_length=100)
    address = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    fund_need = models.IntegerField()
    fund_raised = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(null=True)
    document = models.FileField(null=True)


class Invest(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=1000)
    modeofpay = models.CharField(choices=MODES_OF_PAYMENT, max_length=100)
