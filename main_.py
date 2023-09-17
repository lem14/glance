import numpy as np
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from preprocessing import preprocessing
from data_proc import data_add
from data_proc import conf_int


"""
# Welcome to glance!

If you have any questions, checkout our [documentation]
"""
img_file_buffer = st.camera_input("Take a picture")
##PROCESSING STEPS
if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)
    img_array = np.array(img)
    img_size = np.shape(img_array)
    #st.write(str(img_size))

    # crop image to only right side
    img_array = img_array[:, int(np.floor(img_size[1] / 2)):img_size[1], :]
    img_size = np.shape(img_array)
    #segment top of image
    img_a= img_array[0:int(np.floor(img_size[0] / 2)), :, :]

    #segment bottom of image
    img_b = img_array[int(np.floor(img_size[0] / 2)):img_size[0], :, :]

    final1=preprocessing(img_a)
    cv2.imwrite("im1.png",final1)

    final2 = preprocessing(img_b)
    cv2.imwrite("im2.png", final2)

    with st.spinner('Loading..'):
        custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/'
        ocr_text_a= pytesseract.image_to_string('im1.png', config=custom_config)
        ocr_text_b= pytesseract.image_to_string('im2.png', config=custom_config)
    if len(ocr_text_a) != 0:
        a = ocr_text_a.split()
        #st.write(a)

        b = ocr_text_b.split()
        #st.write(b)
        st.subheader('Recorded Measurements')
        hr = int(a[0])
        resp = int(a[1])
        spo2 = int(a[2])
        co2 = int(b[0])
        bp = b[1][:-2]
        bps = int(bp[0:3])
        bpd = int(bp[-2:])
        mmhg = int(b[1][-2:])
        new_line = '\n'
        Path = f'''{"HR:"+ str(hr) + " RESP:"+ str(resp) + " SP02:" + str(spo2) + " CO2:"+ str(co2)+" BP:"+str(bp)+" MMHG:"+str(mmhg) }'''
        st.code(Path, language="python")

    else:
        st.write(str("nothing detected, please try again"))

    st.subheader('Previous Measurements')

    # add new measurement to previous measurements and graph
    hr_data = data_add(hr+15)  #simulation of hazardous condition
    hr_data_all = np.append(hr_data, hr)

    bps_data = data_add(bps)
    bps_data_all = np.append(bps_data, bps)

    bpd_data = data_add(bpd)
    bpd_data_all = np.append(bpd_data, bpd)

    resp_data = data_add(resp)
    resp_data_all = np.append(resp_data, resp)

    co2_data = data_add(co2)
    co2_data_all = np.append(co2_data, co2)

    spo2_data = data_add(spo2-5)
    spo2_data_all = np.append(spo2_data, spo2)

    # tabnames = st.markdown()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Heart Rate", "Systolic BP", "Diastolic",
                                                  "Respiratory Rate", "CO2", "SpO2"])

    with tab1:
        st.header("Heart Rate")
        st.line_chart(hr_data_all)

    with tab2:
        st.header("Systolic BP")
        st.line_chart(bps_data_all)

    with tab3:
        st.header("Diastolic BP")
        st.line_chart(bpd_data_all)

    with tab4:
        st.header("Respiratory Rate")
        st.line_chart(resp_data_all)

    with tab5:
        st.header("CO2")
        st.line_chart(co2_data_all)

    with tab6:
        st.header("SpO2")
        st.line_chart(spo2_data_all)







    ## configure warnings
    #determine if the point lies within confidence interval. If not, warn.
    if conf_int(hr_data, hr)==False:
        st.write("Heart rate potentially abnormal for patient!")
    else:
        st.write("Heart rate  is within normal range.")

    if conf_int(bpd_data, bpd)==False:
        st.write("Diastolic BP potentially abnormal for patient!")
    else:
        st.write("Diastolic BP is within normal range.")

    if conf_int(bps_data, bps) == False:
        st.write("Systolic BP potentially abnormal for patient!")
    else:
        st.write("Systolic BP is within normal range.")

    if conf_int(resp_data, resp) == False:
        st.write("Respiratory rate potentially abnormal for patient!")
    else:
        st.write("Respiratory rate is within normal range.")

    if conf_int(co2_data, co2) == False:
        st.write("Carbon dioxide levels potentially abnormal for patient!")
    else:
        st.write("Carbon dioxide level is within normal range.")

    if conf_int(spo2_data, spo2) == False:
        st.write("O2 saturation potentially abnormal for patient!")
    else:
        st.write("O2 saturation level is within normal range.")

