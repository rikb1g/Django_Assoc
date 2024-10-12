from django.urls import path
from .views import finance_global, FinanceMovementsIncome,FinanceMovementsExpense


urlpatterns = [
    path('finance_global',finance_global,name="finance_global"),
    path('finance_income_new',FinanceMovementsIncome.as_view(),name="new_income"),
    path('finance_expense_new',FinanceMovementsExpense.as_view(),name="new_expense"),
]