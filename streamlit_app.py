from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import simulate_patient
import interact
import matplotlib
import io
from typing import List, Optional
import markdown
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
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
    warn_stats_on = st.toggle("View Warnings")

with col2:
    all_stats_on = st.toggle("View All Stats")

# build top row
col1, col2, col3, col4 = st.columns(4)

with col1:
    if all_stats_on:
        st.success('BP: 120/80, SpO2: 99', icon="✅")
    else:
        st.success('',icon="✅")

with col2:
    if all_stats_on:
        st.error('BP: 120/80, SpO2: 75', icon="🚨")
    else:
        st.error(" ", icon="🚨")

with col3:
   st.success('',icon="✅")

with col4:
   st.warning("", icon="⚠️")

# build side rows
col1, col2, col3, col4 = st.columns(4)

with col1:
   st.error(" ", icon="🚨")
   st.success('',icon="✅")
   st.warning("", icon="⚠️")

with col2:
   st.empty()

with col3:
   st.empty()

with col4:
   st.error(" ", icon="🚨")
   st.success('',icon="✅")
   st.success('',icon="✅")


patient = st.selectbox('Select Bed #:', range(1,11), 1)

def plotData(metric):
    patient_data = simulate_patient.existing_data[metric]
    st.line_chart(patient_data)

# tabnames = st.markdown()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Systolic BP", "Diastolic BP", "Heart Rate",
                                              "Respiratory Rate", "CO2", "SpO2"])

with tab1:
   st.header("Systolic BP")
   plotData('Systolic')

with tab2:
   st.header("Diastolic BP")
   plotData('Diastolic')

with tab3:
   st.header("Heart Rate")
   plotData('HR')

with tab4:
   st.header("Respiratory Rate")
   plotData('RR')

with tab5:
   st.header("CO2")
   plotData('CO2')

with tab6:
   st.header("SpO2")
   plotData('SpO2')


