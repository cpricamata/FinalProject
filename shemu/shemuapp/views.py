from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip

# Create your views here.

users_list = []
current_user = None

def signup_view(request):
    global current_user
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'shemuapp/signup.html', {
                'error': 'Passwords do not match'
            })
        
        for user in users_list:
            if user['username'] == username:
                return render(request, 'shemuapp/signup.html', {
                    'error': 'Username already exists'
                })
        
        users_list.append({
            'username': username,
            'password': password1
        })
        
        current_user = username
        return redirect('employees')
    
    return render(request, 'shemuapp/signup.html')

def login_view(request):
    global current_user
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        for user in users_list:
            if user['username'] == username and user['password'] == password:
                current_user = username
                return redirect('employees')
        
        return render(request, 'shemuapp/login.html', {
            'error': 'Invalid username or password'
        })
    
    return render(request, 'shemuapp/login.html')

def logout_view(request):
    global current_user
    current_user = None
    return redirect('login')

def manage_account(request, pk):
    global current_user
    
    if current_user is None:
        return redirect('login')
    
    return render(request, 'shemuapp/manage_account.html', {
        'current_user': current_user,
        'pk': pk
    })

def change_password(request, pk):
    global current_user
    
    if current_user is None:
        return redirect('login')
    
    pk = int(pk)
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        for user in users_list:
            if user['username'] == current_user:
                if user['password'] != current_password:
                    return render(request, 'shemuapp/change_password.html', {
                        'error': 'Current password is incorrect',
                        'pk': pk
                    })
                
                if new_password1 != new_password2:
                    return render(request, 'shemuapp/change_password.html', {
                        'error': 'New passwords do not match',
                        'pk': pk
                    })                
                user['password'] = new_password1
                break
        
        return redirect('manage_account', pk=pk)
    return render(request, 'shemuapp/change_password.html', {
        'pk': pk
    })

def delete_account(request, pk):
    global current_user
    
    if current_user is None:
        return redirect('login')
    
    if request.method == 'POST':
        for user in users_list:
            if user['username'] == current_user:
                users_list.remove(user)
                break       
        current_user = None
        return redirect('signup')
    
    return redirect('manage_account', pk=pk)

#EMPLOYEES SECTION GRR

def employees(request):
    global current_user

    if current_user is None:
        return redirect('login')
    
    employees = Employee.objects.all()
    return render(request, 'shemuapp/employees.html', {'employees': employees})

def create_employee(request):
    global current_user

    if current_user is None:
        return redirect('login')
    
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
    return render(request, 'shemuapp/create_employee.html')

def update_employee(request, id_number=None):
    global current_user
    
    if current_user is None:
        return redirect('login')

    if not id_number:
        id_number = request.POST.get('id_number')

    if request.method == 'POST':
        if 'name' not in request.POST:
            employee = get_object_or_404(Employee, id_number=id_number)
            return render(request, 'shemuapp/update_employee.html', {'emp': employee})
        
        try:
            name = request.POST.get('name')
            rate = request.POST.get('rate')
            allowance = request.POST.get('allowance')

            Employee.objects.filter(id_number=id_number).update(
                name=name,
                rate=float(rate) if rate and rate.strip() else 0.0,
                allowance=float(allowance) if allowance and allowance.strip() else 0.0
            )
            return redirect('employees')
        
        except (ValueError, TypeError):
            return redirect('employees')

    return redirect('employees')

def delete_employee(request, id_number=None):
    global current_user
    
    if current_user is None:
        return redirect('login')
    
    if request.method == 'POST':
        if not id_number:
            id_number = request.POST.get('id_number')
        employee = get_object_or_404(Employee, id_number=id_number)

        employee.delete()
    return redirect('employees')

def add_overtime(request, id_number):
    global current_user
    
    if current_user is None:
        return redirect('login')
    
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        employee = get_object_or_404(Employee, id_number=id_number)
        hours = float(request.POST.get('overtime_hours', 0))

        if hours < 0:
            all_employees = Employee.objects.all()
            return render(request, 'employees.html', {
                'employees': all_employees,
                'error': 'Hours cannot be negative',
            })

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
    global current_user
    
    if current_user is None:
        return redirect('login')
    
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
    global current_user
    
    if current_user is None:
        return redirect('login')
    
    payslip = get_object_or_404(Payslip, id=payslip_id)
    return render(request, 'view_payslip.html', {'payslip': payslip})