
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse





class School(models.Model):
    YEAR_CHOICES = [
        (f"{year}/{year+1}", f"{year}/{year+1}") for year in range(2024, 2034)
    ]

    name = models.CharField(max_length=100)
    scholl_year = models.CharField(max_length=9, choices=YEAR_CHOICES, default="2024/2025")


    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return self.name

class Activities(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField(validators=[MinValueValidator(0)])

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return self.name
    

    def student_count(self):
        return self.student_set.count()



class Teacher(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100,blank=True)
    class_schedule = models.CharField(max_length=100, blank=True)
    activity = models.ForeignKey(Activities, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return f"{self.name} da disciplina: {self.activity}"


