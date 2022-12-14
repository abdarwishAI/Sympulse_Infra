# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Import required libraries
import numpy as np
#import pandas_datareader as web
import pandas as pd

#import matplotlib.pyplot as plt
plt.style.use('Solarize_Light2')
import math
import datetime
import joblib

#import os
from datetime import date
from datetime import datetime, timedelta
import streamlit as st

# Get the Stock price
import datetime
from datetime import date
from PIL import Image
image = Image.open('Sympulse_Logo.png')

colum1, colum2 = st.columns([0.2, 1])

#st.image(image, caption='Sympulses')
colum1.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


#### Streamlit Web App
colum2.title('Sympulse Infra Dimensioning')
st.write ("___________________________________________________________")

st.subheader("**Probe Solution Infra Calculator**")
col1, col2, col3 = st.columns([1, 1, 1])
#st.text_input("Enter Stock Symbol 'Ticker' examples:   FB  ,  MSFT  ,  TWTR ,  AAPL " , "TWTR")

#parameters
devices= col1.number_input('Number of Devices', 1, 1000000, value=(50))
hurs= col2.number_input('Working Hours/Day', 1, 24,value=(8))
Data_Retention = col3.number_input('Data Retention (Days)', 30, 365)

#calculations/equations
Daily_RawData_GB = round((devices * hurs), 1)
Daily_RawData_ProcessData = round((Daily_RawData_GB*2),1)
total_rawdata_GB_MinIO = round((Data_Retention*Daily_RawData_ProcessData),1)
Processed_Data_GB_YB = round((total_rawdata_GB_MinIO/4),1)
MySQL_Storage = devices

#calculating Spark cluster #############
RAM_Factor_percent = 2.7778
CPU_Factor_percent = 0.2250
Spark_Memory_GB = round((Daily_RawData_ProcessData * RAM_Factor_percent),1)
CPU_Core = round((Daily_RawData_ProcessData * CPU_Factor_percent),1)


#calculating Microservices per pod
RAM_ms = 2 * 16
CPU_ms = 2 * 2 * 4 


# show the results in a table
results = {'MinIO_Storage(GB)': f'{total_rawdata_GB_MinIO}',
           'YB_Storage(GB)': f'{Processed_Data_GB_YB}',
           'MySQL_Storage(GB)': f'{MySQL_Storage}',
           'Spark_Memory(GB)':f'{Spark_Memory_GB}',
           'CPU_Cores':f'{CPU_Core}',
           'MicroServices_Memory':f'{RAM_ms}',
           'MicroServices_CPU_Cores':f'{CPU_ms}'}

result_table_probe = pd.DataFrame.from_dict(results, orient='index',
                       columns=['infra_required'])
st.write(result_table_probe)

#
#st.write("**Infra Dimensioning per Sympulse Service Name**")
st.subheader("**Infra Dimensioning per Sympulse Service Name**")
Sympulse_Service = st.selectbox(
    'Select Sympulse Service Name',
    ('Sympulse Consumer', 'Sympulse Enterprise', 'Sympulse Report', 'Sympulse Streaming', 'Sympule Screenshare'))



if Sympulse_Service == 'Sympulse Consumer':
    col4, col5, col6 = st.columns([1, 1, 1])
    Number_of_pods_per_service_consumer = col4.number_input('No. of pods per service', 1, 3000, value=(4))

    Total_RAM_GB = round((Number_of_pods_per_service_consumer * 10),1)
    Total_CPU_Cores = round((Number_of_pods_per_service_consumer * 4),1)
    results_consumer = {'Total_RAM(GB) =':Total_RAM_GB, 
                        'CPU_Cores = ':Total_CPU_Cores}
    
    result_table_consumer = pd.DataFrame.from_dict(results_consumer, orient='index',
                           columns=['infra_required'])
    
    st.write(result_table_consumer)
    
elif Sympulse_Service == 'Sympulse Enterprise':
    col4, col5, col6 = st.columns([1, 1, 1])
    Number_of_pods_per_service_enterprise = col4.number_input('No. of pods per service', 1, 3000, value=(6))
    Total_RAM_GB = round((Number_of_pods_per_service_enterprise * 16),1)
    Total_CPU_Cores = round((Number_of_pods_per_service_enterprise * 4),1)
    results_Enterprise = {'Total_RAM(GB) =':Total_RAM_GB,
                          'CPU_Cores = ':Total_CPU_Cores}
    result_table_enterprise = pd.DataFrame.from_dict(results_Enterprise, orient='index',
                           columns=['infra_required'])
    st.write(result_table_enterprise)


elif Sympulse_Service == 'Sympulse Report':
    col4, col5, col6 = st.columns([1, 1, 1])
    Number_of_pods_per_service_report = col4.number_input('No. of pods per service', 1, 3000, value=(6))
    Total_RAM_GB = round((Number_of_pods_per_service_report * 16),1)
    Total_CPU_Cores = round((Number_of_pods_per_service_report * 4),1)
    results_Report = {'Total_RAM(GB) =':Total_RAM_GB,
                      'CPU_Cores = ':Total_CPU_Cores}
    result_table_report = pd.DataFrame.from_dict(results_Report, orient='index',
                           columns=['infra_required'])
    st.write(result_table_report)

    
elif Sympulse_Service == 'Sympulse Streaming':
    col4, col5, col6 = st.columns([1, 1, 1])
    Number_of_pods_per_service_streaming = col4.number_input('No. of pods per service', 1, 3000, value=(4))
    Total_RAM_GB = round((Number_of_pods_per_service_streaming * 6),1)
    Total_CPU_Cores = round((Number_of_pods_per_service_streaming * 4),1)
    results_Streaming = {'Total_RAM(GB) =':Total_RAM_GB,
                         'CPU_Cores = ':Total_CPU_Cores}
    result_table_Streaming = pd.DataFrame.from_dict(results_Streaming, orient='index',
                           columns=['infra_required'])
        
    st.write(result_table_Streaming)

elif Sympulse_Service == 'Sympule Screenshare':
    col4, col5, col6 = st.columns([1, 1, 1])
    Number_of_connections = col4.number_input('No. of concurrent connections', 1, 3000, value=(40))
    
    Number_of_pods_per_screenshare = Number_of_connections / 3
    Total_RAM1_GB = round((Number_of_pods_per_screenshare * 12),2)
    #st.write(type(Total_RAM1_GB))
    Total_CPU1_Cores = round((Number_of_pods_per_screenshare * 6),2)
    results_Screenshare = {'Total_RAM(GB) =':Total_RAM1_GB,
                         'CPU_Cores = ':Total_CPU1_Cores}
    result_table_Screenshare = pd.DataFrame.from_dict(results_Screenshare, orient='index',
                           columns=['infra_required'])
    
    st.write(result_table_Screenshare)



st.write ("___________________________________________________________")
st.write ('Developed By: Ahmed B. Darwish')
st.write ("ahmed.darwish@rakuten.com")
st.write ("")
st.write ("") 