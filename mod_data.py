


from pymongo import MongoClient
from datetime import datetime

from bson.json_util import dumps, loads
import re

from matplotlib import pyplot as plt
import subprocess

from functools import wraps

import random
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
database = client['hisani']
database2 = client['hisani_accounts']
users_collection = database['accounts']
patients = database['patients']
transactions = database['transactions']
accounts = database['accounts']
diag = database['diagnoses']
beds = database['beds']
ilt = database['inventoryledgerentries']
pP = database['patientplans']



def update_data_column(col):

    all_documents = col.find().limit(10)
    for x in all_documents:
        k = x['_id']
        randzz = random.randint(145346 , 976578)
        col.find_one_and_update({"_id" :k} , { '$set' : {"password" : randzz} })
    all_documents2 = col.find().limit(10)
    for n in all_documents2:   
        print(n)
update_data_column(beds)