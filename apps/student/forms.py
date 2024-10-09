from django import forms
from django.contrib import admin
from .models import Activities, TypeFee, Student



class StudentForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        school = kwargs.pop('school',None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['activity'].queryset = Activities.objects.filter(school= school)
            self.fields['fee'].queryset = TypeFee.objects.filter(school=school)
        if not Activities.objects.filter(school= school):
            self.fields['activity'].empty_label = "No activities"
    
    class Meta:
        model = Student
        fields = ['name','entry_year', 'education_officer','phone_numeber_officer','activity','fee' ]

        widgets= {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'entry_year': forms.TextInput(attrs={'class':'form-control'}),
            'education_officer': forms.TextInput(attrs={'class':'form-control'}),
            'phone_numeber_officer': forms.TextInput(attrs={'class':'form-control'}),
            'activity': forms.SelectMultiple(attrs={'class':'form-control'}),
            'fee': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class TypeFeeForm(forms.ModelForm):
    class Meta:
        model = TypeFee
        fields = ['name', 'value']

        widgets ={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'value': forms.TextInput(attrs={'class':'form-control'}),
        }




class StudentAdmin(admin.ModelAdmin):
    form = StudentForm

class TypeFeeAdmin(admin.ModelAdmin):
    form = TypeFeeForm