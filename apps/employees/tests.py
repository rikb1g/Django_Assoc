from django.test import TestCase
from django.utils import timezone
from .models import Employee, TableIRS
from apps.school.models import School






class EmployeeTest(TestCase):
    def setUp(self) -> None:
        self.table = TableIRS.objects.create(name="Solteiro", tax=0.00)
        self.school = School.objects.create(name="Ribeiro")

        self.obj = Employee.objects.create(name="TEste",salary=420,Irs=self.table, school= self.school, start_date=timezone.now().date())

    def test_object_creation(self):
        self.assertEqual(str(self.obj),'TEste')
