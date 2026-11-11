from calendar import month

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import MonthlyPayment, Student



@receiver(post_save, sender=Student)
def create_montly_payment(sender, instance, created, **kwargs):
    fees = []
    student = instance

    scholl_year = int(instance.scholl_year.split('/')[0])
    number_of_fees = 12

    # Calcular o valor atualizado da mensalidade
    fee_value = student.value_fee_calcutator()

    for month in range(9, 9 + number_of_fees):
        month_year = divmod(month - 1, 12)
        current_month = month_year[1] + 1
        year = scholl_year + month_year[0]

        payment_date = date(year, current_month, 1)

        if current_month in [8, 9]:
            continue

        payment = MonthlyPayment.objects.filter(
            student=student,
            payment_date=payment_date
        ).first()

        if payment:
            # Atualizar apenas mensalidades ainda não pagas
            if not payment.isPaid and payment.value != str(fee_value):
                payment.value = fee_value
                payment.save(update_fields=['value'])
        else:
            # Criar nova mensalidade
            fees.append(
                MonthlyPayment(
                    student=student,
                    school=student.school,
                    payment_date=payment_date,
                    value=fee_value,
                    isPaid=False,
                    isLate=False
                )
            )

    if fees:
        MonthlyPayment.objects.bulk_create(fees)

    return fees