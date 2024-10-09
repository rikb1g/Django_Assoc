from django.contrib import admin
from .models import Student, TypeFee,MonthlyPayment

admin.site.register(Student)
admin.site.register(TypeFee)
admin.site.register(MonthlyPayment)