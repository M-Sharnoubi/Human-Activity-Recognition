from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout, BatchNormalization

def build_gru(input_shape=(128, 9), num_classes=6):
    return Sequential([
        GRU(
            64,
            return_sequences=False,
            input_shape=input_shape
        ),

        BatchNormalization(),
        Dropout(0.3),

        Dense(64, activation='relu'),
        Dropout(0.3),

        Dense(num_classes, activation='softmax')

    ], name='Fast_GRU_Model')