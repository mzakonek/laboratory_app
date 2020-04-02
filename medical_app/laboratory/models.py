from django.db import models
from users.models import User
from django.utils import timezone


class Parameter(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, related_name='surveys', on_delete=models.CASCADE)
    parameters = models.ManyToManyField(Parameter, blank=True, related_name="surveys_assigned")

    def __str__(self):
        return self.name


