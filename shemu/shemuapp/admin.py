from django.contrib import admin

from .models import Employee
admin.site.register(Employee)

from .models import Payslip
admin.site.register(Payslip)
# Register your models here.
