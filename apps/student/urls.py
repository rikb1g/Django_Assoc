from django.urls import path
from .views import StudentList, StudentCreate, StudentUpdate,TypeFeeCreate,student_remove, archive_student, edit_student, get_all_fees,edit_type_fee



urlpatterns = [
    path('stutents_list',StudentList.as_view(), name='students_list'),
    path('new_student',StudentCreate.as_view(), name='new_student'),
    path('student_update/<int:student_id>/',edit_student, name='student_update'),
    path('edit_type_fee/<int:student_id>/',edit_type_fee, name='edit_type_fee'),
    path('student_remove/<int:pk>',student_remove, name='student_remove'),
    path('student_archive/<int:pk>',archive_student, name='student_archive'),
    path('student_fee',TypeFeeCreate.as_view(), name='new_fee_type'),
    path('all_fees/',get_all_fees, name='all_fees'),
]