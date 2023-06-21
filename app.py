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

import random
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
database = client['hisani']
users_collection = database['accounts']
patients = database['patients']
transactions = database['transactions']
accounts = database['accounts']
diag = database['diagnoses']

container = st.container()
sidebar = st.sidebar

    
months = ['Jan' , 'Feb' , 'March' , 'April', 'May','June' ,'July','Aug','Sep','Oct','Nov','Dec']
 
def data_visual(data):

    #st.sidebar("Select Graph Type")
    crt = st.sidebar.selectbox("Chart Type",['Pie_Chart', 'Histogram','Bar','Line','Scatter_Chart'])
    x_axis = st.sidebar.selectbox("Select X axis" , data.columns)
    y_axix = st.sidebar.selectbox("Select Y Axis",data.columns)
    create_chart(crt,data,x_axis,y_axix)



def generate_data(col,folder):
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
            with open(folder + de_time +'.json', 'w') as file:
                file.write(json_data)
                file.close()
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
def patients_col():
    col = patients
    folder ='jsonData/patient/' 
    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization','Update Data'])
    defau = "jsonData/patient/20230621 124514893477.json"
    if to_read is None:
        to_read = defau

    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
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
            f_params = st.selectbox("Sort By",data.columns)
            gen2 = list(data[f_params])
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
            
        
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())
    def create_chart(crt,data,x_axis,y_axix):
        container.write("Data Visualization")
        
        if crt == "Bar":
            st.header("Bar Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.bar(data,x=x_axis,y=y_axix) 
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
        crt = st.sidebar.selectbox("Chart Type",['Bar','Line','Scatter_Chart'])
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
        else:
            if options == 'Update Data':
                generate_data(col,folder)
    create_sideMenu()

def transactions_col():
    col = transactions
    folder ='jsonData/transactions/'
    defau = "jsonData/transactions/20230615 194837504100.json"
    
    options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization','Update Data'])

    to_read  = st.sidebar.file_uploader("Upload a Json File")
    if to_read is None:
        to_read = defau
    
    def group_by_sum(data_frm):
        group_c = st.sidebar.selectbox("Select Month" , months)
        methodz = st.sidebar.selectbox("Payment Method" , ['Cash', 'M-Pesa'])
        de_data = data_frm.loc[(data_frm['method'] == methodz)]
        sorted = pd.DataFrame(columns = data_frm.columns)
        super_data = de_data[['subjectName','amount','method']]
        super_data = super_data.sort_values('subjectName')
        de_sum = de_data['amount'].sum()
        container.write(super_data)
        st.info("#Total Paid by Cash is Ksh " + str(de_sum))

    def analyze(data):
        to_view = st.sidebar.selectbox("Type of Analysis",['Data_Description','Sort_Data'])
        container.write("# Data Analysis On File " + to_read)
        if to_view == 'Data_Description':
            container.write("Data Secription")
            container.write(data.describe())

            st.info("Minimum Value show the highest discount offered")
        
        if to_view == 'Sort_Data':
            group_by_sum(data)

    def create_chart(crt,data,x_axis,y_axix):
        container.write("Data Visualization")
        
        if crt == "Bar":
            st.header("Bar Chart Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.bar(data,x=x_axis,y=y_axix) 
            st.bar_chart(data[['amount','method']])
            st.plotly_chart(figure)

        

        if crt == "Line":
            st.header("Line Graph Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.line(data,x=x_axis,y=y_axix )
            st.area_chart(data[['amount','method']])
            st.plotly_chart(figure)
            
        if crt == "Histogram":
            st.header("Histogram Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.histogram(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)

        if crt == "Scatter_Chart":
            st.header("Scatter Based on " +str(x_axis )+ ' and ' + str(y_axix))
            figure = pE.scatter(data,x=x_axis,y=y_axix)
            st.plotly_chart(figure)
        
        if crt == "Pie_Chart":
            st.header("Pie Chart On Amounts Payed On Cash and M-pesa " )
            figure = pE.pie(data, values='amount' , names="method" )
            st.plotly_chart(figure)
    def data_visual(data):
        #st.sidebar("Select Graph Type")
        crt = st.sidebar.selectbox("Chart Type",['Pie_Chart', 'Histogram','Bar','Line','Scatter_Chart'])
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
    

def diagnoses_col():
    folder ='jsonData/diagnoses/'
    col = diag
    options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization','Update Data'])
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    defau = "jsonData/diagnoses/20230615 194837504100.json"
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
    
    



#@st.cache
def main():
    sidebar = st.sidebar
    logo = Image.open('src/images/uber.jpg')
    container.image(logo,width=250)
    dep = sidebar.selectbox("Collection For Analysis" , ['Accounts', 'Patients','Transactions','Diagnoses'])
    if dep == 'Patients':
        patients_col()
    if dep == 'Accounts':
        accounts_col()
    if dep == 'Transactions':
        transactions_col()
    if dep =='Diagnoses':
        diagnoses_col()

    
    






if __name__ == "__main__":
    main()
