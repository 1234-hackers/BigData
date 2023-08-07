import pandas as pd 
import numpy as np
import seaborn as sb
from pymongo import MongoClient
from datetime import datetime

from bson.json_util import dumps, loads
import re

from matplotlib import pyplot as plt

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

database = client['hisani']

database2 = client['hisani_accounts']


f = database2['latest']



users_collection = database['accounts']
patients = database['patients']
transactions = database['transactions']

def try_connection():
    if client:
        print("connected")
        
    else:
        return print("error")
#try_connection()



def get_cusor(collection_name):
    csr_found = collection_name.find().limit(20)
    return csr_found

collection_data = get_cusor(transactions)

def get_time():
    now = datetime.now()
    fmt = now.strftime("%d/%m/%Y%H:%M:%S")
    return (now)

#de_time = get_time()
#print(de_time)
def write_json(csr_found):
    new = list(csr_found)
    json_data = dumps(new, indent = 2)
    de_time = get_time()
    de_time = str(de_time)
    de_time = de_time.replace("-" , "")
    de_time = de_time.replace(":" , "")
    de_time = de_time.replace("." , "")
    with open('jsonData/'+ de_time +'.json', 'w') as file:
        file.write(json_data)

#write_json(collection_data)

#pandas
def patient_data_analysis():
    df = pd.read_json("jsonData/patient/20230613 185207779305.json")

    #getting keys of the data
    dts = df.columns
    #print(dts)

    def add_age():
                age = df['dob']
                
                xc = []
                xc2 = []
                age_now = []
                for x in age:
                    xc.append(x)
                for k in xc:
                    birth = str(k['$date'])
                    birthx=birth[0:4]
                    try:
                        de_time = str(get_time())
                        the_year = de_time[0:4]
                        age = int(the_year) - int(birthx)
                    except ValueError:
                        age2 = df['date']
                        for k in age2:
                            xc2.append(k)
                        for d in xc2:
                            adm = str(d['$date'])
                        de_time = str(get_time())
                        the_year = de_time[0:4]
                        admited = adm[0:4]
                        age = int(the_year) - int(admited)
                        age_now.append(str(age))
                        
                    else:
                        age_now.append(str(age))

                
                print(age_now)
                df['age'] = age_now
                print(df.columns)
    #add_age()
    # age = df['dob']
    # xc = []
    # for x in age:
    #     xc.append(x)
    # for k in xc:
    #     birth = str(k['$date'])
    #     birthx=birth[0:4]
    #     try:
    #         de_time = str(get_time())
    #         the_year = de_time[0:4]
    #         age = int(the_year) - int(birthx)
    #     except ValueError:
    #         age = "NA"
    #     else:
    #         print("Born" + str(birthx) + "Age " + str(age))
    #         print(age)
        
    

    #print(age)

    #print(df[['name' , 'gender']])


    #get a specific column
    #print(df['name'])

    #get multiple colums
    #print(df[['name' , 'gender']])

    #getting all documents

    def get_docs():
        for index , row in df.iterrows():
            print(index , row)


    # #filtering data based on specific feilds
    # sort = df.loc[(df['gender'] =="Female") & (df['nokRShip'].str.contains('father|mum' , flags=re.I,regex=True))]

    # #filtering based on how words starts
    # sort1 = df.loc[(df['name'].str.contains('ja[a-z]*',flags=re.I,regex=True)) & (df['gender'].str.contains('female|male' , flags=re.I,regex=True))]



    # print(sort1[['name' , 'gender' ,'nokRShip' ,'dob','doesntKnowDOB','opNo','ipNo']])

    #print(all_m.describe())
#patient_data_analysis()

def transactions_data():
    df = pd.read_json("jsonData/20230615 194837504100.json")
    dts = df.columns

    for n in dts:
        print(n)

    amounts = df['method']

    sort = df.loc[(df['method'] =="M-Pesa")]

    #print(sort)
    def draw_now():
        graph = distplot(sort, kde=False)
        graph.show()
        
    draw_now()

    print()
    
#transactions_data()



def draw():
    graph = distplot(sort, kde=False)
    graph.show()

def generate_data(col):
    def try_connection():
        if client:
            return "connected"
        else:
            return "error"
    def get_time():
        now = datetime.now()
        fmt = now.strftime("%d/%m/%Y%H:%M:%S")
        return (now)
    csr_found = col.find().limit(20)
    
    def write_json(csr_found):
        cond = try_connection()
        if cond == "connected":
            new = list(csr_found)
            json_data = dumps(new, indent = 2)
            de_time = get_time()
            de_time = str(de_time)
            de_time = de_time.replace("-" , "")
            de_time = de_time.replace(":" , "")
            de_time = de_time.replace("." , "")
            with open('jsonData/'+ de_time +'.json', 'w') as file:
                file.write(json_data)
                file.close()
            return print("New Data Collected. Upload Latest File For Analysis")

        if cond == "error":
                return print("Could Not Connect To Database")
    write_json(csr_found)

#generate_data(col)



def find_docs():
    patient = "patients"
    docs = f.find({"coll" : patient})
    if docs:
        for x in docs:
            print(x)
    else:
        print("Noin")
find_docs()