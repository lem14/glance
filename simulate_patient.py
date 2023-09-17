import numpy as np
import pandas as pd

existing_data = pd.DataFrame({
    'Bed_Number': ['A'] * 10,  # Existing subject
    'Time': pd.date_range(start='2023-09-16 09:00:00', periods=10, freq='H'),
    'Systolic': [113, 125, 130, 124, 123, 112, 119, 118, 122, 120],
    'Diastolic':[79, 75, 75, 76, 71, 70, 70, 73, 78, 73],
    'HR': [10, 15, 12, 18, 20, 22, 25, 28, 30, 35],
    'RR': [78, 90, 78, 60, 97, 95, 76, 99, 62, 92],
    'CO2': [20, 40, 35, 64, 23, 25, 27, 20, 18, 24],
    'SpO2': [95, 95, 95, 95, 94, 97, 98, 91, 96, 93]
    })

length = np.size(existing_data['Systolic'])

vital_limits = pd.DataFrame({

    'Systolic_lower': [105*np.ones(length)],
    'Systolic_upper': [140*np.ones(length)],
    'Diastolic_lower':[60*np.ones(length)],
    'Diastolic_upper':[90*np.ones(length)],
    'HR_lower': [60 *np.ones(length)],
    'HR_upper': [100*np.ones(length)],
    'RR_lower': [12*np.ones(length)],
    'RR_upper': [18*np.ones(length)],
    'CO2_lower': [23*np.ones(length)],
    'CO2_upper': [29*np.ones(length)],
    'SpO2_lower': [95*np.ones(length)],
    'SpO2_upper': [100*np.ones(length)]
})