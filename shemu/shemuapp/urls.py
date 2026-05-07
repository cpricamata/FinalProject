from django.urls import path
from . import views


urlpatterns = [
    path('', views.employees, name='employees'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path('update-employee/', views.update_employee, name='update_employee'),
    path('delete-employee/', views.delete_employee, name='delete_employee'),
    path('add-overtime/', views.add_overtime, name='add_overtime'),
    path('payslips/', views.payslips, name='payslips'),
    path('view-payslip/<int:payslip_id>/', views.view_payslip, name='view_payslip'),
]