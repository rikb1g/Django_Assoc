from django import forms
from django.contrib import admin
from .models import School, Activities, Teacher




class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }


class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = ['name', 'value']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'value': forms.TextInput(attrs={'class':'form-control'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name','phone', 'email', 'class_schedule','activity' ]

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'class_schedule': forms.TextInput(attrs={'class':'form-control'}),
            'activity': forms.Select(attrs={'class':'form-control'}),
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activity'].required = True


class SchoolAdmin(admin.ModelAdmin):
    form = SchoolForm

class ActivitiesAdmin(admin.ModelAdmin):
    form = ActivitiesForm

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm