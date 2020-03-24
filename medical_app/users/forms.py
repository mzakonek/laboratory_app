from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Patient, Specialist, GENDER_CHOICES
import datetime as dt

YEARS = [x for x in range(1940, dt.datetime.now().year)]


class SpecialistSignUpForm(UserCreationForm):
    employee_code = forms.CharField(label="Enter your employee code to continue")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_specialist = True
        user.save()
        specialist = Specialist.objects.create(user=user)

        specialist.employee_code = self.cleaned_data.get("employee_code")

        return user


class PatientSignUpForm(UserCreationForm):
    weight = forms.IntegerField(min_value=0)
    height = forms.IntegerField(min_value=0)
    date_of_birth = forms.DateField(
        label='What is your birth date?',
        initial="1990-06-21",
        widget=forms.SelectDateWidget(years=YEARS)
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(
            user=user,
            date_of_birth=self.cleaned_data.get("date_of_birth"),
            height=self.cleaned_data.get("height"),
            weight=self.cleaned_data.get("weight"),
            gender=self.cleaned_data.get("gender")
        )

        return user
