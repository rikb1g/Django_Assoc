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
    name = models.CharField(max_length=100, verbose_name="Nome")
    entry_year = models.IntegerField(verbose_name="Ano de Matrícula")
    out_year = models.IntegerField(blank=True, null=True, verbose_name="Ano de saída")
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    education_officer = models.CharField(max_length=100, verbose_name="Nome Encarregado de educação")
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