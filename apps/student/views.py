from typing import Any
from django.db.models.query import QuerySet
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView
from .models import Student, TypeFee
from .forms import StudentForm, TypeFeeForm
from apps.school.models import Activities



class StudentList(ListView):
    model = Student
    context_object_name = 'students_list'

    def post(self,request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('students_list')
    
    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        context['activities'] = Activities.objects.all()
        print(context)
        return context

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('query_students')
        school = self.request.user.user.school

        if query:
            return Student.objects.filter(name__icontains=query, school=school,active=True)

        if school:
            return Student.objects.filter(school=school, active=True)
        
class StudentHistoric(ListView):
    model = Student
    context_object_name = 'historic_students_list'

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('query_students')
        school = self.request.user.user.school

        if query:
            return Student.objects.filter(name__icontains=query, school=school,active=False)

        if school:
            return Student.objects.filter(school=school, active=False)
    
    
        
    
class StudentCreate(CreateView):
    model = Student
    form_class = StudentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.user.school
        return kwargs
    
    def form_valid(self, form):
        student = form.save(commit=False)
        student.school = self.request.user.user.school
        student.save()
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class StudentUpdate(CreateView):
    model = Student
    form_class = StudentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.user.school
        return kwargs
    
class TypeFeeCreate(CreateView):
    model = TypeFee
    form_class = TypeFeeForm
    

    def form_valid(self, form):
        fee = form.save(commit=False)
        fee.school = self.request.user.user.school
        fee.save()

        return super().form_valid(form)
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



    
def student_remove(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('students_list')

def archive_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.active = False
    student.save()
    return redirect('students_list')

@require_http_methods(['GET', 'POST'])
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        print(form)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    student_data = {
        'name': student.name,
        'entry_year': student.entry_year,
        'out_year': student.out_year,
        'education_officer': student.education_officer,
        'phone_numeber_officer': student.phone_numeber_officer,
        'activity': list(student.activity.values_list('id', flat=True)),
        'fee': list(student.fee.values_list('id', flat=True)),
    }

    return JsonResponse(student_data)

@require_http_methods(['GET', 'POST'])
def edit_type_fee(request, fee_id):
    fee = get_object_or_404(TypeFee, id=fee_id)

    if request.method == 'POST':
        form = TypeFeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    fee_data = {
        'name': fee.name,
    }

    return JsonResponse(fee_data)

def get_all_fees(request):
    fees = TypeFee.objects.all().values('id', 'name')
    return JsonResponse(list(fees), safe=False)


        


    
