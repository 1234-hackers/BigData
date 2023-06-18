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
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
database = client['hisani']
users_collection = database['accounts']
patients = database['patients']
transactions = database['transactions']

container = st.container()

    #write_json(collection_data)

    #pandas
    
def patient_data_analysis():
    df = pd.read_json("jsonData/20230613 185207779305.json")
    return df

   


def create_chart(crt,data,x_axis,y_axix):
    container.write("Data Visualization")
    
    if crt == "Bar":
        st.header("Bar Chart")
        figure = pE.bar(data,x=x_axis,y=y_axix , color="Country")
        st.plotly_chart(figurw)

    if crt == "Line":
        st.header("Line Graph")
        figure = pE.line(data,x=x_axis,y=y_axix)
        st.plotly_chart(figurw)
        
    if crt == "Histogram":
        st.header("Histogram")
        figure = pE.histogram(data,x=x_axis,y=y_axix , color="Country")
        st.plotly_chart(figurw)

    if crt == "Scatter Chart":
        st.header("Scatter")
        figure = pE.scatter(data,x=x_axis,y=y_axix , color="Country")
        st.plotly_chart(figurw)
    
    if crt == "Pie":
        st.header("Pie Chart")
        figure = pE.pie(data,x=x_axis,y=y_axix , color="Country")
        st.plotly_chart(figurw)


def data_visual(data):

    st.sidebar("Select Graph Type")
    crt = st.sidebar.selectbox("Chart Type",['Bar','Line','Scatter','Histogram','Pie'])
    x_axis = st.sidebar.selectbox("Select X axis" , data.columns)
    y_axix = st.sidebar.selectbox("Select Y Axis",data.columns)
    create_chart(crt,data,x_axis,y_axix)



def generate_data():

    def get_cusor(collection_name):
        csr_found = collection_name.find().limit(20)
        return csr_found

    collection_data = get_cusor(transactions)

    def get_time():
        now = datetime.now()
        fmt = now.strftime("%d/%m/%Y%H:%M:%S")
        return (now)

    def try_connection():
        if client:
            return "connected"
        else:
            return "error"
    def write_json(csr_found):
        cond = try_connection()
        if cond == "conected":
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
            write_json()
            return "New Data Collected. Upload Latest File For Analysis"

        if cond == "error":
                return "Could Not Connect to Database"

    

    return write_json()




def sort_data(data_frm):
        st.sidebar.header("Apply Filters")
        sorting = st.sidebar.selectbox("Sort By", data_frm.columns)
        new_df = data_frm.sort_values(by=sorting)
        return new_df
def group_by_sum(data_frm):
    group_c = st.sidebar.selectbox("Group By Mean" , data_frm.columns)
    grouped_by_sum = data_frm.group_by(group_c).sum()
    return grouped_by_sum

def group_by_mean(data_frm):
    group_c = st.sidebar.selectbox("Group By Mean" , data_frm.columns)
    grouped_by_mean = data_frm.group_by(group_c).mean()
    return grouped_by_mean

def analyze(data):
    container.write("# Data Analysis")
    container.write(data.head())
    container.write("Data Secription")
    container.write(data.describe())
    
    
    
    sort_data(data)
    container.write("Cleaned Data")
    container.write(new_df)

    cleaned2 = group_by_sum(data)
    container.write("Grouped by Sum")
    container.write(cleaned2)

    cleaned3 = group_by_mean(data)
    container.write("Group by Mean")
    container.write(cleaned3)

#@st.cache
def main():
    sidebar = st.sidebar
    logo = Image.open('src/images/uber.jpg')
    container.image(logo,width=250)
    st.title("DATA ANALYSIS")
    st.markdown("This is the data analyzation and Visualization")
    
    to_read  = st.sidebar.file_uploader("Upload a Json File")
    st.sidebar.image(logo,width = 55)
    
    options = st.sidebar.radio('Pages' , options=['Data Analysis' , 'Data Visualization'])

    if to_read is not None:
        
        data = pd.read_json(to_read)


        if  options == 'Data Analysis':
            analyze(data)

        if options == 'Data Visualization':
            data_visual(data)






if __name__ == "__main__":
    main()
