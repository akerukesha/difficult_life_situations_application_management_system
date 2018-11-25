from django.contrib import admin

from models import Priority, Comment, Case, CaseDepartmentPriority, SolutionCase, ResultCase

admin.site.register(Priority)
admin.site.register(Comment)
admin.site.register(Case)
admin.site.register(CaseDepartmentPriority)
admin.site.register(SolutionCase)
admin.site.register(ResultCase)