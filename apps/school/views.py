from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import  CreateView, UpdateView
from django.views.decorators.http import require_http_methods

from .models import Activities, Teacher
from .forms import ActivitiesForm, TeacherForm
from apps.student.models import TypeFee


class ActivitiesCreate(CreateView):
    model = Activities
    form_class = ActivitiesForm


    def form_valid(self, form):
        activitie = form.save(commit=False)
        activitie.school = self.request.user.user.school
        activitie.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class TeacherCreate(CreateView):
    model = Teacher
    form_class = TeacherForm

    def form_valid(self, form):
        teacher = form.save(commit=False)
        teacher.school = self.request.user.user.school
        teacher.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
def activitie_delete(request, pk):
    activitie = get_object_or_404(Activities, pk=pk)
    activitie.delete()
    return redirect('home')

def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('home')

def school_manager(request):
    data= {}
    data['school'] = request.user.user.school.name
    data['activities'] = Activities.objects.filter(school=request.user.user.school)
    data['teachers'] = Teacher.objects.filter(school=request.user.user.school)
    data['fees'] = TypeFee.objects.filter(school=request.user.user.school)

    data['edit_activity_form'] = ActivitiesForm
    data['edit_teacher_form'] = TeacherForm



    return render(request, 'school/school_manager.html', context=data)

def get_all_activities(request):
    activities = Activities.objects.all().values('id', 'name')
    return JsonResponse(list(activities), safe=False)


@require_http_methods(['GET', 'POST'])
def edit_activity(request, activity_id):
    activitie = get_object_or_404(Activities, id=activity_id)
    if request.method == 'POST':
        form = ActivitiesForm(request.POST, instance=activitie)
        for a in form:
            print(a)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    

    activitie_data = {
        'name': activitie.name,
        'value': activitie.value
    }

    return JsonResponse(activitie_data)

@require_http_methods(['GET', 'POST'])
def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    print(teacher)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    teacher_data = {
        'name': teacher.name,
        'phone': teacher.phone,
        'email': teacher.email,
        'class_schedule': teacher.class_schedule,
        'activity': teacher.activity.id,  
    }
    return JsonResponse(teacher_data)



def add_activity(request):
    form = ActivitiesForm(request.POST)
    form.instance.school = request.user.user.school
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
def add_teacher(request):
    form = TeacherForm(request.POST)
    form.instance.school = request.user.user.school
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def delete_activity(request, pk):
    activity = get_object_or_404(Activities, pk=pk)
    if activity:
        activity.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)
    
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if teacher:
        teacher.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)
    

    
