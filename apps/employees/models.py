from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import ForeignKey


from apps.school.models import School

class TableIRS(models.Model):
    name = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=5,decimal_places=5)

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    security_system = models.FloatField(default=0.11, verbose_name="Seg Social")
    salary = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Saláro")
    hours = models.IntegerField(default=20,validators=[MinValueValidator(0)], verbose_name="Horas")
    Irs = models.ManyToManyField(TableIRS,verbose_name="IRS")
    duodecimos = models.BooleanField(default=True,verbose_name="Duodécimos")
    school = ForeignKey(School,on_delete=models.CASCADE, verbose_name="Escola")
    contract = models.FileField(blank=True, upload_to="employees/contract",verbose_name="Contrato")
    start_date = models.DateField(verbose_name="Data de início")
    end_date = models.DateField(blank=True, null=True, verbose_name="Fim do contrato")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class EmployeeSalary(models.Model):
    employee= models.ForeignKey(Employee,on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Data de início")
    end_date = models.DateField( verbose_name="Data fim")
    fouls = models.FloatField(validators=[MinValueValidator(0)], default=0, verbose_name="Falta em horas")
    value = models.FloatField(validators=[MinValueValidator(0)], default=0, verbose_name="Valor de Salário")

    def __str__(self):
        return f"{self.employee} - data {self.start_date} a {self.end_date}"