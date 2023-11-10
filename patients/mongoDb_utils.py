from bson import ObjectId

from doctors.models import Slots_collection
from patients.models import Appointment_collection


def get_all_appointment(email):
    Appointment = Appointment_collection.find({'patient': email})
    return list(Appointment)


def convert_to_serializable(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, str):
        return obj
    else:
        return obj


def convert_array_to_serializable(array):
    for item in array:
        for key, value in item.items():
            item[key] = convert_to_serializable(value)
    return array


replace_none_with_default = lambda value, default: default if value is None else value
