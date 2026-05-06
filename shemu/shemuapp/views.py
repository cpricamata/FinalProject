from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip

# Create your views here.

def employees(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})

def create_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        id_number = request.POST['id_number']
        rate = float(request.POST['rate'])
        allowance = request.POST.get('allowance', 0)
        if allowance == '':
            allowance = 0
        
        Employee.objects.create(
            name=name,
            id_number=id_number,
            rate=rate,
            allowance=float(allowance)
        )
        return redirect('employees')
    return render(request, 'create_employee.html')

def update_employee(request, id_number):
    if request.method == 'POST':
        if 'id_number' in request.POST and 'name' not in request.POST:
            id_number = request.POST.get('id_number')
            employee = get_object_or_404(Employee, id_number=id_number)
            return render(request, 'update_employee.html', {'employee': employee})
        Employee.objects.filter(if_number=id_number).update(
            name=request.POST.get('name'),
            id_number=request.POST.get('rate'),
            rate=float(request.POST.get('rate')),
            allowance=float(request.POST.get('allowance', 0) or 0)
        )
        return redirect ('employees')
    return redirect('employees')

def delete_employee(request, id_number):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        Employee.objects.filter(id_number=id_number).delete()
    return redirect('employees')

def add_overtime(request, id_number):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        employee = get_object_or_404(Employee, id_number=id_number)
        hours = float(request.POST.get('overtime_hours', 0))

        overtime_amount = (employee.rate /160) * 1.5 * hours

        if employee.overtime_pay:
            new_overtime = employee.overtime_pay + overtime_amount
        else:
            new_overtime = overtime_amount

        Employee.objects.filter(id_number=id_number).update(
            overtime_pay=new_overtime
        )
    return redirect('employees')

def payslips(request):
    all_employees = Employee.objects.all()
    all_payslips = Payslip.objects.all()

    #will cont this since i can't see Payslips model yet ;;
