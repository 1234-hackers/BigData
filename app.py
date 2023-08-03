import streamlit as st
from matplotlib import pyplot as plt
import plotly.express as pE
# Your imports goes below

import pandas as pd 
import numpy as np
import seaborn as sb
from pymongo import MongoClient
from datetime import datetime


from PIL import Image

from bson.json_util import dumps, loads
import re

from matplotlib import pyplot as plt
import subprocess

from flask import session
from passlib.hash import  scram
from functools import wraps

from streamlit_option_menu import option_menu
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
QueEnt = database['queueentries']


container = st.container()
sidebar = st.sidebar

def register_now():
    st.container()
    st.write("Register Now ")
    de_username = st.text_input("Username" , key="reg")
    password = st.text_input("password")
    users_ = database2['accounts']
    debz = st.button("Register")
    if debz:
        existing_user =  users_.find_one({"username":de_username})
        if existing_user:
            login()
        else:
            passcode = scram.hash(password)
            users_.insert_one({"username":de_username , "password": passcode})


months = ['Jan' , 'Feb' , 'March' , 'April', 'May','June' ,'July','Aug','Sep','Oct','Nov','Dec']

em_collections = database.list_collection_names()

def top_menu():
        de_menuz = option_menu(
            menu_title = "Main Menu",
            options=['Data Analysis' , 'Data Visualization','Update Data'],
            icons = ['math','chart','clock'],
            menu_icon = "cast",
            orientation = "verticle"
            )
    
        return de_menuz



