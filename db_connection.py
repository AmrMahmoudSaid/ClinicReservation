import pymongo

url = 'mongodb+srv://AmrMahmoud:amr.mahmoud@cluster0.exwcjr4.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(url)

db = client['clinic_reservation']