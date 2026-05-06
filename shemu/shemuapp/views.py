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
        
        #if only id number is submitted, it means the user clicked "Update" button
        #show the update form w employee data
        if 'id_number' in request.POST and 'name' not in request.POST:
            id_number = request.POST.get('id_number')
            employee = get_object_or_404(Employee, id_number=id_number)
            return render(request, 'update_employee.html', {'employee': employee})
        
        #update the employee if all fields are submitted
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

    months = ['January', 'February', 'March', 
              'April', 'May', 'June', 
              'July', 'August', 'September', 
              'October', 'November', 'December']
    
    if request.method == 'POST':
        payroll_for = request.POST.get('payroll_for')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cycle = int(request.POST.get('cycle'))

        if cycle == 1:
            date_range = "1-15"
        else:
            date_range = "16-31"

        if payroll_for == 'all':
            employees_to_process = Employee.objects.all()
        else:
            employees_to_process = Employee.objects.filter(id_number=payroll_for)

        #checking existing payslips
        errors = []

        for emp in employees_to_process:
            exists = Payslip.objects.filter(
                id_number=emp,
                month=month,
                year=year,
                pay_cycle=cycle
            ).exists()

            if exists:
                errors.append(emp.id_number)
        
        if errors:
            return render(request, 'payslips.html', {
                'employees': all_employees,
                'payslips': all_payslips,
                'months': months,
                'error': f"Payslips already exist for: {', '.join(errors)}"
            })
        
        for emp in employees_to_process:
            half_rate = emp.rate / 2
            allowance = emp.getAllowance()
            overtime = emp.getOvertime()

            if cycle == 1: #cycle1: Pag-Ibig
                pag_ibig = 100
                philhealth = 0
                sss = 0

                tax_base = half_rate + allowance +overtime - pag_ibig
                tax = tax_base * 0.2
                total_pay = tax_base - tax
            else: #cycle2: Philhealth and SSS
                pag_ibig = 0
                philhealth = emp.rate * 0.04
                sss = emp.rate * 0.045

                tax_base = half_rate + allowance + overtime - philhealth - sss
                tax = tax_base * 0.2
                total_pay = tax_base - tax
            
            Payslip.objects.create(
                id_number=emp,
                month=month,
                date_range=date_range,
                year=year,
                pay_cycle=cycle,
                rate=emp.rate,
                earnings_allowance=allowance,
                deductions_tax=tax,
                deductions_health=philhealth,
                pag_ibig=pag_ibig,
                sss=sss,
                overtime=overtime,
                total_pay=total_pay
            )

            emp.resetOvertime()

        return redirect('payslips')
    return render(request, 'payslips.html', {
        'employees': all_employees,
        'payslips': all_payslips,
        'months': months
    })

def view_payslip(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)
    return render(request, 'view_payslip.html', {'payslip: payslip'})