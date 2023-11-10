from django.urls import path
from doctors.views import get_all_doctors, add_slot, update_slot, delete_slot, get_slots

urlpatterns = [
    path('', get_all_doctors),
    path('slot', add_slot),
    path('slots', get_slots),
    path('slot/<str:variable>', update_slot),
    path('slot/delete/<str:variable>', delete_slot),
]