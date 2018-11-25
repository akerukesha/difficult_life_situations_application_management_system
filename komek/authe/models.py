from __future__ import unicode_literals

from django.db import models

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from utils import time_utils
from utils.user_types import USER_TYPES, USER, SOCIAL_WORKER, COMMISSION_HEAD, DEPARTMENTAL_WORKER, DEPARTMENTAL_COMMISSION

from department.models import Department


class MainUserManager(BaseUserManager):
    """
    """
    def create_user(self, username, password=None):
        """
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username)
        user.set_password(password)
        user.timestamp = time_utils.get_timestamp_in_milli()
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        """
        user = self.create_user(username, password=password)
        user.email = username
        user.is_admin = True
        user.is_superuser = True
        user.is_moderator = True
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    """
    """
    username = models.CharField(max_length=100, blank=False, unique=True,
                                                    verbose_name=u'Username')
    full_name = models.CharField(max_length=555, blank=True,
                                                    verbose_name=u'Full name')
    email = models.CharField(max_length=50, blank=True,
                                                    verbose_name=u'E-mail')
    is_active = models.BooleanField(default=True, verbose_name=u"Active")
    is_admin = models.BooleanField(default=False, verbose_name=u'Admin')
    is_moderator = models.BooleanField(default=False, verbose_name=u"Moderator")
    timestamp = models.BigIntegerField(default=0)
    phone_number = models.CharField(max_length=50, blank=True,
                                                    verbose_name=u'Phone number')
    user_type = models.SmallIntegerField(choices=USER_TYPES,
                    default=USER, verbose_name=u"User type")
    

    objects = MainUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return u"{} {}".format(self.id, self.username)

    def is_staff(self):
        """
        """
        return self.is_admin or self.is_moderator

    def get_full_name(self):
        return u"{} {}".format(self.username, self.full_name)

    def get_short_name(self):
        return self.username

    def full(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'timestamp': self.timestamp,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'is_moderator': self.is_moderator,
            'phone_number': self.phone_number,
            'user_type': self.user_type,
        }

    class Meta:
        verbose_name = u"User"
        verbose_name_plural = u"Users"


class TokenLog(models.Model):
    """
    """
    token = models.CharField(max_length=500, blank=False, null=False)
    user = models.ForeignKey(MainUser, blank=False, null=False,
                                                        related_name='tokens')

    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "token={0}".format(self.token)

    class Meta:
        index_together = [
            ["token", "user"]
        ]