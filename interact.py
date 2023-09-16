# Function to create an interactive bubble
import streamlit as st 

def interactive_bubble(label):
    if st.button(label):
        st.write(f"You clicked the bubble: {label}")