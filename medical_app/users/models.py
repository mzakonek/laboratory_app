from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_specialist = models.BooleanField(default=False)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateTimeField()
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_code = models.CharField(max_length=10)
