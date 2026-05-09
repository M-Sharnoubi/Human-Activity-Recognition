from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization

def build_lstm(input_shape=(128, 9), num_classes=6):
    return Sequential([
        # First LSTM layer with 128 units and return sequences for the next LSTM layer
        LSTM(128, return_sequences=True, input_shape=input_shape),
        BatchNormalization(),
        Dropout(0.5),

        # Second LSTM layer with 64 units 
        LSTM(64),
        BatchNormalization(),
        Dropout(0.5),

        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])