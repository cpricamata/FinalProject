from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('manage-account/<int:pk>/', views.manage_account, name='manage_account'),
    path('change-password/<int:pk>/', views.change_password, name='change_password'),
    path('delete-account/<int:pk>/', views.delete_account, name='delete_account'),
    path('employees/<int:pk>/', views.employees, name='employees'),
    path('create-employee/<int:pk>/', views.create_employee, name='create_employee'),
    path('update-employee/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete-employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('add-overtime/<int:pk>/', views.add_overtime, name='add_overtime'),
    path('payslips/<int:pk>/', views.payslips, name='payslips'),
    path('view-payslip/<int:pk>/<int:payslip_id>/', views.view_payslip, name='view_payslip'),
]