import numpy as np
import pandas as pd

existing_data = pd.DataFrame({
    'Bed_Number': ['A'] * 10,  # Existing subject
    'Time': pd.date_range(start='2023-09-16 09:00:00', periods=10, freq='H'),
    'Value': [10, 15, 12, 18, 20, 22, 25, 28, 30, 35]  # Example values for demonstration
})