from django.urls import path
from .views import ActivitiesCreate, TeacherCreate, school_manager, get_all_activities, edit_activity, add_activity, delete_activity,delete_teacher, add_teacher, update_teacher


urlpatterns = [
    path('activities', ActivitiesCreate.as_view(), name='activities_new'),
    path('teachers', TeacherCreate.as_view(), name='teachers_new'),
    path('school_manager', school_manager, name='school_manager'),
    path('all_activities/', get_all_activities, name='all_activities'),
    path('edit_activity/<int:activity_id>/', edit_activity, name='edit_activite'),
    path('update_teacher/<int:teacher_id>/', update_teacher, name='uptate_teacher'),
    path('addactivityform/', add_activity, name='add_activity_form'),
    path('addTeacherForm/', add_teacher, name='add_teacher_form'),
    path('delete_activity/<int:pk>/', delete_activity, name='delete_activity'),
    path('delete_teacher/<int:pk>/', delete_teacher, name='delete_teacher'),
]