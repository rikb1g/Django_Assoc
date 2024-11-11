from django.urls import path
from .views import finance_global, FinanceMovementsIncome,FinanceMovementsExpense, create_category_expense, create_category_income, finance_moviments_list,UptadeMovementFinancer,delete_movements


urlpatterns = [
    path('finance_global',finance_global,name="finance_global"),
    path('finance_income_new',FinanceMovementsIncome.as_view(),name="new_income"),
    path('finance_expense_new',FinanceMovementsExpense.as_view(),name="new_expense"),
    path('create_category_expense',create_category_expense,name="create_category_expense"),
    path('create_category_income',create_category_income,name="create_category_income"),
    path('finance_moviments_list',finance_moviments_list,name="finance_moviments_list"),
    path('UptadeMovementFinancer/<int:pk>/',UptadeMovementFinancer.as_view(),name="uptadeMovementFinancer"),
    path('delete_movements/<int:id>/',delete_movements,name="delete_movements"),
]