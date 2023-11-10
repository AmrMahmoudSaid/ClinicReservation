from django.db import models
from db_connection import db


# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    confirmed_password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)


Patient_collection = db['patient']
Appointment_collection = db['appointment']


