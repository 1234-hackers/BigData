import polars as pl
import polars.selectors as cs  
import numpy as np
import seaborn as sb
from pymongo import MongoClient
from datetime import datetime

from bson.json_util import dumps, loads

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

database = client['hisani']
users_collection = database['accounts']

patients = database['patients']

def try_connection():
    if client:
        print("connected")
        
    else:
        return print("error")

#try_connection()



def get_cusor(collection_name):
    csr_found = collection_name.find().limit(20)
    return csr_found

patients = get_cusor(patients)

def get_time():
    now = datetime.now()
    fmt = now.strftime("%d/%m/%Y%H:%M:%S")
    return (now)


def write_json(csr):
    new = list(csr)
    json_data = dumps(new, indent = 2)
    de_time = get_time()
    de_time = str(de_time)
    de_time = de_time.replace("-" , "")
    de_time = de_time.replace(":" , "")
    de_time = de_time.replace("." , "")
    with open('jsonData/'+ de_time +'.json', 'w') as file:
        file.write(json_data)

#write_json(patients)


df = pl.read_json("jsonData/data.json")

#show data_types and head

print(df.head())



