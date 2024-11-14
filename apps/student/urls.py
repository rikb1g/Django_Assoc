from django.urls import path
from .views import (StudentList, StudentCreate, StudentUpdate,TypeFeeCreate,student_remove, archive_student, edit_student,
                    get_all_fees,add_type_fee, update_type_fee, delete_type_fee, delete_student, month_payment_global,
                    insert_fee, remove_fee, StudentHistoric)



urlpatterns = [
    path('stutents_list',StudentList.as_view(), name='students_list'),
    path('new_student',StudentCreate.as_view(), name='new_student'),
    path('student_update/<int:student_id>/',edit_student, name='student_update'),
    path('student_Historic/',StudentHistoric.as_view(), name='student_historic'),
    path('student_remove/<int:pk>',student_remove, name='student_remove'),
    path('student_archive/<int:pk>',archive_student, name='student_archive'),
    path('student_delete/<int:pk>/',delete_student, name='student_delete'),
    path('student_fee',TypeFeeCreate.as_view(), name='new_fee_type'),
    path('all_fees/',get_all_fees, name='all_fees'),
    path('add_fee_form/',add_type_fee, name='add_fee_form'),
    path('update_type_fee/<int:pk>/',update_type_fee, name='update_type_fee'),
    path('delete_type_fee_form/<int:pk>/',delete_type_fee, name='delete_type_fee'),
    path('fees_global', month_payment_global, name='fees_global'),
    path('insert_fee/', insert_fee, name='insert_fee'),
    path('remove_fee/',remove_fee , name='remove_fee'),


]