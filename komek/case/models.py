from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from department.models import Department, UserDepartment

from utils import time_utils

User = settings.AUTH_USER_MODEL


class Priority(models.Model):
    """
    """
    name = models.CharField(max_length=1000, null=False, blank=False,
                                            verbose_name=u"Priority name")
    timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                    verbose_name=u"Priority timestamp")

    def __unicode__(self):
        return u"{} {}".format(self.id, self.name)

    def full(self):
        return {
            'id': self.id,
            'name': self.name,
            'timestamp': self.timestamp,
        }

    class Meta:
        verbose_name = u"Priority"
        verbose_name_plural = u"Priorities"


class Comment(models.Model):
    """
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                                        related_name="user")
    text = models.CharField(max_length=1000000, null=False, blank=False,
                                            verbose_name=u"Comment text")
    timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                    verbose_name=u"Priority timestamp")

    def __unicode__(self):
        return u"{} {}".format(self.id, self.user.id)

    def full(self):
        return {
            'user': { self.user.full() },
            'id': self.id,
            'text': self.text,
            'timestamp': self.timestamp,
        }

    class Meta:
        verbose_name = u"Comment"
        verbose_name_plural = u"Comments"


class Case(models.Model):
    """
    """
    full_name = models.CharField(max_length=555, blank=False,
                                                    verbose_name=u'Full name')
    iin = models.CharField(max_length=15, blank=False, verbose_name=u'IIN')
    address = models.CharField(max_length=1000, blank=False,
                                                    verbose_name=u'Address')
    address_residential = models.CharField(max_length=1000, blank=False,
                                            verbose_name=u'Residential address')
    contacts = models.CharField(max_length=100, blank=False,
                                                    verbose_name=u'Contacts')
    status = models.CharField(max_length=1000, blank=False,
                                                    verbose_name=u'Status')
    place_of_work = models.CharField(max_length=1000, blank=False,
                                                verbose_name=u'Place of work')
    occupation = models.CharField(max_length=100, blank=False,
                                                    verbose_name=u'Occupation')
    income = models.CharField(max_length=1000, blank=False,
                                                    verbose_name=u'Income')
    health_condition = models.CharField(max_length=1000000, blank=False,
                                            verbose_name=u'Health condition')
    description = models.CharField(max_length=1000000, blank=False,
                                            verbose_name=u'Problem description')
    parent_case = models.IntegerField(null=True, blank=False,
                                                    verbose_name=u'Parent case')
    
    # SOCIAL WORKER
    needs = models.CharField(max_length=1000000, blank=False,
                                                    verbose_name=u'Needs')
    place = models.CharField(max_length=1000, blank=False,
                                            verbose_name=u'Place of gathering')
    datetime = models.CharField(max_length=100, blank=False,
                                            verbose_name=u"Time of gathering")
    problems = models.CharField(max_length=1000000, blank=False,
                                                    verbose_name=u'Problems')
    
    is_approved_by_social_worker = models.BooleanField(default=False,
                                    verbose_name=u"Approved by social worker")

    # DEPARTMENTAL COMMISSION
    deadline = models.BigIntegerField(null=False, blank=False, default=0,
                                                    verbose_name=u"Deadline")

    is_approved_by_departmental_worker = models.BooleanField(default=False,
                                verbose_name=u"Approved by departmental worker")

    is_approved_by_departmental_commission = models.BooleanField(default=False,
                            verbose_name=u"Approved by departmental commission")

    is_approved = models.BooleanField(default=False, verbose_name=u"Approved")
    
    def __unicode__(self):
        return u"{} {}".format(self.id, self.full_name)

    def full(self):
        obj = {
            'id': self.id,
            'full_name': self.full_name,
            'iin': self.iin,
            'address': self.address,
            'address_residential': self.address_residential,
            'contacts': self.contacts,
            'status': self.status, 
            'place_of_work': self. place_of_work,
            'occupation': self.occupation,
            'income': self.income,
            'health_condition': self.health_condition,
            'description': self.description,
            'needs': self.needs,
            'place': self.place,
            'datetime': self.datetime,
            'problems': self.problems,
            'is_approved_by_social_worker': self.is_approved_by_social_worker,
            'deadline': self.deadline,
            'is_approved': self.is_approved,
            'parent_case': self.parent_case,
        }

        dep_pri = CaseDepartmentPriority.objects.filter(case__id=self.id)
        if dep_pri is not None:
            obj['departments'] = [x.full() for x in dep_pri]

        solutions = SolutionCase.objects.filter(case__id=self.id).order_by('timestamp')
        if solutions is not None:
            obj['solutions'] = [x.full() for x in solutions]
            is_solutions_done = True
            for x in solutions:
                is_solutions_done = is_solutions_done & x.is_done
            obj['is_approved_by_departmental_worker'] = is_solutions_done

        results = ResultCase.objects.filter(case__id=self.id).order_by('timestamp')
        if results is not None:
            obj['results'] = [x.full() for x in results]
            is_results_done = True
            for x in results:
                is_results_done = is_results_done & x.is_done
            obj['is_approved_by_departmental_commission'] = is_results_done

        sib = Case.objects.filter(parent_case=self.parent_case)
        if sib is not None:
            obj['siblings'] = [x.id for x in sib]

        return obj

    class Meta:
        verbose_name = u"Case"
        verbose_name_plural = u"Cases"


class CaseDepartmentPriority(models.Model):
    """
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                                    related_name="case_for_department_priority")
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                            related_name="department_for_case")
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE,
                                            related_name="priority_for_case")

    def __unicode__(self):
        return u"{} {} {} {}".format(self.id, self.case.id, self.department.name,
                                                            self.priority.name)

    def full(self):
        return {
            'id': self.id,
            'department': self.department.full(),
            'priority': self.priority.full(),
        }

    class Meta:
        verbose_name = u"CaseDepartmentPriority"
        verbose_name_plural = u"CaseDepartmentPriorities"


