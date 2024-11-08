import json
from django.db.models.query import QuerySet
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Student, TypeFee,MonthlyPayment
from .forms import StudentForm, TypeFeeForm
from apps.financeManagment.models import FinanceMovements, CategoryFinanceMoviment, TypeFinanceMoviment
from apps.school.models import Activities
from datetime import datetime



class StudentList(ListView):
    model = Student
    context_object_name = 'students_list'

    def post(self,request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('students_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activities.objects.all()
        print(context)
        return context

    def get_queryset(self):
        query = self.request.GET.get('query_students')
        school = self.request.user.user.school

        if query:
            return Student.objects.filter(name__icontains=query, school=school,active=True)

        if school:
            return Student.objects.filter(school=school, active=True)
        
class StudentHistoric(ListView):
    model = Student
    context_object_name = 'historic_students_list'

    def get_queryset(self):
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
        FinanceMovements.objects.creat()
        
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



def get_all_fees(request):
    fees = TypeFee.objects.all().values('id', 'name')
    return JsonResponse(list(fees), safe=False)



@require_http_methods(['GET', 'POST'])
def update_type_fee(request, pk):
    fee = get_object_or_404(TypeFee, pk=pk)
    form = TypeFeeForm(request.POST, instance=fee)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    type_fee_data = {
        'name': fee.name,
        'value': fee.value,
    }

    return JsonResponse(type_fee_data)
 
def add_type_fee(request):
    form = TypeFeeForm(request.POST)
    form.instance.school = request.user.user.school
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    

def delete_type_fee(request, pk):
    fee = get_object_or_404(TypeFee, pk=pk)
    if fee:
        fee.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)
    

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if student:
        student.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)
    

# Montly PAyment
    
def month_payment_global(request):
    school_year = request.user.user.school.scholl_year
    list_year = school_year.split('/')
    year = list_year[0]
    next_year = list_year[1]
    current_month = datetime.now().strftime("%B")
    print(current_month)


    

    months_current_year = [x for x in range(9,13)]
    months_next_year = [x for x in range(1,9)]


    payment_fee_per_month = (
        MonthlyPayment.objects.filter(
            Q(school= request.user.user.school),
            Q(payment_date__year= year,payment_date__month__in=months_current_year) |
            Q(payment_date__year=next_year,payment_date__month__in=months_next_year)
        )    
    )

    context = {
        'payment_fee_per_month': payment_fee_per_month,
        'school_year': list_year[0],
        'school_year_next': list_year[1],
        'current_month': current_month,
    }
    return render(request, 'student/monthly_payment.html',context=context)


def insert_fee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fee_id = data.get('id')
            value_fee = data.get('value')
            print(fee_id)
            print(value_fee)
    
            # Buscar e atualizar o pagamento da mensalidade
            fee = MonthlyPayment.objects.get(id=fee_id)
            fee.isPaid = True
            fee.value = value_fee
            fee.save()
            
        
            category_type, _ = CategoryFinanceMoviment.objects.get_or_create(name='mensalidades',type='income')    
            moviment_type, _ = TypeFinanceMoviment.objects.get_or_create(name='income')
            

            # Criar o movimento financeiro
            try:
                finance_moviment_exist = FinanceMovements.objects.get(description=f"{fee_id},{fee.student},{fee.payment_date}")
                print(finance_moviment_exist)

                finance_moviment_exist.value = fee.value
                finance_moviment_exist.save()
                print("salvou")

            except FinanceMovements.DoesNotExist:
                print("deu erro")
                finance = FinanceMovements.objects.create(
                    moviment= moviment_type,
                    category= category_type,   
                    description=f"{fee_id},{fee.student},{fee.payment_date}",
                    date = fee.payment_date,
                    value=value_fee,
                    school= fee.school,
                )
                finance.save()
                return JsonResponse({'success': True})        
                
            except Exception as e:
                print(e)
                return JsonResponse({'success': False, 'error': 'Erro ao criar movimento financeiro'})
            
            return JsonResponse({'success': True})
        
        except MonthlyPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mensalidade não encontrada'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método não permitido.'})


def remove_fee(request):
    if request.method == 'POST':
        try:
            data= json.loads(request.body)
            fee_id = data.get('id')
            fee = MonthlyPayment.objects.get(id=fee_id)
            fee.value = ""
            fee.isPaid = False
            fee.save()

            try: 
                finance = FinanceMovements.objects.get(description=f"{fee_id},{fee.student},{fee.payment_date}")
                if finance:
                    finance.delete()
                    return JsonResponse({'success': True})
            except FinanceMovements.DoesNotExist:
                return JsonResponse({'success': True})


        except MonthlyPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mensalidade não existe'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido.'})


        


    

    
