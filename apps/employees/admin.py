from django.contrib import admin

from .models import TableIRS, Employee, EmployeeSalary

admin.site.register(Employee)
admin.site.register(TableIRS)
admin.site.register(EmployeeSalary)

# Register your models here.
