from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Dropout
from tensorflow.keras import regularizers

def build_rnn(input_shape=(128, 9), num_classes=6):
    return Sequential([
        SimpleRNN(128, return_sequences=False, input_shape=input_shape, 
                    kernel_regularizer=regularizers.l2(0.005)),
        Dropout(0.5),
        Dense(16, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])