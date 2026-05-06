from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=300)
    id_number = models.CharField(max_length=300)
    rate = models.FloatField(max_digits=10, decimal_places=2)
    overtime_pay = models.FloatField(max_digits=10, decimal_places=2, null=True, blank=True)
    allowance = models.FloatField(max_digits=10, decimal_places=2, null=True, blank=True)

    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number
    
    def getRate(self):
        return self.rate
    
    def getOvertime(self):
        if self.overtime_pay is not None:
            message = "No overtime pay"
            return message
        else:
            return self.overtime_pay
    
    def resetOvertime(self):
        self.overtime_pay = 0

    def getAllowance(self):
        if self.allowance is not None:
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
        year = models.CharField(max_length=4)
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
        return self.rate

    def getCycleRate(self):
        return self.rate / 2

    def getEarnings_allowance(self):
        return self.earnings_allowance

    def getDeductions_tax(self):
        return self.deductions_tax

    def getDeductions_health(self):
        return self.deductions_health

    def getPag_ibig(self):
        return self.pag_ibig

    def getSSS(self):
        return self.sss

    def getOvertime(self):
        return self.overtime

    def getTotal_pay(self):
        return self.total_pay

    def __str__(self):
        return "pk: {}, Employee: {}, Period: {} {}, {}, Cycle: {}, Total Pay: {}".format(self.pk, self.id_number, self.month, self.date_range, self.year, self.pay_cycle, self.total_pay)


