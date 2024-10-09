from django.db import models
from django.contrib.auth.models import User
from apps.school.models import School


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True)
    school = models.OneToOneField(School,on_delete=models.CASCADE)

    def __str__(self):
        return self.username


