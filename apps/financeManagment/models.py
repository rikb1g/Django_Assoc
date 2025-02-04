from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from apps.school.models import School


class TypeFinanceMoviment(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class CategoryFinanceMoviment(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name
    

def file_upload_path(filename):
    return f'financeManager/{filename}'

class FinanceMovements(models.Model):
    moviment = models.ForeignKey(TypeFinanceMoviment, on_delete=models.CASCADE,blank=True, null=True)
    category = models.ForeignKey(CategoryFinanceMoviment, on_delete=models.PROTECT,blank=True, null=True, verbose_name="Categoria")
    billing_number= models.CharField(max_length=100, blank=True, null=True, verbose_name="Número Fatura")
    description = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='FinanceManager/', verbose_name="Ficheiro",blank=True,null=True)
    value = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Valor")
    date = models.DateField(null=True, blank=True, verbose_name="Data")
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"Moviment -{self.moviment} - value {self.value}, -date {self.date}"

    @classmethod
    def get_total_value_income_per_month(cls,school,month,year):
        return cls.objects.filter(school=school,date__year=year,date__month=month,
                                  moviment__name="income").aggregate(total=Sum('value'))['total'] or 0

    @classmethod
    def get_total_value_expense_per_month(cls,school,month,year):
        return cls.objects.filter(school=school,date__year=year,date__month=month,
                                  movimet__name="expense").aggregate(total=Sum('value'))['total'] or 0
    @classmethod
    def total_income(cls,school,year):
        value_total = 0

        for month in range(9,13):
            income = cls.objects.filter(school=school,date__year=year,date__month=month,
                                        moviment__name="income").aggregate(total=Sum('value'))['total'] or 0
            value_total += income

        for month in range(1,9):
            income = cls.objects.filter(school=school,date__year=year+1,date__month=month,
                                        moviment__name="income").aggregate(total=Sum('value'))['total'] or 0
            value_total += income

        return value_total

    @classmethod
    def total_expense(cls,school,year):
        value_total = 0
        for month in range(9,13):
            expense = cls.objects.filter(school=school,date__year=year,date__month=month,
                                         moviment__name="expense").aggregate(total=Sum('value'))['total'] or 0
            value_total += expense

        for month in range(1,9):
            expense = cls.objects.filter(school=school,date__year=year+1,date__month=month,
                                         moviment__name="expense").aggregate(total=Sum('value'))['total'] or 0
            value_total += expense

        return value_total










