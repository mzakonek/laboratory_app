from django.contrib import admin
from django.urls import include, path

from users.views import users_laboratory, users_patients, users_specialists  # authentication views

urlpatterns = [
    path('', include('laboratory.urls')),  # domain views
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', users_laboratory.SignUpView.as_view(), name='signup'),
    path('accounts/signup/patient/', users_patients.PatientSignUpView.as_view(), name='patient_signup'),
    path('accounts/signup/teacher/', users_specialists.SpecialistSignUpView.as_view(), name='specialist_signup'),

    path('admin/', admin.site.urls),

]

