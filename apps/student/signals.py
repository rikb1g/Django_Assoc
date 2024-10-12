from calendar import month

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import MonthlyPayment, Student



@receiver(post_save, sender=Student)
def create_montly_payment(sender, instance, created, **kwargs):
    fees = []
    if created:
        current_year = instance.entry_year
        number_of_fees = 12

        for month in range(9,9+ number_of_fees):
            month_year = divmod(month -1 ,12)
            current_month = month_year[1] +1
            year = current_year + month_year[0]

            payment_date = date(year,current_month,1)
            print(payment_date)

            if current_month in [8,9]:
                continue
            fee = MonthlyPayment(
                student=instance,
                school=instance.school,
                payment_date=payment_date,
                isPaid= False,
                isLate= False
            )
            print(fee)
            fees.append(fee)
    if fees:
        MonthlyPayment.objects.bulk_create(fees)

    return fees
