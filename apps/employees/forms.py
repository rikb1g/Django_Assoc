from django import forms
from django.contrib import admin
from .models import TableIRS, Employee, EmployeeSalary


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','salary','hours','Irs','duodecimos','contract','start_date','end_date']
        widgets= {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'salary': forms.TextInput(attrs={'class':'form-control'}),
            'hours': forms.TextInput(attrs={'class':'form-control'}),
            'Irs': forms.SelectMultiple(attrs={'class':'form-control'}),
            'duodecimos': forms.NullBooleanSelect(attrs={'class':'form-control'}),
            'contract': forms.FileInput(attrs={'class':'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),          
        }

class EmployeeEndForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['end_date']
        widgets= {
            'end_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        }

class TableIRSForm(forms.ModelForm):
    class Meta:
        model = TableIRS
        fields = ['name','tax']
        widgets= {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'tax': forms.TextInput(attrs={'class':'form-control'}),
        }


class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalary
        fields = ['employee','start_date','end_date','fouls','value' ]
        widgets= {
            'employee': forms.SelectMultiple(attrs={'class':'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'fouls': forms.TextInput(attrs={'class':'form-control'}),
            'value': forms.TextInput(attrs={'class':'form-control'}),
        }

class EmployeeEndForm(admin.ModelAdmin):
    form = EmployeeEndForm

class EmployeeForm(admin.ModelAdmin):
    form = EmployeeForm

class TableIRSForm(admin.ModelAdmin):
    form = TableIRSForm

class EmployeeSalaryForm(admin.ModelAdmin):
    form = EmployeeSalaryForm