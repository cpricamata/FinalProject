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