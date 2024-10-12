from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from scholmanagment import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.core.urls'),name="home"),
    path("accounts/", include("django.contrib.auth.urls"),name="login"),
    path("school/", include("apps.school.urls"),name="school"),
    path("student/", include("apps.student.urls"),name="student"),
    #path("user/", include("apps.user.urls"),name="user"),
    #path("employees/", include("apps.employees.urls"),name="employees"),
    path("finance/", include("apps.financeManagment.urls"),name="finance"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