def create_chart(crt,data,x_axis,y_axix):
        container.write("Data Visualization")
        
        if crt == "Bar":
            st.header("Bar Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.bar(data,x=x_axis,y=y_axix,color=x_axis , barmode="group") 
            st.bar_chart(data[['gender','locality']])
            st.plotly_chart(figure)

        

        if crt == "Line":
            st.header("Line Graph Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.line(data,x=x_axis,y=y_axix )
            st.area_chart(data[['locality','gender']])
            st.plotly_chart(figure)
            
        if crt == "Histogram":
            st.header("Histogram")
            figure = pE.histogram(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)

        if crt == "Scatter_Chart":
            st.header("Scatter Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.scatter(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)
        
        if crt == "Pie_Chart":
            st.header("Pie Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.pie(data,values='locality' , names='gender' )
            st.plotly_chart(figure)   
def data_visual(data):
    #st.sidebar("Select Graph Type")
    crt = st.sidebar.selectbox("Chart Type",['Pie_Chart', 'Histogram','Bar','Line','Scatter_Chart'])
    x_axis = st.sidebar.selectbox("Select X axis" , data.columns)
    y_axix = st.sidebar.selectbox("Select Y Axis",data.columns)
    create_chart(crt,data,x_axis,y_axix)


import time
def generate_data(col,folder):
    st.write("Fetch latest Data For Analysis For " + str(folder[9:]))
    def try_connection():
        if client:
            return "connected"
        else:
            return "error"
    def get_time():
        now = datetime.now()
        fmt = now.strftime("%d/%m/%Y%H:%M:%S")
        return (now)
    csr_found = col.find().limit(100)
    
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
            with open(folder + de_time +'.json', 'w') as file:
                file.write(json_data)
                file.close()
            bar = st.progress(0,"COllecting Data..."  )
            for x in range(100):
                time.sleep(0.1)
                bar.progress(x + 1,"COllecting Data...")
            return st.success("New Data Collected. Upload Latest File For Analysis")

        if cond == "error":
                return st.warning("Could Not Connect To Database")
    


    prompt = st.button("Update Data" , key="update_data" )
    if prompt:
        write_json(csr_found)
    else:
        pass


def take_date():
    age = st.slidebar("Select An Age  Set" ,0,50)
    date = st.date_input("Select Date")
#reusable sorting and filter functions returning a dataframe
def sort_data(data_frm):
        sec = data_frm.columns[::-1]
        p = data_frm.columns[1:9]
        rand = np.random.permutation(sec)
        sort_param1 = st.sidebar.selectbox("Sort By", data_frm.columns)
        sort_param2 = st.sidebar.selectbox("Second Key", sec , key="ghfgh")
        sort_param3 = st.sidebar.selectbox("Aditional Key", p , key="ghfgfgh")
       
        data_new = data_frm[[sort_param1 , sort_param2 , sort_param3]]
        return data_new

def group_by_mean(data_frm):
    group_c = st.sidebar.selectbox("Group By Mean" , data_frm.columns)
    grouped_by_mean = data_frm.groupbyb(group_c).mean()
    return grouped_by_mean

def get_time():
    now = datetime.now()
    fmt = now.strftime("%d/%m/%Y%H:%M:%S")
    return (now)

#defferent pages
#@login_required
def patients_col():
    col = patients
    folder ='jsonData/patient/' 
    to_read = None
    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    # options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization','Update Data'])
    defau = "jsonData/patient/20230621 124514893477.json"
    if to_read is None:
        to_read = defau
    def top_menu():
        de_menuz = option_menu(
            menu_title = None,
            options=['Data Analysis' , 'Data Visualization','Update Data'],
            icons = ['math','chart','clock'],
            menu_icon = "cast",
            orientation = "verticle"
            )
        
        return de_menuz
    with st.sidebar:
        de_menu = top_menu()
    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Sort_Data'])
        container.write("# Data Analysis")
        if to_view == 'Sort_Data':
            age = data['dob']
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
                    age2 = data['date']
                    for k in age2:
                        xc2.append(k)
                    for d in xc2:
                        adm = str(d['$date'])
                    de_time = str(get_time())
                    the_year = de_time[0:4]
                    admited = adm[0:4]
                    age = int(the_year) - int(admited)
                    age_now.append(int(age))
                        
                else:
                    age_now.append(int(age))
    

            data['age']=age_now
            range_age1 = st.slider("Sort By Age" , min_value=1,max_value=100 , value=(1,100))
            st.info("Current Age Set " + str(range_age1))
            gen = list(data['gender'])
            
            range_age = []
            for x in range_age1:
                v = int(x)
                range_age.append(v)
            f_params = st.selectbox("Sort By",['age','region','gender','county','locality','country'])
            gen2 = list(data[f_params].unique())
            g = []
            for x in gen2:
                if gen2.count(x) > 1:
                    if not x in g:
                        g.append(x)
                else:
                    if not x in g:
                        g.append(x)
            keyz = st.selectbox("parameter" ,g)
            found = data.loc[(data[f_params] ==keyz) & (data['age'] > range_age[0]) & (data['age'] < range_age[1])]
            

            container.write(found[['name','dob','gender','age','county','locality','country','phone']])
            container.success("Number Of Results  " + str(found.shape[0]))
            
        
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
    def create_chart(crt,data,x_axis,y_axix):
        container.write("Data Visualization")
        
        if crt == "Bar":
            st.header("Bar Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.bar(data,x=x_axis,y=y_axix,color=x_axis , barmode="group") 
            st.bar_chart(data[['gender','locality']])
            st.plotly_chart(figure)

        

        if crt == "Line":
            st.header("Line Graph Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.line(data,x=x_axis,y=y_axix )
            st.area_chart(data[['locality','gender']])
            st.plotly_chart(figure)
            
        if crt == "Histogram":
            st.header("Histogram")
            figure = pE.histogram(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)

        if crt == "Scatter_Chart":
            st.header("Scatter Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.scatter(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)
        
        if crt == "Pie_Chart":
            st.header("Pie Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.pie(data,values='locality' , names='gender' )
            st.plotly_chart(figure)
    def data_visual(data):
        #st.sidebar("Select Graph Type")
        age = data['dob']
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
                age2 = data['date']
                for k in age2:
                    xc2.append(k)
                for d in xc2:
                    adm = str(d['$date'])
                de_time = str(get_time())
                the_year = de_time[0:4]
                admited = adm[0:4]
                age = int(the_year) - int(admited)
                age_now.append(int(age))
                        
            else:
                age_now.append(int(age))
    

        data['age']=age_now
        crt = st.sidebar.selectbox("Chart Type",['Bar','Line','Scatter_Chart'])
        x_axis = st.sidebar.selectbox("Select X axis" , ['age','region','gender','county','locality','country'])
        y_axix = st.sidebar.selectbox("Select Y Axis",['gender','age','region','county','locality','country'])
        create_chart(crt,data,x_axis,y_axix)

    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        


    if to_read is not None:
            data = pd.read_json(to_read)
            if  de_menu == 'Data Analysis':
                analyze(data)
            if de_menu == 'Data Visualization':
                data_visual(data)
            
            if de_menu == 'Update Data':
                generate_data(col,folder)
        

def transactions_col():
    col = transactions
    folder ='jsonData/transactions/'
    to_read = None
    defau = "jsonData/transactions/20230626 131506324764.json"

    
    with st.sidebar:
        de_menu = top_menu()    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    if to_read is None:
        to_read = defau

    
    def group_by_sum(data_frm):
        months2 = []
        for x in range(1,13):
            str(x)
            months2.append(x)

        group_c = st.sidebar.selectbox("Select Month" , months2)
        methodz = st.sidebar.selectbox("Payment Method" , data_frm['method'].unique())
        month = data_frm['date']
        xc = []
        age_now = []
        for x in month:
            xc.append(x)
        for k in xc:
            birth = str(k['$date'])
            birthx=birth[5:7]
            try:
                birthx = int(birthx)
            except ValueError:
                pass    
            else:
                age_now.append(int(birthx))
        data_frm['month'] = age_now
        de_data = data_frm.loc[(data_frm['method'] == methodz) & (data_frm['month']==group_c )]
        sorted = pd.DataFrame(columns = data_frm.columns)
        super_data = de_data[['subjectName','amount','method','date' , 'month']]
        super_data = super_data.sort_values('subjectName')
        de_sum = de_data['amount'].sum()
        container.write(super_data)
        st.info("#Total Paid by " + methodz + " In (nth)  " + str(group_c) + " Month is Ksh " + str(de_sum))
    def analyze(data):
        
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
        #container.write("# Data Analysis On File " + to_read)
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
          

            st.info("Minimum Value show the highest discount offered")
        
        if to_view == 'Sort_Data':
            group_by_sum (data)

    def create_chart(crt,data,x_axis,y_axix):
        container.write("Data Visualization")
        
        if crt == "Bar":
            st.header("Bar Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.bar(data,x=x_axis,y=y_axix , color=x_axis , barmode="group") 
            #st.bar_chart(data , x_axis ,y_axix)
            st.plotly_chart(figure)

        

        if crt == "Line":
            st.header("Line Graph Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.line(data,x=x_axis,y=y_axix,color=x_axis )
            #st.area_chart(data[['amount','method']])
            st.plotly_chart(figure)
            
        if crt == "Histogram":
            st.header("Histogram Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.histogram(data,x=x_axis,y=y_axix , color = x_axis, text_auto = True , histfunc="avg")
            st.plotly_chart(figure)

        if crt == "Scatter_Chart":
            st.header("Scatter Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.scatter(data,x=x_axis,y=y_axix,color=x_axis,marginal_x='histogram',marginal_y='rug')
            st.plotly_chart(figure)
        
        if crt == "Pie_Chart":
            st.header("Pie Chart On Payment and Method "  )
            figure = pE.pie(data, values='amount' , names="method" )
            st.plotly_chart(figure)
    def data_visual(data):
        #st.sidebar("Select Graph Type")
        crt = st.sidebar.selectbox("Chart Type",['Pie_Chart', 'Histogram','Bar','Line','Scatter_Chart'])
        x_axis = st.sidebar.selectbox("Select X axis" , ['amount','method','recordedBy','subjecttype'])
        y_axix = st.sidebar.selectbox("Select Y Axis",['method','amount','recordedBy','subjecttype'])
        create_chart(crt,data,x_axis,y_axix)
   
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  de_menu == 'Data Analysis':
                analyze(data)
            if de_menu == 'Data Visualization':
                data_visual(data)
            if de_menu == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()
    
def beds_col():
    folder = 'jsonData/beds/'
    to_read = None
    col = beds
    with st.sidebar:
        options = top_menu()
    to_read = st.sidebar.file_uploader("Upload a Json File")
    defau = "jsonData/beds/20230630 163457604253.json"
    if to_read is None:
        to_read = defau
    def group_by_sum_bed(data):
        created_by = data['createdBy'].unique
        status = container.selectbox("Status",['Active', 'Not Active'])
            #ward = container.selectbox("Ward",['62a787e54a3424abccff1bc8'])
        if status == "Active":
            sort_data = data.loc[(data['active'] == True)]
        if status == "Not Active":
           sort_data = data.loc[(data['active'] == False)]
        container.write(sort_data)
        st.success( "Number Of Beds  " + status +" is " + str(sort_data.shape[0]))
    def analyze(data):
        container.write("# Data Analysis On File " + to_read)
        group_by_sum_bed(data)
    def create_chart(crt,data,x_axis,y_axix):
        container.write("Data Visualization")
        if crt == "Bar":
            st.header("Bar Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.bar(data,x=x_axis,y=y_axix,color=x_axis , barmode="group") 
            st.plotly_chart(figure)
        if crt == "Line":
            st.header("Line Graph Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.line(data,x=x_axis,y=y_axix )
            st.plotly_chart(figure)
            
        if crt == "Histogram":
            st.header("Histogram")
            figure = pE.histogram(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)

        if crt == "Scatter_Chart":
            st.header("Scatter Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.scatter(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)
        if crt == "Pie Chart":
            de_pie()
        

    def data_visual(data):
        #st.sidebar("Select Graph Type")
        crt = st.sidebar.selectbox("Chart Type",['Scatter_Chart','Histogram','Bar','Line'])
        x_axis = st.sidebar.selectbox("Select X axis" , data.columns)
        y_axix = st.sidebar.selectbox("Select Y Axis",data.columns)
        create_chart(crt,data,x_axis,y_axix)

    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()

#@login_required
def invent_items_col():
    inv = database['inventoryitems']
    folder ='jsonData/invent_items/'
    to_read = None
    col = inv
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    defau = "jsonData/invent_items/20230630 180431229613.json"
    if to_read is None:
        to_read = defau
    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Sort_Data'])
        container.write("# Data Analysis For Inventory")
        if to_view == 'Sort_Data':
            sec = ['category','name','account' ,'issuedIn' , 'receivedIn']
            p = ['name','account' ,'issuedIn' , 'receivedIn']
            sort_param1 = st.sidebar.selectbox("Sort By", sec)
            sort_param2 = st.sidebar.selectbox("Second Key", p, key="ghfgh")
            if not sort_param1 == sort_param2:
                    data_new = data[[sort_param1 , sort_param2 , 'date' ]]
                    container.write("Cleaned Data")
                    container.write(data_new)
            keyz = list(data['category'].unique())
            container.success("Category  Classes")
            em =[]
            for x in keyz:
                dx  = data.loc[(data['category'] ==x  )]
                container.write("*  " + x)
                container.write("Number Of Items " + str( dx.shape[0]))
                em.append(dx.shape[0])
                
                container.write(dx)
            for_g = {
            'names' : keyz,
            'vl' : em
                    }
            df_g = pd.DataFrame(for_g)

        figure = pE.histogram(df_g,x=em,y=keyz , color = em, text_auto = True)
        st.plotly_chart(figure)

        figure = pE.pie(df_g, values= em, names=keyz )
        st.plotly_chart(figure)
        

                
                


                
    with st.sidebar:
        options = top_menu()
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()


##
def single_ordersItems():
    inv = database['singleorderitems']
    folder ='jsonData/singleorderitems/'
    to_read = None
    col = inv
    options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization','Update Data'])
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    defau = "jsonData/diagnoses/20230630 180431229613.json"
    if to_read is None:
        to_read = defau
    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
        
        container.write("# Data Analysis For Inventory")
        
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
        
        if to_view == 'Sort_Data':
            data_new = sort_data(data)
            container.write("Cleaned Data")
            container.write(data_new)
            for x in data_new:
                container.write(x)
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()


##
def diagnoses_col():
    folder ='jsonData/diagnoses/'
    to_read = None
    col = diag
    with st.sidebar:
        options = top_menu() 
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    defau = "jsonData/diagnoses/20230724 132130022123.json"
    if to_read is None:
        to_read = defau
    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Sort_Data' , 'Data_Description'])
        container.write("# Data Analysis")
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
        
        if to_view == 'Sort_Data':
            gen2 = st.sidebar.selectbox("Sort By", ['code' , 'name'])
            keyz = list(data[gen2].unique())
            g = []
            for x in keyz:
                if keyz.count(x) > 1:
                    if not x in g:
                        g.append(x)
                else:
                    if not x in g:
                        g.append(x)
            second_pm = st.selectbox("parameter" ,g)
            data_new  = data.loc[(data[gen2] ==second_pm)]
            container.write("Cleaned Data")
            container.write(data_new)
            container.success("Number Of Results  " + str(data_new.shape[0]))
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                st.header("Pie Chart")
                figure = pE.pie(data , names='code' )
                st.plotly_chart(figure) 
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()




def accounts_col():
    col = accounts
    folder ='jsonData/diagnoses/'
    options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization','Update Data'])
    defau = "jsonData/accounts/20230615 194837504100.json"
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    if to_read is None:
        to_read = defau
    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
        container.write("# Data Analysis")
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
        
        if to_view == 'Sort_Data':
            data_new = sort_data(data)
            container.write("Cleaned Data")
            container.write(data_new)
            for x in data_new:
                container.write(x)

    
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()
    
    #:bar_chart:,

def invent_ledger_items():
    col = ilt
    folder ='jsonData/invent_ledger_items/'
    to_read = None
    defau = "jsonData/invent_ledger_items/20230729 225406968772.json"
    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    if to_read is None:
        to_read = defau
    

    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
        container.write("# Data Analysis")
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
        
        if to_view == 'Sort_Data':
            data2 = data[['committedOn'][3:10]]
            
            container.write(data2)
     



    with st.sidebar:
        options = top_menu()
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()




def patients_plans():
    col = pP
    folder ='jsonData/patientPlans/'
    to_read = None
    defau = "jsonData/patientPlans/20230729 231141181965.json"
    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    if to_read is None:
        to_read = defau

    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
        container.write("# Data Analysis")
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
        
        if to_view == 'Sort_Data':
            data_new = sort_data(data)
            container.write("Cleaned Data")
            container.write(data)
    
    with st.sidebar:
        options = top_menu()
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()


def queueentries():
    col = QueEnt
    folder ='jsonData/queueentries/'
    to_read = None
    defau = "jsonData/queueentries/20230802 130133492888.json"
    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    if to_read is None:
        to_read = defau

    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",[ 'Sort_Data'])
        container.write("# Queue Entries ")
       
        if to_view == 'Sort_Data':
            data_new = sort_data(data)
            container.write("Cleaned Data")
            the_date = data['date']
            the_time = data['playedOn']
            xc = []
            xc2 = []
            age_now = []
            de_time = []
            play_t = []
            for x in the_date:
                xc.append(x)
            for k in xc:
                day = str(k['$date'])
                birthx = day[0:10]
                entered = day[11:16]
                age_now.append(birthx)
                de_time.append(entered)
           
            for x in the_time:
                xc2.append(x)
            for v in xc:
                day = str(v['$date'])
                playt = day[11:16]  
                play_t.append(playt)
            data['day']=age_now
            data['Time In'] = de_time
            data['Play Time'] = play_t
            container.write(data[['_id','station','file','errored','day','Time In','played','Play Time']])
    
    with st.sidebar:
        options = top_menu()
    def create_sideMenu():
        logo = Image.open('src/images/uber.jpg')
        sidebar.image(logo,width = 55)
        if to_read is not None:
            data = pd.read_json(to_read)
            if  options == 'Data Analysis':
                analyze(data)
            if options == 'Data Visualization':
                data_visual(data)
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()






#@st.cache
def main():
    sidebar = st.sidebar
  
    # def login():
    #     container.write("Welcome")
    #     username = st.text_input("Username")
    #     password = st.text_input("password", key="log")
    #     users_ = database2['accounts']
    #     deb = st.button("Login")
    #     if deb:
    #         existing_user =  users_.find_one({"username":username})
    #         if existing_user:
    #             passc = existing_user['password']
    #             if scram.verify(password,passc):
    #                 dep = st.sidebar.selectbox("Options",options = ['Accounts', 'Patients','Transactions','Diagnoses','Beds','Inventory'])
                    
    #                 if dep == 'Patients':
    #                     patients_col()
    #                 if dep == 'Accounts':
    #                     accounts_col()
    #                 if dep == 'Transactions':
    #                     transactions_col()
    #                 if dep =='Diagnoses':
    #                     diagnoses_col()
    #                 if dep =='Beds':
    #                     beds_col()
    #                 if dep == 'Inventory':
    #                     invent_items_col()
    #                 #session['login_user'] = username
    #             else:
    #                 st.warning("Wrong Passcode")

                   

    # login()

    dep = st.sidebar.selectbox("Options",options = ['Patients','Accounts','Transactions','Diagnoses','Beds','Inventory', 'LedgerItems',
    'QueEntries','PatientsPlans'])
                    
    if dep == 'Patients':
        patients_col()
    if dep == 'Accounts':
        accounts_col()
    if dep == 'Transactions':
        transactions_col()
    if dep =='Diagnoses':
        diagnoses_col()
    if dep =='Beds':
        beds_col()
    if dep == 'Inventory':
        invent_items_col()
    if dep  == 'LedgerItems':
        invent_ledger_items()
    if dep == 'PatientsPlans':
        patients_plans()
    if dep == 'QueEntries':
        queueentries()


    






if __name__ == "__main__":
    main()
