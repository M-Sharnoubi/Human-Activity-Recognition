import joblib
import pandas as pd
import numpy as np
from pathlib import Path

window_size = 128
step_size = 64
sensor_names = [
    'body_acc_x', 'body_acc_y', 'body_acc_z',
    'body_gyro_x', 'body_gyro_y', 'body_gyro_z',
    'total_acc_x', 'total_acc_y', 'total_acc_z'
]

# Load the scaler once when the script starts
SCALER_PATH = Path(__file__).parent / "har_scaler.joblib"
scaler = joblib.load(SCALER_PATH)

def preprocess_data(df: pd.DataFrame):
    # Extract the columns the model expects
    sensor_data = df[sensor_names].values
    timestamps = df['timestamp'].values

    # Normalize the data before windowing
    sensor_data_scaled = scaler.transform(sensor_data)

    # Create sliding windows using the scaled data
    windows = []
    time_metadata = []
    
    for start in range(0, len(sensor_data_scaled) - window_size + 1, step_size):
        end = start + window_size
        windows.append(sensor_data_scaled[start:end])
        
        time_metadata.append({
            'window':     int(len(windows)),
            't_start_ms': float(timestamps[start]),
            't_end_ms':   float(timestamps[end - 1]),
        })

    return np.array(windows), time_metadata