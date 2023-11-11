import json

from bson import ObjectId
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.views import get_user
from doctors.models import Slots_collection, Doctors_collection
from patients.models import Patient_collection, Appointment_collection

# Create your views here.
from patients.mongoDb_utils import replace_none_with_default, get_all_appointment, convert_array_to_serializable


def find_slots(email):
    slots = Slots_collection.find({'doctor': email}, {'date': 1, 'time': 1, '_id': 1, 'available': 1})
    return list(slots)


@api_view(['POST'])
def add_appointment(request, variable):
    user_email = get_user(request)
    user = Patient_collection.find_one({"email": user_email})
    if user:
        document_id = ObjectId(variable)
        slot = Slots_collection.find_one({'_id': document_id})
        if slot:
            if slot.get('available'):
                doctor = Doctors_collection.find_one({'email': slot.get('doctor')})
                appointment = {
                    'patient name': user.get('name'),
                    'patient': user_email,
                    'doctor_email': slot.get('doctor'),
                    'doctor_name': doctor.get('name'),
                    'time': slot.get('time'),
                    'date': slot.get('date'),
                    'is_updated': False
                }
                Appointment_collection.insert_one(appointment)
                new_value = {'$set': {'available': False}}
                slot = Slots_collection.find_one_and_update({'_id': document_id}, new_value)
                return JsonResponse({'status': 'success', 'message': 'Slot added successfully', 'data': {
                    'patient name': user.get('name'),
                    'doctor email': slot.get('doctor'),
                    'time': slot.get('time'),
                    'date': slot.get('date')
                }}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': 'Slot is not available'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
def update_appointment(request, variable):
    user_email = get_user(request)
    user = Patient_collection.find_one({"email": user_email})
    if user:
        data = json.loads(request.body.decode('utf-8'))
        document_id = ObjectId(variable)
        original_value = Appointment_collection.find_one({'_id': document_id})
        date = replace_none_with_default(data.get('date'), original_value.get('date'))
        time = replace_none_with_default(data.get('time'), original_value.get('time'))
        appointment_id = replace_none_with_default(data.get('slot_id'), original_value.get('slot_id'))
        new_value = {'$set': {'time': time, 'date': date, 'id': appointment_id}}
        appointment = Appointment_collection.find_one_and_update({'_id': document_id}, new_value)
        if appointment:
            slot_id = appointment.get('solt_id')
            new_value = {'$set': {'available': True}}
            object_id = ObjectId(slot_id)
            sol = Slots_collection.find_one_and_update({"_id": object_id}, new_value)
            print(sol)
            return JsonResponse(
                {'status': 'success', 'message': 'Appointment added successfully', 'data': {'date': date,
                                                                                            'time': time, 'doctor_name':
                                                                                                appointment.get('doctor_name')}},
                status=status.HTTP_200_OK)
        else:
            return Response({"message": "updated failed", "data": appointment}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def delete_appointment(request, variable):
    user_email = get_user(request)
    user = Patient_collection.find_one({"email": user_email})
    if user:
        document_id = ObjectId(variable)
        appointment = Appointment_collection.find_one({"_id": document_id})
        if appointment:
            if user.get('email') == appointment.get('patient'):
                Appointment_collection.delete_one({"_id": document_id})
                return JsonResponse({'status': 'success', 'message': 'Appointment deleted successfully'},
                                    status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'cant found'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_appointments(request):
    user_email = get_user(request)
    user = Patient_collection.find_one({"email": user_email})
    if user:
        appointment = get_all_appointment(user_email)
        if appointment:
            send = convert_array_to_serializable(appointment)

            return JsonResponse({'status': 'success', 'length:': len(appointment), 'data': send},
                                status=status.HTTP_200_OK)
            # print(send)
            # return Response(send)
        else:
            return JsonResponse({'status': 'success', 'length:': len(appointment), 'data': {}},
                                status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def get_slots(request):
    user_email = get_user(request)
    user = Patient_collection.find_one({"email": user_email})
    if user:
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('_id')
        document_id = ObjectId(id)
        doctor = Doctors_collection.find_one({'_id': document_id})
        # slots = Slots_collection.find({'doctor': doctor.get('email')})
        lss = find_slots(doctor.get('email'))
        print(lss)
        if lss:
            send = convert_array_to_serializable(lss)

            return JsonResponse({'status': 'success', 'data': send},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': 'success', 'length:': 0},
                                status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
