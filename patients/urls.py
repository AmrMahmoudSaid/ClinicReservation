from django.urls import path
from patients.views import add_appointment, delete_appointment, update_appointment, get_appointments

urlpatterns = [
    path('appointment', get_appointments),
    path('appointment/slot/<str:variable>', add_appointment),
    path('appointment/<str:variable>', update_appointment),
    path('appointment/delete/<str:variable>', delete_appointment),
]