class SolutionCase(models.Model):
    """
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                                            related_name="case_for_solution")
    user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE,
                default=None, related_name="user_department_for_solution")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                            related_name="comment_for_solution")
    info_type = models.CharField(max_length=100, default="solution",
                                            verbose_name=u'Type of info')
    is_done = models.BooleanField(default=False,
                                verbose_name=u"is done")
    timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                    verbose_name=u"Solution Case timestamp")

    def __unicode__(self):
        return u"{} {} {} {}".format(self.id, self.case.id, self.department.name,
                                                            self.comment.text)

    def full(self):
        return {
            'id': self.id,
            'user_department': self.user_department.full(),
            'comment': self.comment.full(),
            'info_type': self.info_type,
            'is_done': self.is_done,
            'timestamp': self.timestamp,
        }

    class Meta:
        verbose_name = u"Solution Case"
        verbose_name_plural = u"Solution Cases"


class ResultCase(models.Model):
    """
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                                                related_name="case_for_result")
    user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE,
                    default=None, related_name="user_department_for_result")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                            related_name="comment_for_result")
    info_type = models.CharField(max_length=100, default="result",
                                            verbose_name=u'Type of info')
    is_done = models.BooleanField(default=False,
                                verbose_name=u"is done")
    timestamp = models.BigIntegerField(null=False, blank=False, default=0,
                                    verbose_name=u"Result Case timestamp")

    def __unicode__(self):
        return u"{} {} {} {}".format(self.id, self.case.id, self.department.name,
                                                            self.comment.text)

    def full(self):
        return {
            'id': self.id,
            'user_department': self.user_department.full(),
            'comment': self.comment.full(),
            'info_type': self.info_type,
            'is_done': self.is_done,
            'timestamp': self.timestamp,
        }

    class Meta:
        verbose_name = u"Result Case"
        verbose_name_plural = u"Result Cases"