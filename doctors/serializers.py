from rest_framework import serializers
from doctors.models import Doctors_collection


class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors_collection
        fields = ('_id', 'email', 'password')
