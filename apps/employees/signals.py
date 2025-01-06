from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeSalary
from apps.financeManagment.models import FinanceMovements, CategoryFinanceMoviment,TypeFinanceMoviment



@receiver(post_save, sender=EmployeeSalary)
def salary_calculater(sender, created, instance, **kwargs):
    houry_rate = (instance.employee.salary * 12)/(52*instance.employee.hours)
    if created:
        if instance.pk:
            salary_update = EmployeeSalary.objects.get(pk=instance.pk)
            off_value = houry_rate * instance.fouls
            social_security = (instance.value - off_value) * salary_update.employee.security_system

            if salary_update.employee.duodecimos:
                duodecimos = salary_update.employee.salary / 12
                final_value = instance.value - social_security + duodecimos + duodecimos
            else:
                final_value = instance.value - social_security
            
            expense = CategoryFinanceMoviment.objects.get_or_create(name='expense')
            salary= TypeFinanceMoviment.objects.get_or_create(name="Salários")
            
            try:
                finance_moviment = FinanceMovements.objects.get(description=f"Func: {salary_update.employee.name},de {salary_update.start_date} a {salary_update.end_date}")
                finance_moviment.description =f"Func: {instance.employee.name},de {instance.start_date} a {instance.end_date}"
                finance_moviment.value= final_value
                finance_moviment.date=instance.end_date
                finance_moviment.save()

            except FinanceMovements.DoesNotExist:
                FinanceMovements.objects.create(moviment= expense, category=salary,description=f"Func: {instance.employee.name},de {instance.start_date} a {instance.end_date}", value= final_value,date =instance.end_date,school=instance.employee.school)

            
            

            






