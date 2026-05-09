from django.contrib import admin
from .models import Employee, Payslip, Account

admin.site.register(Employee)

admin.site.register(Payslip)

admin.site.register(Account)