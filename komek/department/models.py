from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from utils import time_utils


User = settings.AUTH_USER_MODEL


class Department(models.Model):
    """
    """
    name = models.CharField(max_length=1000, null=False, blank=False,
                                            verbose_name=u"Department name")
    timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                    verbose_name=u"Department timestamp")

    def __unicode__(self):
        return u"{} {}".format(self.id, self.name)

    def full(self):
    	return {
    		'id': self.id,
    		'name': self.name,
    		'timestamp': self.timestamp,
    	}

    class Meta:
        verbose_name = u"Department"
        verbose_name_plural = u"Departments"


class UserDepartment(models.Model):
    """
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="user_for_department")
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                    related_name="department_for_user")

    def __unicode__(self):
        return u"{} {}".format(self.user.username, self.department.name)

    def full(self):
        return {
            'user': self.user.full(),
            'department': self.department.full(),
        }

    class Meta:
        verbose_name = u"User Department"
        verbose_name_plural = u"User Departments"