import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from doctors.models import Doctors_collection, Slots_collection
from rest_framework import status
from rest_framework.response import Response
from bson import ObjectId
from authentication.views import get_user

# Create your views here.
from doctors.mongoDb_utils import convert_array_to_serializable, replace_none_with_default, get_all_slots


def find_all_doctors():
    persons = Doctors_collection.find({}, {'name': 1, '_id': 1})
    print(persons)
    return list(persons)


@api_view(['GET'])
def get_all_doctors(request):
    persons = find_all_doctors()
    print(persons)
    send = convert_array_to_serializable(persons)
    return JsonResponse({'status': 'success', 'length:': len(persons), 'data': send},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def add_slot(request):
    user_email = get_user(request)
    user = Doctors_collection.find_one({"email": user_email})
    if user:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        date = data.get('date')
        time = data.get('time')
        slot = {
            'date': date,
            'time': time,
            'doctor': user_email,
            'available': True
        }
        Slots_collection.insert_one(slot)

        return JsonResponse({'status': 'success', 'message': 'Slot added successfully', 'data': {'date': date,
                                                                                                 'time': time,
                                                                                                 'doctor': user_email}},
                            status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
def update_slot(request, variable):
    user_email = get_user(request)
    user = Doctors_collection.find_one({"email": user_email})
    if user:
        data = json.loads(request.body.decode('utf-8'))
        document_id = ObjectId(variable)
        original_value = Slots_collection.find_one({'_id': document_id})
        print(original_value)
        date = replace_none_with_default(data.get('date'), original_value.get('date'))
        time = replace_none_with_default(data.get('time'), original_value.get('time'))
        available = replace_none_with_default(data.get('available'), original_value.get('available'))

        new_value = {'$set': {'time': time, 'date': date, 'available': available}}
        slot = Slots_collection.find_one_and_update({'_id': document_id}, new_value)

        if slot:
            return JsonResponse({'status': 'success', 'message': 'Slot added successfully', 'data': {'date': date,
                                                                                                     'time': time}},
                                status=status.HTTP_200_OK)
        else:
            return Response({"message": "updated failed", "data": slot}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def delete_slot(request, variable):
    user_email = get_user(request)
    user = Doctors_collection.find_one({"email": user_email})
    if user:
        document_id = ObjectId(variable)
        slot = Slots_collection.find_one({"_id": document_id})
        if slot:
            if user.get('email') == slot.get('doctor'):
                Slots_collection.delete_one({"_id": document_id})
                return JsonResponse({'status': 'success', 'message': 'Slot deleted successfully'},
                                    status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'cant found'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_slots(request):
    user_email = get_user(request)
    user = Doctors_collection.find_one({"email": user_email})
    print(user)
    if user:
        slots = get_all_slots(user_email)
        if slots:
            send = convert_array_to_serializable(slots)

            return JsonResponse({'status': 'success', 'length:': len(slots), 'data': send},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': 'success', 'length:': 0},
                                status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
