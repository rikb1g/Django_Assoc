from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import FinanceMovements, TypeFinanceMoviment
from django.db.models.functions import TruncMonth
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView
from .forms import FinanceMovementsForm, CategoryFinanceMovimentForm



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
    
    total_expense = (FinanceMovements.objects.filter(
        Q(school = request.user.user.school),
        Q(moviment__name="expense"),
        Q(date__year=year, date__month__in=months_current_year) |
        Q(date__year=next_year, date__month__in=months_next_year)
    )
    .aggregate(total=Sum('value'))
    )
    total_income = (FinanceMovements.objects.filter(
        Q(school = request.user.user.school),
        Q(moviment__name="income"),
        Q(date__year=year, date__month__in=months_current_year) |
        Q(date__year=next_year, date__month__in=months_next_year)
    )
    .aggregate(total=Sum('value'))
    )

    summary = (total_expense['total'] if total_expense['total'] is not None else 0) - (total_income ['total'] if total_income['total'] is not None else 0 )

    context = {
        'income_per_month': income_per_month,
        'expenses_per_month': expenses_per_month,
        'total_expense' : total_expense['total'] if total_expense['total'] is not None else 0 ,
        'total_income' : total_income ['total'] if total_income['total'] is not None else 0 ,
        'summary': summary
    }

    return render(request, 'financeManagment/finance_global.html', context=context)


class FinanceMovementsIncome(CreateView):
    model = FinanceMovements
    form_class = FinanceMovementsForm
    template_name = 'financeManagment/new_income.html'
    success_url = 'finance_global'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryFinanceMovimentForm()
        return context
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['category_type'] = 'income'
        return kwargs


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        income = form.save(commit=False)
        income_type, created = TypeFinanceMoviment.objects.get_or_create(name='income')
        income.school = self.request.user.user.school
        income.moviment = income_type
        income.save()
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)
    

class FinanceMovementsExpense(CreateView):
    model = FinanceMovements
    form_class = FinanceMovementsForm
    template_name = 'financeManagment/new_expense.html'
    success_url = 'finance_global'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryFinanceMovimentForm()
        return context
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['category_type'] = 'expense'
        return kwargs

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        expense = form.save(commit=False)
        expense_type, created = TypeFinanceMoviment.objects.get_or_create(name='expense')
        expense.school = self.request.user.user.school
        expense.moviment = expense_type
        expense.save()

        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)
    


def create_category_income(request):
    if request.method == 'POST':
        form = CategoryFinanceMovimentForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.type = 'income'
            category.save()
            return  redirect('new_income')
    else:
        form = CategoryFinanceMovimentForm()

    return render(request, 'new_income.html',{'form': form})


def create_category_expense(request):
    print("aqasdasda")
    if request.method == 'POST':
        form = CategoryFinanceMovimentForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.type = 'expense'
            category.save()
            return  redirect('new_expense')
    else:
        form = CategoryFinanceMovimentForm()

    return render(request, 'new_expense.html',{'form': form})

