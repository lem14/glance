from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import simulate_patient
import interact
import matplotlib.pyplot as plt
import numpy as np
import io
from typing import List, Optional
import markdown
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from simulate_patient import vital_limits
from plotly import express as px
from plotly.subplots import make_subplots
import pyperclip
# matplotlib.use("TkAgg")
matplotlib.use("Agg")
COLOR = "black"
BACKGROUND_COLOR = "#fff"


st.set_page_config(page_title='Glance Dashboard',  layout='wide', page_icon="🚨")

"""
# Welcome to Glance!
alerts are binary, humans are not

ICU Floor Plan
"""

# add toggle options
col1, col2, col3, col4 = st.columns(4)

with col1:
    warn_stats_on = st.toggle("View Alert Stats")

with col2:
    all_stats_on = st.toggle("View All Stats")

# build top row
col1, col2, col3, col4 = st.columns(4)

with col1:
    if all_stats_on:
        st.success('Bed 4 - BP: 118/75, SpO2: 99, HR: 78', icon="✅")
    else:
        st.success('Bed 4',icon="✅")

with col2:
    if all_stats_on | warn_stats_on:
        st.error('Bed 5 - BP: 122/81, SpO2: 75, HR: 65', icon="🚨")
    else:
        st.error("Bed 5 - LOW SpO2", icon="🚨")

with col3:
   if all_stats_on:
        st.success('Bed 6 - BP: 115/78, SpO2: 98, HR: 70', icon="✅")
   else:
        st.success('Bed 6',icon="✅")

with col4:
   if all_stats_on:
       st.warning('Bed 7 - BP: 119/73, SpO2: 98, HR: 86', icon="⚠️")
   else:
       st.warning('Bed 7 - \>2 hrs since last scan', icon="⚠️")

# build side rows
col1, col2, col3, col4 = st.columns(4)

with col1:
    if all_stats_on | warn_stats_on:
        st.error('Bed 3 - BP: 150/93, SpO2: 97, HR: 120', icon="🚨")
    else:
        st.error("Bed 3 - HIGH BP, HIGH HR", icon="🚨")
   
    if all_stats_on:
        st.success('Bed 2 - BP: 120/79, SpO2: 99, HR: 85', icon="✅")
    else:
        st.success('Bed 2',icon="✅")

    if all_stats_on:
       st.warning('Bed 1 - BP: 114/77, SpO2: 98, HR: 82', icon="⚠️")
    else:
       st.warning('Bed 1 - \>2 hrs since last scan', icon="⚠️")

with col2:
   st.empty()

with col3:
   st.empty()

with col4:
   if all_stats_on | warn_stats_on:
        st.error('Bed 8 - BP: 110/70, SpO2: 92, HR: 48', icon="🚨")
   else:
        st.error("Bed 8 - LOW HR", icon="🚨")

   if all_stats_on:
        st.success('Bed 9 - BP: 118/76, SpO2: 99, HR: 66', icon="✅")
   else:
        st.success('Bed 9',icon="✅")

   if all_stats_on:
        st.success('Bed 10 - BP: 109/71, SpO2: 99, HR: 90', icon="✅")
   else:
        st.success('Bed 10',icon="✅")   

# individual patient view
patient = st.selectbox('Select Bed #:', range(1,11), 1)

# plot recorded data
#def plotData(metric, vital_limits):
#    patient_data = simulate_patient.existing_data[metric]
#    repeat = patient_data.shape[0]
#    patient_const = simulate_patient.existing_data[metric] * repeat
#    data = [patient_data.values, np.asarray(patient_const)]
#    to_plot = pd.DataFrame(np.asarray(data).T ,columns=[metric, "const_val"])
#    st.line_chart(to_plot)

def plotData(metric, vital_limits):
    
    patient_data = simulate_patient.existing_data[metric].values

    limits = []
    for limit in vital_limits:
        if metric in limit:
            limits.append(vital_limits[limit])
   
   
    lower = limits[0].values[0]
    upper = limits[1].values[0]
    #print(f"data shape has: {patient_data.size}, lower: {lower.size}, upper: {upper.size}")

   
    data = np.asarray([lower, patient_data, upper])


    to_plot = pd.DataFrame(data.T , columns=["lower", metric, "upper"])
    st.line_chart(to_plot)



tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Systolic BP", "Diastolic BP", "Heart Rate",
                                              "Respiratory Rate", "CO2", "SpO2"])

with tab1:
   st.header("Systolic BP")
   plotData('Systolic', vital_limits)

with tab2:
   st.header("Diastolic BP")
   plotData('Diastolic', vital_limits)

with tab3:
   st.header("Heart Rate")
   plotData('HR' , vital_limits)

with tab4:
   st.header("Respiratory Rate")
   plotData('RR', vital_limits)

with tab5:
   st.header("CO2")
   plotData('CO2', vital_limits)

with tab6:
   st.header("SpO2")
   plotData('SpO2', vital_limits)