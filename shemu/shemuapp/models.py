from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=300)
    id_number = models.CharField(max_length=300, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number
    
    def getRate(self):
        return self.rate
    
    def getOvertime(self):
        if not self.overtime_pay:
            message = "No overtime pay"
            return message
        else:
            return self.overtime_pay
    
    def resetOvertime(self):
        Employee.objects.filter(id=self.id).update(overtime_pay=0)

    def getAllowance(self):
        if not self.allowance:
            message = "No allowance"
            return message
        else:
            return self.allowance
        
    def __str__(self):
        return f"{self.pk}, rate:{self.rate}"

class Payslip(models.Model): #Payslip Attributes
    id_number = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='payslips') 
    #on_delete=models.CASCADE : https://www.freecodecamp.org/news/how-to-use-a-foreign-key-in-django/
    month = models.CharField(max_length=20)
    date_range = models.CharField(max_length=50)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(9999)
        ],
        help_text="Enter a 4-digit year"
    )
    pay_cycle = models.IntegerField()
    rate = models.FloatField()
    earnings_allowance = models.FloatField(default=0)
    deductions_tax = models.FloatField(default=0)
    deductions_health = models.FloatField(default=0)
    pag_ibig = models.FloatField(default=0)
    sss = models.FloatField(default=0)
    overtime = models.FloatField(default=0)
    total_pay = models.FloatField()

    def getIDNumber(self): #Methods
        return self.id_number

    def getMonth(self):
        return self.month

    def getDate_range(self):
        return self.date_range

    def getYear(self):
        return self.year

    def getPay_cycle(self):
        return self.pay_cycle

    def getRate(self):
        return f"{self.rate:.2f}"

    def getCycleRate(self):
        self.rate = self.rate/2
        return f"{self.rate:.2f}"

    def getEarnings_allowance(self):
        return f"{self.earnings_allowance:.2f}"

    def getDeductions_tax(self):
        return f"{self.deductions_tax:.2f}"

    def getDeductions_health(self):
        return f"{self.deductions_health:.2f}"

    def getPag_ibig(self):
        return f"{self.pag_ibig:.2f}"

    def getSSS(self):
        return f"{self.sss:.2f}"

    def getOvertime(self):
        return f"{self.overtime:.2f}"

    def getTotal_pay(self):
        return f"{self.total_pay:.2f}"

    def __str__(self):
        return "pk: {}, Employee: {}, Period: {} {}, {}, Cycle: {}, Total Pay: {:.2f}".format(self.pk, self.id_number, self.month, self.date_range, self.year, self.pay_cycle, self.total_pay)

class Account(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

    def getUsername(self):
        return self.username
    def getPasswowrd(self):
        return self.password
    def __str__(self):
        return self.username