from tabnanny import verbose

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from apps.school.models import School, Activities



class TypeFee(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0,validators=[MinValueValidator(0)])
    
    def get_absolute_url(self):
        return reverse('home')
    
    def __str__(self) -> str:
        return self.name



class Student(models.Model):
    YEAR_CHOICES = [
        (f"{year}/{year + 1}", f"{year}/{year + 1}") for year in range(2024, 2034)
    ]
    entry_year = models.CharField(max_length=4, verbose_name= "Ano de entrada",blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    scholl_year = models.CharField(
        max_length=9,
        choices=YEAR_CHOICES,
        verbose_name="Ano letivo",blank=True, null=True
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    education_officer = models.CharField(max_length=100, verbose_name="Nome Encarregado de educação",blank=True, null=True)
    nif = models.CharField(max_length=9, verbose_name="Nif", blank= True,null=True)
    phone_numeber_officer = models.CharField(max_length=100, verbose_name="Contacto Enc Educação")
    activity = models.ManyToManyField(Activities, blank=True, verbose_name="Atividade")
    fee = models.ManyToManyField(TypeFee, verbose_name="Mensalidade")
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('students_list')


    def value_fee_calcutator(self):
        fee = sum(fee.value for fee in self.fee.all())
        activity = sum(activity.value for activity in self.activity.all())
        total = fee + activity
        return total

    def __str__(self):
        return self.name

class MonthlyPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Estudante")
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(verbose_name='Data de pagamento')
    value = models.CharField(max_length=100, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    isLate = models.BooleanField(default=False)

    def is_late(self):
        today = timezone.now()
        next_month = self.payment_date.replace(day=1) + timedelta(days=32)
        first_dya_next_month = next_month.replace(day=1)

        return today >= first_dya_next_month and not self.isPaid


    def __str__(self):
        return f"fee- {self.student.name}, date_payment - {self.payment_date}. "