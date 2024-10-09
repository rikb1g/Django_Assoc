from django.urls import path
from .views import ActivitiesCreate, TeacherCreate, school_manager, get_all_activities, edit_activity, add_activity, delete_activity


urlpatterns = [
    path('activities', ActivitiesCreate.as_view(), name='activities_new'),
    path('teachers', TeacherCreate.as_view(), name='teachers_new'),
    path('school_manager', school_manager, name='school_manager'),
    path('all_activities/', get_all_activities, name='all_activities'),
    path('edit_activity/<int:activity_id>/', edit_activity, name='edit_activite'),
    path('addactivityform/', add_activity, name='add_activite'),
    path('delete_activity/<int:pk>/', delete_activity, name='delete_activity'),
]