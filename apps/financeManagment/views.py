from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import FinanceMovements, TypeFinanceMoviment
from django.db.models.functions import TruncMonth
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView
from .forms import FinanceMovementsForm



def finance_global(request):
    school_year = request.user.user.school.scholl_year
    list_year = school_year.split('/')
    year = list_year[0]
    next_year = list_year[1]
    

    months_current_year = [x for x in range(9,13)]
    months_next_year = [x for x in range(1,9)]

    income_per_month = (
        FinanceMovements.objects.filter(
            Q(school=request.user.user.school),
            Q(moviment__name="income"),
            Q(date__year=year, date__month__in=months_current_year) |
            Q(date__year=next_year, date__month__in=months_next_year)
        )
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('value'))
        .order_by('month')
    )

    expenses_per_month = (
        FinanceMovements.objects.filter(
            Q(school=request.user.user.school),
            Q(moviment__name="expense"),
            Q(date__year=year, date__month__in=months_current_year) |
            Q(date__year=next_year, date__month__in=months_next_year)
        )
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('value'))
        .order_by('month')
    )

    context = {
        'income_per_month': income_per_month,
        'expenses_per_month': expenses_per_month,
    }

    return render(request, 'financeManagment/finance_global.html', context=context)


class FinanceMovementsIncome(CreateView):
    model = FinanceMovements
    form_class = FinanceMovementsForm
    template_name = 'financeManagment/new_income.html'
    success_url = 'finance_global'


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        income = form.save(commit=False)
        try:
            income.moviment = 'income'
            income.save()
        except:
            TypeFinanceMoviment.objects.create(name='income')
            income.moviment = 'income'
            income.save()
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)
    

class FinanceMovementsExpense(CreateView):
    model = FinanceMovements
    form_class = FinanceMovementsForm
    template_name = 'financeManagment/new_expense.html'
    success_url = 'finance_global'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        expense = form.save(commit=False)
        try:
            expense.moviment = 'expense'
            expense.save()
        except:
            TypeFinanceMoviment.objects.create(name='expense')
            expense.moviment = 'expense'
            expense.save()

        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)

