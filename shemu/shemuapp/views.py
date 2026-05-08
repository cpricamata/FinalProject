from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip, Account

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match'
            })
        
        if Account.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })
    
        Account.objects.create(
            username=username,
            password=password1
        )
        
        return redirect('login')
    
    return render(request, 'signup.html')

def login_view(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        account = Account.objects.filter(username=username, password=password).first()
        
        if account:
            return redirect('employees', pk=account.pk)
        
        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })
    
    return render(request, 'login.html')

def logout_view(request):
    return redirect('login')

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    return render(request, 'manage_account.html', {
        'current_user': account.getUsername(),
        'pk': pk
    })

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if account.password != current_password:
            return render(request, 'change_password.html', {
                'error': 'Current password is incorrect',
                'pk': pk
                    })
                
        if new_password1 != new_password2:
            return render(request, 'change_password.html', {
                'error': 'New passwords do not match',
                'pk': pk
            })      

        account.password = new_password1          
        account.save()

        return redirect('manage_account', pk=pk)
    return render(request, 'change_password.html', {
        'pk': pk
    })

def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        account.delete()
        return redirect('signup')
    
    return redirect('manage_account', pk=pk)

#EMPLOYEES SECTION GRR

def employees(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees, 'pk': pk, 'current_user': account.getUsername()})

def create_employee(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
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
        return redirect('employees', pk=pk)
    return render(request, 'create_employee.html', {'pk': pk, 'current_user': account.getUsername()})

def update_employee(request, pk, id_number=None):
    account = get_object_or_404(Account, pk=pk)

    if not id_number:
        id_number = request.POST.get('id_number')

    if request.method == 'POST':
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if name and rate:
            original_id = request.POST.get('original_id_number', id_number)

            Employee.objects.filter(id_number=original_id).update(
                name=name,
                id_number=request.POST.get('id_number'),
                rate=float(rate) if rate and rate.strip() else 0.0,
                allowance=float(allowance) if allowance and allowance.strip() else 0.0
            )
            return redirect('employees', pk=pk)
        
        else:
            employee = get_object_or_404(Employee, id_number=id_number)
            return render(request, 'update_employee.html', {
                'emp': employee,
                'pk': pk,
                'current_user': account.getUsername()
            })

    return redirect('employees', pk=pk)

def delete_employee(request, pk, id_number=None):
    account = get_object_or_404(Account, pk=pk)
    
    if request.method == 'POST':
        if not id_number:
            id_number = request.POST.get('id_number')
        employee = get_object_or_404(Employee, id_number=id_number)

        employee.delete()
    return redirect('employees', pk=pk)

def add_overtime(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        employee = get_object_or_404(Employee, id_number=id_number)
        hours = float(request.POST.get('overtime_hours', 0))

        if hours < 0:
            all_employees = Employee.objects.all()
            return render(request, 'employees.html', {
                'employees': all_employees,
                'error': 'Hours cannot be negative',
                'pk': pk,
                'current_user': account.getUsername()
            })

        rate = float(employee.rate)
        current_overtime = float(employee.overtime_pay) if employee.overtime_pay else 0.0

        overtime_amount = (rate /160) * 1.5 * hours

        new_overtime = current_overtime + overtime_amount

        Employee.objects.filter(id_number=id_number).update(
            overtime_pay=new_overtime
        )
    return redirect('employees', pk=pk)

def payslips(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
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
            return render(request, 'shemuapp/payslips.html', {
                'employees': all_employees,
                'payslips': all_payslips,
                'months': months,
                'error': f"Payslips already exist for: {', '.join(errors)}"
            })
        
        for emp in employees_to_process:
            half_rate = float(emp.rate) / 2
            allowance = float(emp.allowance) if emp.allowance else 0.0
            overtime = float(emp.overtime_pay) if emp.overtime_pay else 0.0

            if cycle == 1: #cycle1: Pag-Ibig
                pag_ibig = 100
                philhealth = 0
                sss = 0

                tax_base = half_rate + allowance +overtime - pag_ibig
                tax = tax_base * 0.2
                total_pay = tax_base - tax
            else: #cycle2: Philhealth and SSS
                pag_ibig = 0
                philhealth = float(emp.rate) * 0.04
                sss = float(emp.rate) * 0.045

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

        return redirect('payslips', pk=pk)
    return render(request, 'payslips.html', {
        'employees': all_employees,
        'payslips': all_payslips,
        'months': months,
        'pk': pk,
        'current_user': account.getUsername()
    })

def view_payslip(request, pk, payslip_id):
    account = get_object_or_404(Account, pk=pk)
    payslip = get_object_or_404(Payslip, id=payslip_id)
<<<<<<< Updated upstream

    gross_pay = payslip.getCycleRate() + payslip.earnings_allowance + payslip.overtime
    total_deductions = payslip.deductions_tax + payslip.pag_ibig + payslip.deductions_health + payslip.sss

    return render(request, 'view_payslip.html', {'payslip': payslip, 'pk': pk, 'gross_pay': gross_pay, 'tota_deductions': total_deductions, 'current_user': account.getUsername()})

def about_us(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'about_us.html', {
        'pk': pk,
        'current_user': account.getUsername()
    })
=======
    return render(request, 'shemuapp/view_payslip.html', {'payslip': payslip, 'pk': pk, 'current_user': account.getUsername()})

def homepage(request):
    return render(request, 'shemuapp/homepage.html')
>>>>>>> Stashed changes
