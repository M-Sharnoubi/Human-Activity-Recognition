from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, BatchNormalization, Activation, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np

def build_cnn(input_shape=(128, 9), num_classes=6):
  model = Sequential([
          # First conv block
          Conv1D(filters=64, kernel_size=3, padding='same', input_shape=input_shape),
          BatchNormalization(),
          Activation('relu'),
          MaxPooling1D(pool_size=2),
          Dropout(0.2),

          # Second conv block
          Conv1D(filters=128, kernel_size=3, padding='same'),
          BatchNormalization(),
          Activation('relu'),
          MaxPooling1D(pool_size=2),
          Dropout(0.2),

          # Third conv block
          Conv1D(filters=256, kernel_size=3, padding='same'),
          BatchNormalization(),
          Activation('relu'),
          MaxPooling1D(pool_size=2),
          Dropout(0.2),

          # Fully connected layer
          Flatten(),
          Dense(units=128, activation='relu'),
          Dropout(0.5),
          Dense(units=num_classes, activation='softmax')
      ])
  return model

# model = build_cnn()
# model.summary()