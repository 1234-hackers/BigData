import polars as pl
import numpy as np
import seaborn as sb
from pymongo import MongoClient
from datetime import datetime

from bson.json_util import dumps, loads

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

database = client['hisani']
users_collection = database['accounts']

def try_connection():
    if client:
        print("connected")
        
    else:
        return print("error")

#try_connection()

patients = users_collection.find().limit(5)
def get_time():
    now = datetime.now()
    fmt = now.strftime("%d/%m/%Y %H:%M:%S")
    return print(fmt)


def write_json(csr):
    new = list(csr)
    json_data = dumps(new, indent = 2)
    with open('jsonData/data.json', 'w') as file:
        file.write(json_data)


write_json(patients)

get_time()