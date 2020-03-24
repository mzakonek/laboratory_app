from django.contrib import admin
from .models import User, Patient, Specialist

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Specialist)
