from django.test import TestCase
from django.utils import timezone
from .models import TypeFinanceMoviment, CategoryFinanceMoviment,FinanceMovements
from apps.school.models import School


class FinanceMovementsTest(TestCase):
    def setUp(self) -> None:
        self.type = TypeFinanceMoviment.objects.create(name="income")
        self.cate = CategoryFinanceMoviment.objects.create(name="Despesas Gerais")
        self.school = School.objects.create(name="Ribeiro")
        self.obj = FinanceMovements.objects.create(moviment=self.type, category= self.cate, description="teste", school=self.school, date=timezone.now().date(), value= 12)


    def test_object_creation(self):
        self.assertEqual(str(self.obj), 'teste')

    def test_get_total_income(self):
        total = FinanceMovements.get_total_value_income_per_month(self.school,timezone.now().month(),timezone.now().year())
        self.assertEqual(self.obj.value, total)

    

