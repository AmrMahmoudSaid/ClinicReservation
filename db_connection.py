import os

import pymongo
from decouple import config

url = 'mongodb+srv://AmrMahmoud:amr.mahmoud@cluster0.exwcjr4.mongodb.net/?retryWrites=true&w=majority'
# url = os.environ.get('MONGO_URL')

client = pymongo.MongoClient(url)

db = client['clinic_reservation']