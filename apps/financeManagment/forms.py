from django import forms
from django.contrib import admin
from .models import TypeFinanceMoviment, CategoryFinanceMoviment, FinanceMovements


class TypeFinanceMovimentForm(forms.ModelForm):
    class Meta:
        model = TypeFinanceMoviment
        fields = ['name']
        widgjets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }


class CategoryFinanceMovimentForm(forms.ModelForm):
    class Meta:
        model = CategoryFinanceMoviment
        fields = ['name']
        widgjets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }

class FinanceMovementsForm(forms.ModelForm):
    class Meta:
        model = FinanceMovements
        fields = ['moviment', 'category', 'billing_number','description', 'value', 'date', 'file']
        widgjets = {
            'moviment': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'billing_number': forms.TextInput(attrs={'class':'form-control'}),
            'value': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'file': forms.FileInput(attrs={'class':'form-control'}),
        }


class TypeFinanceMovimentAdmin(admin.ModelAdmin):
    form = TypeFinanceMovimentForm

class CategoryFinanceMovimentAdimn(admin.ModelAdmin):
    form = CategoryFinanceMovimentForm
class FinanceMovementsAdmin(admin.ModelAdmin):
    form = FinanceMovementsForm

